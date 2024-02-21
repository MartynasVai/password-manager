import tkinter as tk
import json
import base64
import base64
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
import requests
import json
import base64


from encryption import Encryption

class Managedata:
    def __init__(self):
        self.saved_key = None
        self.public_key = None
        self.saved_username = None
        self.saved_email = None
        self.encryption = Encryption()
        self.data=None
        self.reminder_data=None
        self.selected_item=None


    def decode_base64(self,encoded_data):
        # Add extra padding to make the length a multiple of 4
        padding_length = len(encoded_data) % 4
        encoded_data += '=' * ((4 - padding_length) % 4)

        # Decode URL-safe base64 with automatic padding
        try:
            decoded_data = base64.urlsafe_b64decode(encoded_data)
            return decoded_data
        except Exception as e:
            #print(f"Error decoding base64: {e}")
            return None
        


    def encode_base64(self,data):
        # Encode using URL-safe base64
        encoded_data = base64.urlsafe_b64encode(data)
        return encoded_data 
    
    def register(self,username,email,password):
        salt = self.encryption.generate_random_salt()

        password_salt, password_hash=self.encryption.generate_hash(password,None)

        base64_encoded_password_hash = self.encode_base64(password_hash).decode('utf-8')
        base64_encoded_password_salt = self.encode_base64(password_salt).decode('utf-8')
        base64_encoded_salt = self.encode_base64(salt).decode('utf-8')
        encrypted_private_key, iv, public_key = self.encryption.generate_rsa_keys(password, salt)
        base64_encoded_iv = self.encode_base64(iv).decode('utf-8')

        public_key_bytes = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

        private_key_bytes=self.encryption.decrypt_private_key(encrypted_private_key, password, salt, iv)

        private_key = serialization.load_pem_private_key(
        private_key_bytes,
        password=None,  
        backend=default_backend()
        )


        base64_encoded_encrypted_private_key = self.encode_base64(encrypted_private_key).decode('utf-8')
        base64_encoded_public_key = self.encode_base64(public_key_bytes).decode('utf-8')

        self.saved_key=private_key
        self.saved_email=email
        self.saved_username=username
        self.public_key=public_key_bytes

        user_data = {
        'username': username,
        'email': email,
        'salt': base64_encoded_salt,
        'iv': base64_encoded_iv,
        'public_key':base64_encoded_public_key,
        'encrypted_private_key':base64_encoded_encrypted_private_key,
        'password_hash': base64_encoded_password_hash,
        'password_salt': base64_encoded_password_salt
        }
        # Convert the JSON object to a string
        json_data = json.dumps(user_data)

        # send the JSON data to the registration endpoint 
        register_url = 'https://flask-production-97c9.up.railway.app/register'
        payload = {
            'json_data': json_data,
        }

        registration_response = requests.post(register_url, json=payload)
        #Check if the registration request was successful
        if registration_response.status_code == 200:
            #print('Registration successful!')

            private_key = serialization.load_pem_private_key(
            private_key_bytes,
            password=None,  
            backend=default_backend()
            )
            #self.saved_key=private_key
            self.saved_email=email
            self.saved_username=username


            return True
        else:
            print(f'Error: {registration_response.status_code} - {registration_response.json()}')
            return False



    def login(self,username,password):
        get_salt_url = 'https://flask-production-97c9.up.railway.app/login?action=get_salt&username=' + username
        response = requests.get(get_salt_url)

        if response.status_code == 200:
            data = response.json()
            password_salt = data.get('password_salt')
            password_salt = self.decode_base64(password_salt)
            #print(f'Password Salt: {password_salt}')
        else:
            #print(f'Error: {response.status_code} - {response.json()}')
            pass

        #pass
        ###########################################################################################CHECK HASHES AND THEN VERIFY
        #print("Checking hash")
        password_salt, password_hash = self.encryption.generate_hash(password, password_salt)
        base64_encoded_password_hash = self.encode_base64(password_hash).decode('utf-8')
        check_hash_url = 'https://flask-production-97c9.up.railway.app/login?action=check_hash&username=' + username + '&password_hash=' + base64_encoded_password_hash
        response = requests.get(check_hash_url)
        if response.status_code == 200:
            data = response.json()
            encrypted_private_key = self.decode_base64(data.get('encrypted_private_key'))
            public_key=self.decode_base64(data.get('public_key'))
            self.public_key=public_key
            iv = self.decode_base64(data.get('iv'))
            salt = self.decode_base64(data.get('salt'))
            email=data.get('email')
            #print(f'Encrypted Private Key: {encrypted_private_key}')
            #print(f'IV: {iv}')
            #print(f'Password Salt: {salt}')
        else:
            #print(f'Error: {response.status_code} - {response.json()}')
            pass###########################################################################################VERIFY--------------------------
        private_key_bytes=self.encryption.decrypt_private_key(encrypted_private_key, password, salt, iv)

        private_key = serialization.load_pem_private_key(
        private_key_bytes,
        password=None,  
        backend=default_backend()
        )
        self.saved_key=private_key
        self.saved_email=email
        self.saved_username=username
            # sign username with private key
        #print(username.encode('utf-8'))
        signature=self.encryption.generate_signature(username,self.saved_key)
        #signature = private_key.sign(
        #    username.encode('utf-8'),
        #    padding.PSS(
        #        mgf=padding.MGF1(hashes.SHA256()),
        #        salt_length=padding.PSS.MAX_LENGTH
        #    ),
        #    hashes.SHA256()
        #
        #)
        #print(signature)
        signature=self.encode_base64(signature).decode('utf-8')

        verify_url = 'https://flask-production-97c9.up.railway.app/login?action=verify&username=' + username + '&signature=' + signature
        #print(verify_url)
        response = requests.get(verify_url)

        if response.status_code == 200:
            
            #print('Login attempt successful')
            self.read_data(username)
            return response.status_code
        else:
            #print(f'Error: {response.status_code} - {response.json()}')
            return response.status_code
        #print("a")

    def read_data(self,username):

        signature=self.encryption.generate_signature(username,self.saved_key)
        b64signature=self.encode_base64(signature).decode('utf-8')
        record_data = {
        'verification': b64signature,
        'username': username,
        #'password_salt': base64_encoded_password_salt
        }
        # Convert the JSON object to a string
        json_data = json.dumps(record_data)

        
        # send the JSON data to the registration endpoint 
        read_url = 'https://flask-production-97c9.up.railway.app/read_info'
        payload = {
            'json_data': json_data,
        }

        response = requests.post(read_url, json=payload)
        #print(f'Response: {response.status_code} - {response.json()}')
        if response.status_code == 200:
            # Extract the data from the JSON response
            response_data = response.json()
            data = response_data.get('data', [])
            reminder_data= response_data.get('reminder_records',[])
            # Now 'data' contains the extracted data
            self.data=data
            self.reminder_data=reminder_data
            #print("\n\n\n")
            #print(data)
            #print("\n\n\n")
            #print(reminder_data)

        pass


    def create(self,title,username,email,password):

        signature = self.encryption.generate_signature(self.saved_username, self.saved_key)
        

        b64signature=self.encode_base64(signature).decode('utf-8')

        encrypted_password=self.encryption.encrypt_with_public_key(password.encode('utf-8'),self.public_key)
        b64encrypted_password=self.encode_base64(encrypted_password).decode('utf-8')



        record_data = {
        'verification': b64signature,
        'creator_username': self.saved_username,
        'title': title,
        'username': username,
        'password':  b64encrypted_password,
        'email': email
        #'password_salt': base64_encoded_password_salt
        }
        # Convert the JSON object to a string
        json_data = json.dumps(record_data)

        
        # send the JSON data to the registration endpoint 
        create_url = 'https://flask-production-97c9.up.railway.app/saveinfo'
        payload = {
            'json_data': json_data,
        }

        response = requests.post(create_url, json=payload)
        ##print(f'Error: {response.status_code} - {response.json()}')
        self.read_data(self.saved_username)
        if response.status_code==200:
            return True
        else:
            return False


    def edit(self,title,username,email,password,original_title):
        signature = self.encryption.generate_signature(self.saved_username, self.saved_key)

        

        b64signature=self.encode_base64(signature).decode('utf-8')

        encrypted_password=self.encryption.encrypt_with_public_key(password.encode('utf-8'),self.public_key)
        b64encrypted_password=self.encode_base64(encrypted_password).decode('utf-8')



        record_data = {
        'verification': b64signature,
        'creator_username': self.saved_username,
        'title': title,
        'username': username,
        'password':  b64encrypted_password,
        'email': email,
        'original_title': original_title
        #'password_salt': base64_encoded_password_salt
        }
        # Convert the JSON object to a string
        json_data = json.dumps(record_data)

        
        # send the JSON data to the registration endpoint 
        edit_url = 'https://flask-production-97c9.up.railway.app/edit_info'
        payload = {
            'json_data': json_data,
        }

        response = requests.post(edit_url, json=payload)
        ###print(f'Error: {response.status_code} - {response.json()}')
        self.read_data(self.saved_username)
        if response.status_code==200:
            return True
        else:
            return False





    def delete_record(self, title):
        signature = self.encryption.generate_signature(self.saved_username, self.saved_key)

        b64signature=self.encode_base64(signature).decode('utf-8')
        record_data = {
        'verification': b64signature,
        'creator_username': self.saved_username,
        'title': title
        #'password_salt': base64_encoded_password_salt
        }
        # Convert the JSON object to a string
        json_data = json.dumps(record_data)

        
        # send the JSON data to the registration endpoint 
        delete_url = 'https://flask-production-97c9.up.railway.app/delete_info'
        payload = {
            'json_data': json_data,
        }

        response = requests.post(delete_url, json=payload)
        ###print(f'Error: {response.status_code} - {response.json()}')
        self.read_data(self.saved_username)

    def delete_account(self):
        signature = self.encryption.generate_signature(self.saved_username, self.saved_key)
        b64signature=self.encode_base64(signature).decode('utf-8')
        record_data = {
        'verification': b64signature,
        'creator_username': self.saved_username
        #'password_salt': base64_encoded_password_salt
        }
        json_data = json.dumps(record_data)
        delete_acc_url = 'https://flask-production-97c9.up.railway.app/delete_acc'
        payload = {
            'json_data': json_data,
        }
        self.saved_key = None
        self.public_key = None
        self.saved_username = None
        self.data=None
        self.selected_item=None

        response = requests.post(delete_acc_url, json=payload)

    def edit_acc(self,username,email,password):
        salt = self.encryption.generate_random_salt()

        password_salt, password_hash=self.encryption.generate_hash(password,None)

        base64_encoded_password_hash = self.encode_base64(password_hash).decode('utf-8')
        base64_encoded_password_salt = self.encode_base64(password_salt).decode('utf-8')
        base64_encoded_salt = self.encode_base64(salt).decode('utf-8')
        encrypted_private_key, iv, public_key = self.encryption.generate_rsa_keys(password, salt)
        base64_encoded_iv = self.encode_base64(iv).decode('utf-8')

        public_key_bytes = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

        private_key_bytes=self.encryption.decrypt_private_key(encrypted_private_key, password, salt, iv)

        private_key = serialization.load_pem_private_key(
        private_key_bytes,
        password=None,  
        backend=default_backend()
        )


        base64_encoded_encrypted_private_key = self.encode_base64(encrypted_private_key).decode('utf-8')
        base64_encoded_public_key = self.encode_base64(public_key_bytes).decode('utf-8')

        #self.saved_key=private_key
        #self.saved_email=email
        #self.saved_username=username
        #self.public_key=public_key_bytes





        if self.data is not None:
            result = [{'_id': record['_id'], 'creator_username': record['creator_username'], 'password': record['password']} for record in self.data]
        else:
            result = []

        for record in result:
            # Change the values of the specified fields
            record['creator_username'] = username
            password_to_decrypt=self.decode_base64(record['password'])
            decrypted_password=self.encryption.decrypt_with_private_key(password_to_decrypt,self.saved_key)
            encrypted_password=self.encryption.encrypt_with_public_key(decrypted_password,public_key_bytes)
            new_password=self.encode_base64(encrypted_password).decode('utf-8')
            record['password'] = new_password

        creator_username=self.saved_username
        signature=self.encryption.generate_signature(creator_username,self.saved_key)
        b64signature=self.encode_base64(signature).decode('utf-8')
        user_data = {
        'creator_username':creator_username,
        'verification':b64signature,
        'username': username,
        'email': email,
        'salt': base64_encoded_salt,
        'iv': base64_encoded_iv,
        'public_key':base64_encoded_public_key,
        'encrypted_private_key':base64_encoded_encrypted_private_key,
        'password_hash': base64_encoded_password_hash,
        'password_salt': base64_encoded_password_salt,
        'changed_record_data': result
        }
        # Convert the JSON object to a string
        json_data = json.dumps(user_data)
        edit_acc_url = 'https://flask-production-97c9.up.railway.app/edit_acc'
        payload = {
            'json_data': json_data,
        }

        response = requests.post(edit_acc_url, json=payload)
        self.saved_key=private_key
        self.saved_email=email
        self.saved_username=username
        self.public_key=public_key_bytes
        ##print(f'Response: {response.status_code} - {response.json()}')
        if response.status_code==200:
            return True
        else:
            return False

    def create_reminder(self,title,text,date,time):


        signature = self.encryption.generate_signature(self.saved_username, self.saved_key)
        

        b64signature=self.encode_base64(signature).decode('utf-8')

        record_data = {
        'verification': b64signature,
        'creator_username': self.saved_username,
        'title': title,
        'text': text,
        'date':  date,
        'time': time
        #'password_salt': base64_encoded_password_salt
        }
        # Convert the JSON object to a string
        json_data = json.dumps(record_data)

        
        # send the JSON data to the registration endpoint 
        create_url = 'https://flask-production-97c9.up.railway.app/create_reminder'
        payload = {
            'json_data': json_data,
        }
        print(payload)

        response = requests.post(create_url, json=payload)
        print(f'Error: {response.status_code} - {response.json()}')
        self.read_data(self.saved_username)



    def edit_reminder(self,title,text,date,time,new_title,creator_id):


        signature = self.encryption.generate_signature(self.saved_username, self.saved_key)
        

        b64signature=self.encode_base64(signature).decode('utf-8')

        record_data = {
        'verification': b64signature,
        'creator_id': creator_id,
        'new_title': new_title,
        'title': title,
        'text': text,
        'date':  date,
        'time': time,
        'username':self.saved_username
        #'password_salt': base64_encoded_password_salt
        }
        # Convert the JSON object to a string
        json_data = json.dumps(record_data)

        
        # send the JSON data to the registration endpoint 
        edit_url = 'https://flask-production-97c9.up.railway.app/edit_reminder'
        payload = {
            'json_data': json_data,
        }

        response = requests.post(edit_url, json=payload)
        ###print(f'Error: {response.status_code} - {response.json()}')

        self.read_data(self.saved_username)
        if response.status_code==200:
            return True
        else:
            return False

    def delete_reminder(self, id):
        signature = self.encryption.generate_signature(self.saved_username, self.saved_key)
        b64signature=self.encode_base64(signature).decode('utf-8')

        record_data = {
        'verification': b64signature,
        '_id': id,
        'username':self.saved_username
        #'password_salt': base64_encoded_password_salt
        }
        # Convert the JSON object to a string
        json_data = json.dumps(record_data)

        
        # send the JSON data to the registration endpoint 
        deletereminder_url = 'https://flask-production-97c9.up.railway.app/delete_reminder'
        payload = {
            'json_data': json_data,
        }
        response = requests.post(deletereminder_url, json=payload)
        self.read_data(self.saved_username)
        pass

