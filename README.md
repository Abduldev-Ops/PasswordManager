![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)
![Security](https://img.shields.io/badge/AES_Encryption-Fernet-green?style=for-the-badge)# PasswordManager
# 🔒 Secure Password Manager (CLI Version)

## 🧩 Problem
Managing multiple online accounts often leads to weak or reused passwords.  
This project solves that by providing a **secure, offline password manager** built in Python,  
which encrypts stored credentials inside a local SQLite database.

---

## 🚀 Solution
This application uses the **Fernet encryption system** from Python’s `cryptography` library  
to securely encrypt and decrypt passwords.  

It features a simple **command-line interface (CLI)** that lets users:
- Add accounts  
- Retrieve stored passwords  
- List all saved accounts  
- Delete credentials securely  

---

## ✨ Features
- 🔐 AES-based encryption using Fernet  
- 💾 Local SQLite database (`pass.db`)  
- 🧰 Object-Oriented Design (`DatabaseManager` and `MAIN` classes)  
- 🖥️ Interactive CLI for CRUD operations  
- 🔑 Secret key stored locally in `secret.key`

---

## 🛠️ Technologies Used
| Component | Technology |
|------------|-------------|
| Language | Python |
| Database | SQLite3 |
| Encryption | `cryptography.fernet` |
| Interface | Command Line (CLI) |

---

## 💻 How to Run

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/<your-username>/PasswordManager.git
cd PasswordManager
