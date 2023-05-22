# Stockholm 

## Ransomware Simulation
> This code simulates the WannaCry ransomware encryption/decryption process.

  

## Usage

*To encrypt files:*

    python stockholm.py

> You will be prompted to enter an encryption key. 
> Enter a key with at least 16 characters.

  

*To decrypt files:*

    python stockholm.py -r YOUR_KEY

> Replace YOUR_KEY with the key you entered during encryption.

  

## Features

 - Encrypts/decrypts files with AES-CBC encryption using a key and IV
   
  - Adds .ft extension to encrypted files
   
 - Creates an "infection" folder to hold encrypted files
   
  - Supports encrypting/decrypting a variety of common file types
   
   - Provides silent mode to suppress output
   
   - Displays version information with -v flag


## Requirements

> - Python 3.7+
> - Cryptodome library

Install the Cryptodome library with:

    pip install Cryptodome

## Disclaimer

*This code is for educational purposes only. I do not condone using ransomware to harm others.*

