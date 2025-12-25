import json
import os
import random
import string

class UserManager:
    def __init__(self, data_file='user_data.json'):
        self.data_file = data_file
    
    def load_users(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    content = f.read().strip()
                    if not content:
                        return {} 
                    return json.loads(content)
            except json.JSONDecodeError:
                return {} 
        return {}

    
    def save_users(self, users):
        with open(self.data_file, 'w') as f:
            json.dump(users, f, indent=4)
    
    def generate_user_id(self):
        letter = random.choice(string.ascii_uppercase)
        numbers = ''.join([str(random.randint(0, 9)) for _ in range(4)])
        return f"{letter}{numbers}"
    
    def register(self):
        print("\n=== REGISTRATION ===")
        email = input("Enter email address: ").strip()
        password = input("Enter password: ").strip()
        age = input("Enter age: ").strip()
        
        if not email or not password or not age:
            print("⚠️ Warning: All fields are required!")
            return None
        
        users = self.load_users()

        if email in users:
            print("⚠️ Warning: Email already registered!")
            return None
        
        user_id = self.generate_user_id()
        while any(user.get('id') == user_id for user in users.values()):
            user_id = self.generate_user_id()

        users[email] = {
            'id': user_id,
            'password': password,
            'age': age
        }
        self.save_users(users)
        
        print(f"✅ Registration successful! Your ID is: {user_id}")
        return user_id
    
    def login(self):
        print("\n=== USER LOGIN ===")
        email = input("Enter email address: ").strip()
        password = input("Enter password: ").strip()
        
        users = self.load_users()

        if email in users and users[email]['password'] == password:
            print(f"✅ Login successful! Welcome, {email}")
            print(f"Your ID: {users[email]['id']}")
            return {
                'email': email,
                'id': users[email]['id'],
                'age': users[email]['age']
            }
        else:
            print("⚠️ Warning: Invalid email or password!")
            return None
    
    def forgot_password(self):
        """Reset user password"""
        print("\n=== FORGOT PASSWORD ===")
        email = input("Enter your email address: ").strip()
        code = input("Enter your verification code: ").strip()
        
        users = self.load_users()
        
        if email not in users:
            print("⚠️ Warning: Email not found!")
            return False
        if code != users[email]['id']:
            print("⚠️ Warning: Invalid verification code!")
            print("Please contact the admin to recover your account.")
            return False
        
        age = input("Enter your age for verification: ").strip()
        
        if users[email]['age'] == age:
            new_password = input("Enter new password: ").strip()
            users[email]['password'] = new_password
            self.save_users(users)
            print("✅ Password reset successful!")
            return True
        else:
            print("⚠️ Warning: Age verification failed!")
            return False
    
    def produce_password(self):
        print("\n=== PASSWORD GENERATOR ===")
        length = input("Enter password length: ").strip()
        length = int(length) if length.isdigit() else 10    # random bir şey girerse 10 yap
        
        characters = string.ascii_letters + string.digits + "!@#$%^&*"
        password = ''.join(random.choice(characters) for _ in range(length))
        
        print(f"✅ Generated password: {password}")
        return password
    
    def get_user_by_email(self, email):
        users = self.load_users()
        return users.get(email)


class User:
    def __init__(self, user_id, email, age):
        self.id = user_id
        self.email = email
        self.age = age
    
    def __str__(self):
        return f"User(ID: {self.id}, Email: {self.email}, Age: {self.age})"
    
    def display_info(self):
        print("\n=== USER INFORMATION ===")
        print(f"ID: {self.id}")
        print(f"Email: {self.email}")
        print(f"Age: {self.age}")


'''
class User():
    def __init__(self):
        pass

    def add_user(self, email, password, age, code):
        if not os.path.exists("user_data.json"):
            with open("user_data.json", "w") as f:
                json.dump([], f)

        with open("user_data.json", "r") as f:
            users = json.load(f)

        users.append({"email": email, "password": password, "age": age, "code": code})

        with open("user_data.json", "w") as f:
            json.dump(users, f, indent=4)



user = User()
user.add_user("deneme@gmail.com", "gizli123", "20", "B2024")
'''