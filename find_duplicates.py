import os
import hashlib
import sys
from collections import defaultdict

def get_file_hash(path):
    """Calculates the SHA256 hash of a file."""
    hasher = hashlib.sha256()
    try:
        with open(path, 'rb') as f:
            while chunk := f.read(8192):
                hasher.update(chunk)
        return hasher.hexdigest()
    except (IOError, OSError) as e:
        print(f"Error reading file {path}: {e}", file=sys.stderr)
        return None

def find_duplicate_files(root_dir):
    """Finds duplicate files in a directory and its subdirectories."""
    if not os.path.isdir(root_dir):
        print(f"Error: Directory '{root_dir}' does not exist.", file=sys.stderr)
        return {}

    print("Phase 1: Scanning for files by size...")
    files_by_size = defaultdict(list)
    file_count = 0
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            file_count += 1
            print(f"\rScanned {file_count} files...", end="", flush=True)
            path = os.path.join(dirpath, filename)
            if not os.path.islink(path):
                try:
                    size = os.path.getsize(path)
                    files_by_size[size].append(path)
                except OSError as e:
                    # Print error on new line to not interfere with progress indicator
                    print(f"\nError accessing file {path}: {e}", file=sys.stderr)
    print(f"\nScan complete. Found {file_count} total files.")

    print("\nPhase 2: Hashing potential duplicates...")
    hashes_by_size = defaultdict(list)
    
    # Identify files that need hashing
    files_to_hash = []
    for size in files_by_size:
        if len(files_by_size[size]) > 1:
            files_to_hash.extend(files_by_size[size])
            
    total_to_hash = len(files_to_hash)
    if total_to_hash == 0:
        print("No files with matching sizes found. No hashing needed.")
        return {}

    print(f"Found {total_to_hash} files with matching sizes to analyze.")
    
    for i, path in enumerate(files_to_hash):
        # Progress bar logic
        progress = ((i + 1) / total_to_hash)
        bar_length = 40
        filled_length = int(bar_length * progress)
        bar = '█' * filled_length + '-' * (bar_length - filled_length)
        print(f'\rHashing: |{bar}| {progress:.1%} ({i+1}/{total_to_hash})', end="", flush=True)
        
        file_hash = get_file_hash(path)
        if file_hash:
            hashes_by_size[file_hash].append(path)
    
    print("\nHashing complete.")
    
    duplicates = {k: v for k, v in hashes_by_size.items() if len(v) > 1}
    return duplicates

def manage_duplicates(duplicates):
    """Manages duplicate files based on user input."""
    if not duplicates:
        print("No duplicate files found.")
        return

    print(f"\nFound {len(duplicates)} set(s) of duplicate files.\n")
    
    for i, (file_hash, paths) in enumerate(duplicates.items()):
        print(f"--- Set {i+1} of {len(duplicates)} ---")
        for j, path in enumerate(paths):
            print(f"  {j+1}: {path}")

        while True:
            choice = input("Enter the number of the file to keep (e.g., '1'), or 'all' to keep all: ").strip().lower()
            
            if choice == 'all':
                print("Keeping all files in this set.\n")
                break
            
            try:
                choice_index = int(choice) - 1
                if 0 <= choice_index < len(paths):
                    file_to_keep = paths[choice_index]
                    files_to_delete = [p for p in paths if p != file_to_keep]
                    
                    for f in files_to_delete:
                        try:
                            os.remove(f)
                            print(f"Deleted: {f}")
                        except OSError as e:
                            print(f"Error deleting file {f}: {e}", file=sys.stderr)
                    
                    print(f"Kept: {file_to_keep}\n")
                    break
                else:
                    print("Invalid number. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a number or 'all'.")

def main():
    """Main function to run the duplicate file finder."""
    if len(sys.argv) > 1:
        root_directory = sys.argv[1]
    else:
        root_directory = input("Enter the root directory to scan: ").strip()

    if not root_directory:
        print("No directory provided. Exiting.", file=sys.stderr)
        return

    print(f"\nStarting duplicate file scan in '{root_directory}'...\n")
    duplicates = find_duplicate_files(root_directory)
    manage_duplicates(duplicates)

if __name__ == "__main__":
    main()