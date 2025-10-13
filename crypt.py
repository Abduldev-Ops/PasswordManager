import hashlib
from database import DatabaseManager

class CRYPTO_MANAGER:

    def __init__(self):
        self.db = DatabaseManager()
        self.master_setup()
    
    def master_setup(self):
        checker = False
        self.db.cursor.execute("""
                            CREATE TABLE IF NOT EXISTS vault(
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            master_hash TEXT)
                            """)
        self.db.conn.commit

        self.db.cursor.execute("SELECT master_hash FROM vault where id = 1")
        mast_pass = self.db.cursor.fetchone()

        if mast_pass is None:
            print("No master password found. Create one now.")
            master_pass = input("Enter new master password: ")
            hashed = self.hash_master(master_pass)
            self.db.cursor.execute("INSERT INTO vault (id, master_hash) VALUES (1,?)", (hashed,))
            self.db.conn.commit()
            print("Master password set.")
            checker = True
        else:
            count = 0
            entry_attempt = input("Enter master password to unlock vault: ")
            while not self.verify_master(entry_attempt, mast_pass[0]) and count < 3:
                print("Incorrect master password; Try again")
                entry_attempt = input("Enter master password to unlock vault: ")
                count += 1
            if self.verify_master(entry_attempt, mast_pass[0]):
                checker = True
            if count == 3:
                print("!!! Too many attempts !!!\nExiting")
                checker = False
        return checker

    def hash_master(self, password):
        salt = b'static_salt'
        return hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000).hex()
    
    def verify_master(self, password, stored_hash):
        salt = b'static_salt'
        check = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000).hex()
        return check == stored_hash