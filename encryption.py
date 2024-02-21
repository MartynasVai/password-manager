from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os
from cryptography.hazmat.primitives.padding import PKCS7
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import padding
import hashlib


class Encryption:

    @staticmethod
    def generate_rsa_keys(password, salt):
        # Generate a random RSA key pair
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        public_key = private_key.public_key()



        private_key_bytes = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        #print("private_key\n")
        #print(private_key_bytes)
        #print("private_key_end:\n")
    #
    #
        #public_key_bytes = public_key.public_bytes(
        #encoding=serialization.Encoding.PEM,
        #format=serialization.PublicFormat.SubjectPublicKeyInfo
        #)
        #print("public_key:\n")
        #print(public_key_bytes.decode('utf-8'))  # Decode to print as a string
        #print("public_key_end:\n")
        #PRINT THE KEY##########################################################################################################################
        # Generate a random IV
        iv = os.urandom(16)



        # Encrypt the private key with the password
        encrypted_private_key, iv = Encryption.encrypt_private_key(private_key_bytes, password, salt, iv)

        return encrypted_private_key, iv, public_key
    
    @staticmethod
    def encrypt_private_key(private_key, password, salt, iv):
        # Derive a symmetric encryption key from the password
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        key = kdf.derive(password.encode('utf-8'))

        # Apply PKCS7 padding to the private key
        padder = PKCS7(128).padder()
        padded_private_key = padder.update(private_key) + padder.finalize()


        # Encrypt the padded private key with the derived symmetric key
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        encrypted_private_key = encryptor.update(padded_private_key) + encryptor.finalize()

        # Return the encrypted private key and the IV
        return encrypted_private_key, iv
    
    @staticmethod
    def decrypt_private_key(encrypted_private_key, password, salt, iv):#FOR LOGIN#######################################################################
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        key = kdf.derive(password.encode('utf-8'))

        # Decrypt the encrypted private key with the derived symmetric key
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        padded_private_key = decryptor.update(encrypted_private_key) + decryptor.finalize()

        # Remove the PKCS7 padding from the private key
        unpadder = PKCS7(128).unpadder()
        private_key = unpadder.update(padded_private_key) + unpadder.finalize()

    #PRINT THE KEY##########################################################################################################################
    #    print("DECRYPTED private_key\n")
    #    print(private_key.decode('utf-8'))
    #    print("private_key_end:\n")
    #PRINT THE KEY##########################################################################################################################

        return private_key

    @staticmethod
    def encrypt_with_public_key(data, public_key_bytes):
        # Serialize the public key to bytes
        #public_key_bytes = public_key.public_bytes(
        #    encoding=serialization.Encoding.PEM,
        #    format=serialization.PublicFormat.SubjectPublicKeyInfo
        #)

        # Load the public key
        loaded_public_key = serialization.load_pem_public_key(
            public_key_bytes,
            backend=default_backend()
        )

        # Encrypt the data with the public key
        encrypted_data = loaded_public_key.encrypt(
            data,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        print(encrypted_data)
        print("^^ENCRYPTED DATA\n")
        return encrypted_data

    @staticmethod
    def decrypt_with_private_key(encrypted_data, private_key):


        # Serialize the private key to bytes
        private_key_bytes = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )


        # Load the private key
        loaded_private_key = serialization.load_pem_private_key(
            private_key_bytes,
            password=None,  # No password since encryption_algorithm=serialization.NoEncryption()
            backend=default_backend()
        )

        # Decrypt the data with the private key
        decrypted_data = loaded_private_key.decrypt(
            encrypted_data,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )


        return decrypted_data
    
    @staticmethod
    def generate_signature(message, private_key):
         
        signature = private_key.sign(
        message.encode('utf-8'),
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
        )
        return signature
    
    @staticmethod
    def generate_hash(password, salt):
        if salt is None:
            salt = os.urandom(32)  # 32 bytes for a strong salt

        # Combine password and salt and hash the result using SHA-256
        hashed_password = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 1000000)

        # Return the salt and hashed password as bytes
        print(hashed_password)
        return salt, hashed_password
    
    @staticmethod
    def generate_random_salt():
        return os.urandom(16)