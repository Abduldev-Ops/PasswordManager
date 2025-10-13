import hashlib

password = "mypassword"
hashed = hashlib.sha256(password.encode()).hexdigest()
print("Hashed password:", hashed)
print()


from cryptography.fernet import Fernet

# Generate a key
key = Fernet.generate_key()
print()
print("Encryption Key:", key)

# Create a Fernet object
cipher = Fernet(key)

password = "mypassword"
encrypted = cipher.encrypt(password.encode())
print()
print("Encrypted:", encrypted)


decrypted = cipher.decrypt(encrypted).decode()
print()
print("Decrypted:", decrypted)


stored_password = encrypted
print()
print("Stored (encrypted) password:", stored_password)
print()