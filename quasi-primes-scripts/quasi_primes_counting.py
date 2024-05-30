import sys
import time
from collections import defaultdict

KMER_LENGTH = 16

def encode_kmer(kmer):
    """ Encodes a Kmer string into a 32-bit integer representation. """
    encoded_kmer = 0
    for nucleotide in kmer:
        encoded_kmer <<= 2
        if nucleotide == 'C':
            encoded_kmer |= 1
        elif nucleotide == 'G':
            encoded_kmer |= 2
        elif nucleotide == 'T':
            encoded_kmer |= 3
    return encoded_kmer

def decode_kmer(encoded):
    """ Decodes a 32-bit integer representation back to a Kmer string. """
    kmer = ['A'] * KMER_LENGTH
    for i in range(KMER_LENGTH - 1, -1, -1):
        bits = encoded & 3
        if bits == 1:
            kmer[i] = 'C'
        elif bits == 2:
            kmer[i] = 'G'
        elif bits == 3:
            kmer[i] = 'T'
        encoded >>= 2
    return ''.join(kmer)

def process_kmer_file(filepath, species_id, kmer_map):
    """ Processes each Kmer in a file and updates the map accordingly. """
    try:
        with open(filepath, 'r') as file:
            for kmer in file:
                kmer = kmer.strip()
                if len(kmer) != KMER_LENGTH:
                    continue
                encoded_kmer = encode_kmer(kmer)
                if encoded_kmer in kmer_map:
                    if kmer_map[encoded_kmer][0] != species_id:
                        kmer_map[encoded_kmer] = (0, True)  # Different species, set to 0
                else:
                    kmer_map[encoded_kmer] = (species_id, False)  # New entry
    except FileNotFoundError:
        print(f"Failed to open file: {filepath}", file=sys.stderr)

def load_input_file(input_file, kmer_map):
    """ Loads an input file and processes each line as a file path with a species id. """
    try:
        with open(input_file, 'r') as file:
            file_count = 0
            start_time = time.time()
            for line in file:
                parts = line.strip().split()
                if len(parts) != 2:
                    print(f"Invalid line in input file: {line}", file=sys.stderr)
                    continue
                filepath, species_id = parts
                species_id = int(species_id)
                process_kmer_file(filepath, species_id, kmer_map)
                file_count += 1
                if (time.time() - start_time) > 600:  # 10 minutes check
                    print(f"Processed {file_count} file paths so far.")
                    print(f"Current size of kmerMap: {len(kmer_map)}")
                    start_time = time.time()
    except FileNotFoundError:
        print(f"Failed to open input file: {input_file}", file=sys.stderr)

def save_kmer_map(kmer_map, output_file_path):
    """ Saves the kmer map to an output file. """
    try:
        with open(output_file_path, 'w') as file:
            for encoded_kmer, (species_id, _) in kmer_map.items():
                if species_id != 0:  # Check if the species_id is not zero
                    decoded_kmer = decode_kmer(encoded_kmer)
                    file.write(f"{decoded_kmer} {species_id}\n")
    except FileNotFoundError:
        print(f"Failed to open output file: {output_file_path}", file=sys.stderr)

def main():
    if len(sys.argv) != 3:
        print("Usage: python script.py <input_file_path> <output_file_path>", file=sys.stderr)
        return 1
    input_file_path, output_file_path = sys.argv[1:3]
    kmer_map = defaultdict(lambda: (0, False))  # Using defaultdict for automatic handling of missing keys
    load_input_file(input_file_path, kmer_map)
    save_kmer_map(kmer_map, output_file_path)

if __name__ == "__main__":
    main()

