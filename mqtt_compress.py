import os
import argparse
import time
import argparse
import shutil

def compress_large_files(directory, max_size_mb=100):
    # Check if the directory exists
    if not os.path.exists(directory):
        print(f"Directory '{directory}' does not exist.")
        return
    
    csv_files = [f for f in os.listdir(directory) if f.endswith('.csv')]
    
    for file in csv_files:
        file_path = os.path.join(directory, file)
        file_size_mb = os.path.getsize(file_path) / (1024 * 1024)  # Convert bytes to MB
        
        if file_size_mb >= max_size_mb:
            # Create an archive if any file is equal to or larger than max_size_mb
            archive_name = f'{file[:-4]}_archive.7z'
            command = f'7z a "{os.path.join(directory, archive_name)}" "{file_path}"'
            os.system(command)
            
            print(f"File '{file}' is larger than {max_size_mb} MB. Archived as '{archive_name}'")
            
            # Remove the original CSV file after compression
            os.remove(file_path)
            print(f"Original file '{file}' removed.")
        else:
            print(f"File '{file}' is less than {max_size_mb} MB.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compress large CSV files and remove originals")
    parser.add_argument("directory", help="Directory path containing CSV files")
    parser.add_argument("--maxsize", type=int, default=100, help="Maximum size in MB for a file to be compressed")
    parser.add_argument("--delay", type=int, default=60, help="Delay in seconds between checks")
    args = parser.parse_args()

    while True:
        compress_large_files(args.directory, args.maxsize)
        time.sleep(args.delay)  # Check at specified intervals
