import json
import sys
import random

def load_buckets(json_file):
    """
    Load bucket data from a JSON file.
    
    Args:
    json_file (str): Path to the JSON file containing bucket data.
    
    Returns:
    dict: Dictionary containing bucket data.
    """
    try:
        with open(json_file, 'r') as file:
            buckets = json.load(file)
        return buckets
    except FileNotFoundError:
        print(f"Error: File not found {json_file}")
        sys.exit(1)

def write_simulation_files(buckets, k, percentages):
    """
    Writes simulation files for each specified percentage of total files.
    
    Args:
    buckets (dict): Dictionary containing bucket data.
    k (int): Simulation identifier.
    percentages (list of int): List of percentages to create simulations for.
    """
    base_path = './'
    chosen_files = set()
    total_files = sum(len(files) for files in buckets.values())
    bucket_ids = list(buckets.keys())
    num_buckets = len(bucket_ids)

    for percentage in percentages:
        num_files_total = total_files * percentage // 100
        num_files_to_add = num_files_total - len(chosen_files)
        files_per_bucket = max(1, num_files_to_add // num_buckets)
        additional_files = set()
        attempts = 0

        while len(additional_files) < num_files_to_add and attempts < num_buckets * 2:
            for bucket_id in bucket_ids:
                if len(additional_files) >= num_files_to_add:
                    break
                files = buckets[bucket_id]
                available_files = list(set(files) - chosen_files - additional_files)
                to_select = min(files_per_bucket, len(available_files))
                if available_files and to_select > 0:
                    selected_files = random.sample(available_files, to_select)
                    additional_files.update(selected_files)
            attempts += 1

        chosen_files.update(additional_files)
        filename = f'simulation{k}_{percentage}.txt'
        with open(base_path + filename, 'w') as file:
            file.writelines(f"{filepath}\n" for filepath in sorted(chosen_files))

        print(f"Created file {filename} with {len(chosen_files)} paths")

def main(k):
    """
    Main function to load buckets and write simulation files.
    
    Args:
    k (int): Simulation identifier.
    """
    bins_json_path = '/path/to/bins.json'
    buckets = load_buckets(bins_json_path)
    percentages = [5, 10, 25, 50, 75]
    write_simulation_files(buckets, k, percentages)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <k>")
        sys.exit(1)
    k = int(sys.argv[1])
    main(k)

