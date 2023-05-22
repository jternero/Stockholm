import hashlib
import base64

'''
This script generates a Fernet key based on a string.
'''

# Convert a string to a Fernet key
def get_key(password):
    sha256 = hashlib.sha256()
    sha256.update(password.encode())
    digest = sha256.digest()
    key = base64.urlsafe_b64encode(digest)
    return key

# Prompt the user to enter a string
string = input("Enter a string: ")

# Generate a Fernet key based on the string
key = get_key(string)

# Print the key
print("Fernet key:", key.decode())