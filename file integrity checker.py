import hashlib
import os
import json

# Function to calculate SHA-256 hash of a file
def calculate_hash(file_path):
    sha256 = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            while chunk := f.read(4096):  # Read file in chunks
                sha256.update(chunk)
        return sha256.hexdigest()
    except FileNotFoundError:
        return None

# Function to generate and save file hashes
def generate_file_hashes(directory, hash_file="hashes.json"):
    file_hashes = {}
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            file_hashes[file_path] = calculate_hash(file_path)
    
    with open(hash_file, "w") as f:
        json.dump(file_hashes, f, indent=4)
    
    print(f"Hashes saved in {hash_file}")

# Function to verify file integrity
def verify_integrity(directory, hash_file="hashes.json"):
    try:
        with open(hash_file, "r") as f:
            stored_hashes = json.load(f)
    except FileNotFoundError:
        print("Hash file not found! Run the hash generation first.")
        return
    
    current_hashes = {}
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            current_hashes[file_path] = calculate_hash(file_path)

    for file, old_hash in stored_hashes.items():
        new_hash = current_hashes.get(file)
        if new_hash is None:
            print(f"[DELETED] {file} has been removed!")
        elif old_hash != new_hash:
            print(f"[MODIFIED] {file} has been changed!")

    for file in current_hashes:
        if file not in stored_hashes:
            print(f"[NEW FILE] {file} has been added!")

    print("Integrity check completed.")

# Example usage
if __name__ == "__main__":
    folder_to_monitor = "test_folder"  # Change this to the folder you want to monitor

    # Generate initial hashes
    generate_file_hashes(folder_to_monitor)

    # Verify integrity (run after modifying files to test)
    verify_integrity(folder_to_monitor)
