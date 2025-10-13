from database import DatabaseManager
from crypt import CRYPTO_MANAGER
import hashlib

class MAIN:
    def __init__(self):
        self.db = DatabaseManager()
        print("Welcome to Secure Password Manager")
        confirmation = self.master_setup()
        if confirmation:
            self.start()
        
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
    
    def start(self):
        print("[1] Add new account \n[2] Retrieve account\n[3] List all accounts\n[4] Delete account\n[5] Change password\n[6] Exit")
        user = int(input("Choose an option: "))
        while (user != 6):
            while (user not in [1, 2, 3, 4, 5,6]):
                print("Options are between 1-5")
                user = int(input("Choose an option: "))
                
            if (user == 1):
                self.add_acc()
                print("[1] Add new account \n[2] Retrieve account\n[3] List all accounts\n[4] Delete account\n[5] Change password\n[6] Exit")
                user = int(input("Choose an option: "))
            elif (user == 2):
                self.retr_acc()
                print("[1] Add new account \n[2] Retrieve account\n[3] List all accounts\n[4] Delete account\n[5] Change password\n[6] Exit")
                user = int(input("Choose an option: "))
            elif (user == 3):
                self.list_acc()
                print("[1] Add new account \n[2] Retrieve account\n[3] List all accounts\n[4] Delete account\n[5] Change password\n[6] Exit")
                user = int(input("Choose an option: "))
            elif (user == 4):
                self.del_acc()
                print("[1] Add new account \n[2] Retrieve account\n[3] List all accounts\n[4] Delete account\n[5] Change password\n[6] Exit")
                user = int(input("Choose an option: "))
            elif (user == 5):
                self.change_pass()
                print("[1] Add new account \n[2] Retrieve account\n[3] List all accounts\n[4] Delete account\n[5] Change password\n[6] Exit")
                user = int(input("Choose an option: "))
                
        if (user == 6):
                print("Goodbye")
                self.db.close()

    def add_acc(self):
        username = input("Enter username: ")
        password = input ("Enter password: ")
        site = input("Enter site/label: ")

        self.db.add_pass(username, password, site)
        print("Account saved securely! \n\n" + "-" * 15)

    def retr_acc(self):
        username = input("Enter username to be fetched: ")
        site = input("Enter site/label: ")
        print()

        result  = self.db.get_one(username, site)
        if (result == None):
            print("No record Found")
        else:
            print(f"Account: {result[0]}\nPassword: {result[1]} \nWebsite: {result[2]} \n\n" + "-" * 15)

    def list_acc(self):
        print("Accounts: ")
        accounts = self.db.get_all()
        for acc in accounts:
            print(f"- {acc[0]} ({acc[1]})")
        
        print("-" * 15)

    def change_pass(self):
        username = input("Enter username to be fetched: ")
        site = input("Enter site/label: ")
        result  = self.db.get_one(username, site)
        if(result != None):
            print(f"Account: {result[0]}\nPassword: {result[1]} \nWebsite: {result[2]}")
            ans = input("Is this the correct account? (Y/N) ").capitalize()
            if ans == "Y":
                new_pass = input("Enter the new password: ")
                self.db.change_pass(username, new_pass, site)
                print("-" * 15)
            elif ans == "N":
                print("Password not changed!")
                print("-" * 15)
        elif (result== None):
            print("No record found")
            print("\n-" * 15)

    def del_acc(self):
        username = input("Enter username to be fetched: ")
        site = input("Enter site/label: ")

        result  = self.db.get_one(username, site)
        if(result != None):
            print(f"Account: {result[0]}\nPassword: {result[1]} \nWebsite: {result[2]}")
            ans = input("You're about to delete this account. (Y/N)").capitalize()
            if (ans == "Y" and self.db.remove_pass(username, site)):
                print("Password deleted!")
            elif ans == "N": 
                print("Password not deleted")
        elif (result == None):
            print("No record found")
            print("\n-" * 15)

def main():
    pass_manager = MAIN()

if __name__ == "__main__":
    main()