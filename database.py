import sqlite3
from cryptography.fernet import Fernet

class DatabaseManager:

    def __init__(self, database_name = 'pass.db'):
        self.conn = sqlite3.connect(database_name)
        self.cursor = self.conn.cursor()
        self.key = self.load_key()
        self.cipher = Fernet(self.key)
        self.create_table()

    #created table using sqlite3
    #id, acc(also can be username), pass, website(optional)
    def create_table(self):
        self.cursor.execute("""
                            CREATE TABLE IF NOT EXISTS passwords(
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            acc TEXT,
                            pass TEXT,
                            website TEXT)
                        """)
        
        self.conn.commit()

    def load_key(self):
        try: 
            key_file = open("keyFile", "rb")
            key = key_file.read()
            key_file.close()
            return key
        except FileNotFoundError:
            key = Fernet.generate_key()
            key_file = open("keyFile", "wb")
            key_file.write(key)
            key_file.close()
            return key
    
    
    def add_pass(self, acc_name, password, website):
        encrypt_pass = self.cipher.encrypt(password.encode())
        self.cursor.execute("INSERT INTO passwords (acc, pass, website) VALUES (?,?,?)", (acc_name, encrypt_pass, website))
        self.conn.commit()

    """
    since its going to be encrypted, decrypt it and let it change pass, when trying to change, show both pass acc and website to be sure that it is and give back opt ig
        make username case sensitive as it was inputted
        if any wrong thing is inputted, account for error
        multiple usernames but youre looking for one, check if there ae multiple, if there is, ask for email used if not just give entire passes
        """
    def change_pass(self, acc_name, new_pass, website):
        encrypt_pass = self.cipher.encrypt(new_pass.encode())
        self.cursor.execute("UPDATE passwords SET pass = ? WHERE acc = ? AND website = ?",(encrypt_pass, acc_name, website))
        self.conn.commit()
        print("Change successful")

    def remove_pass(self, acc_name, website):
        self.cursor.execute("DELETE FROM passwords WHERE acc = ? AND website = ?", (acc_name, website))
        self.conn.commit()
        return self.cursor.rowcount > 0

    def get_all(self):
        self.cursor.execute("SELECT acc, website FROM passwords")
        pass_result = self.cursor.fetchall()
        return pass_result


    def get_one(self, acc_name, website):
        self.cursor.execute("SELECT * FROM passwords WHERE acc = ? AND website = ?", (acc_name, website))
        info = self.cursor.fetchone()
        if info:
            dec_pass = self.cipher.decrypt(info[2]).decode()
            return (info[1], dec_pass, info[3])
        return None
    
    def close(self):
        self.conn.close()