import os
import json

# Configuration
DIRECTORY_PATHS = [
    '/path/to/first/directory',
    '/path/to/second/directory'
]
NUM_BUCKETS = 5
SCHEDULER_OUTPUT_PATH = '/path/to/output/directory/bins.json'

def get_file_sizes(directories):
    """
    Collects the file paths and sizes within given directory paths.
    Args:
    directories (list of str): List of directory paths.

    Returns:
    list of tuples: List containing (filepath, filesize) tuples.
    """
    file_sizes = []
    for directory in directories:
        try:
            for filename in os.listdir(directory):
                filepath = os.path.join(directory, filename)
                if os.path.isfile(filepath):
                    file_sizes.append((filepath, os.path.getsize(filepath)))
        except FileNotFoundError:
            print(f"Directory not found: {directory}")
    return file_sizes

def create_buckets(file_sizes, num_buckets):
    """
    Distributes files into a specified number of buckets based on size, in a round-robin fashion.
    Args:
    file_sizes (list of tuples): List of (filepath, filesize).
    num_buckets (int): Number of buckets to distribute files into.

    Returns:
    tuple: (buckets dictionary, bucket sizes dictionary).
    """
    sorted_files = sorted(file_sizes, key=lambda x: x[1], reverse=True)
    buckets = {i: [] for i in range(num_buckets)}
    bucket_sizes = {i: 0 for i in range(num_buckets)}

    for i, file_info in enumerate(sorted_files):
        bucket_id = i % num_buckets
        buckets[bucket_id].append(file_info[0])
        bucket_sizes[bucket_id] += file_info[1]

    return buckets, bucket_sizes

def save_to_json(buckets, output_path):
    """
    Saves the bucket distribution to a JSON file.
    Args:
    buckets (dict): Dictionary containing the file buckets.
    output_path (str): Path to save the JSON file.
    """
    with open(output_path, 'w') as f:
        json.dump(buckets, f, indent=4)

def main():
    file_sizes = get_file_sizes(DIRECTORY_PATHS)
    buckets, bucket_sizes = create_buckets(file_sizes, NUM_BUCKETS)
    save_to_json(buckets, SCHEDULER_OUTPUT_PATH)

    print(f"Scheduler has been saved to {SCHEDULER_OUTPUT_PATH}")
    for bucket_id in sorted(bucket_sizes):
        print(f"Bucket {bucket_id} total size: {bucket_sizes[bucket_id]} bytes")

if __name__ == "__main__":
    main()

