import json
import subprocess
import os
import sys
import re
import gzip
from Bio.Seq import Seq
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

SCHEDULER_JSON_PATH = "/path/to/extractions.json"

def run_jellyfish(fasta_path, kmer_length, output_dir):
    """
    Runs Jellyfish to count kmers in a given FASTA file.
    """
    try:
        identifier = re.search(r'(GCF|GCA)_\d+\.\d+', os.path.basename(fasta_path)).group()
        jellyfish_db = os.path.join(output_dir, f'{identifier}.jf')
        output_file = os.path.join(output_dir, f'{identifier}_kmer_counts.txt')

        subprocess.run(['jellyfish', 'count', '-m', str(kmer_length), '-s', '100M', '-t', '10', '-C', fasta_path, '-o', jellyfish_db], check=True)
        subprocess.run(['jellyfish', 'dump', '-c', jellyfish_db, '-o', output_file], check=True)
        return output_file
    except subprocess.CalledProcessError as e:
        logging.error(f"Jellyfish processing failed: {e}")
        raise

def reverse_complement(kmer):
    """
    Returns the reverse complement of a kmer.
    """
    return str(Seq(kmer).reverse_complement())

def process_kmers(kmers_file, output_file):
    """
    Processes kmers from Jellyfish output and writes kmer and its reverse complement to file.
    """
    try:
        with open(kmers_file, 'r') as infile, open(output_file, 'w') as outfile:
            for line in infile:
                kmer, count = line.strip().split()
                rev_comp = reverse_complement(kmer)
                outfile.write(f"{kmer}\n")
                if rev_comp != kmer:
                    outfile.write(f"{rev_comp}\n")
    except IOError as e:
        logging.error(f"Error processing kmers: {e}")
        raise

def decompress_gz_file(gz_path, output_path):
    """
    Decompresses a gzipped file.
    """
    try:
        with gzip.open(gz_path, 'rt') as gz_file, open(output_path, 'w') as out_file:
            out_file.write(gz_file.read())
    except IOError as e:
        logging.error(f"Error decompressing file {gz_path}: {e}")
        raise

def process_bucket(bucket_id, base_output_dir):
    """
    Processes all files in a given bucket.
    """
    try:
        with open(SCHEDULER_JSON_PATH, 'r') as file:
            scheduler = json.load(file)
        
        if bucket_id not in scheduler:
            logging.warning(f"Bucket ID {bucket_id} not found in the scheduler.")
            return

        output_dir = base_output_dir
        os.makedirs(output_dir, exist_ok=True)

        for filepath in scheduler[bucket_id]:
            logging.info(f"Processing {filepath} in bucket {bucket_id}...")
            identifier = re.search(r'(GCF|GCA)_\d+\.\d+', filepath).group()
            decompressed_path = os.path.join(output_dir, f'{identifier}.fna')
            decompress_gz_file(filepath, decompressed_path)
            kmers_file = run_jellyfish(decompressed_path, 16, output_dir)
            output_file = os.path.join(output_dir, f'{identifier}_16mers.txt')
            process_kmers(kmers_file, output_file)
            os.remove(decompressed_path)
            os.remove(os.path.join(output_dir, f'{identifier}.jf'))
            os.remove(os.path.join(output_dir, f'{identifier}_kmer_counts.txt'))
    except Exception as e:
        logging.error(f"Error processing bucket {bucket_id}: {e}")
        raise

if __name__ == "__main__":
    if len(sys.argv) != 3:
        logging.error("Usage: python script.py bucket_id /path/to/output_directory")
        sys.exit(1)
    bucket_id, output_directory_path = sys.argv[1:3]
    process_bucket(bucket_id, output_directory_path)

