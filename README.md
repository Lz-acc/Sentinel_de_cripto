# Sentinel de Cripto 🔒

**CriptoSentinel** is a Python-based folder encryption tool with a user-friendly GUI. It supports multiple encryption algorithms and allows users to securely encrypt and decrypt entire directories.

---

## Features

- Encrypt and decrypt entire folders
- Supports **Fernet**, **AES-128**, and **AES-256**
- Generates secure keys from passwords
- Real-time log of encrypted/decrypted files
- Dark-themed GUI using **Tkinter**
- Progress bar to track operations
- Save operation logs for future reference

---

## Installation

1. Clone the repository:

git clone 
```
https://github.com/Lz-acc/Sentinel_de_Cripto.git
```
Install dependencies:
```
pip install cryptography
```
Run the GUI:
```
python main.py
```
Usage
Select the folder you want to encrypt or decrypt.

Enter a password.

Choose the encryption algorithm (Fernet, AES-128, AES-256).

Click "Encrypt Folder" or "Decrypt Folder".

Monitor progress in the log section.

Save the log if needed.

Security
Passwords are converted to secure keys using SHA-256.

AES uses CBC mode with random IV for each file.

Fernet ensures authenticated encryption for safety.

Credits
Developed by:

Lorenzo Accasto

Eduardo Augusto

Luan Pereira

Pedro Lucas

License
MIT License
