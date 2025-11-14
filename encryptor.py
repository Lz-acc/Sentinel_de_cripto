from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from base64 import urlsafe_b64encode
import hashlib
from pathlib import Path
import os

# ----------------------------------------
# GERAÇÃO DE CHAVE A PARTIR DA SENHA
# ----------------------------------------
def gerar_chave(senha: str, tamanho=32):
    return hashlib.sha256(senha.encode()).digest()[:tamanho]


# ----------------------------------------
# FERNET
# ----------------------------------------
def criptografar_fernet(pasta: str, senha: str):
    chave = urlsafe_b64encode(gerar_chave(senha))
    f = Fernet(chave)
    for caminho in Path(pasta).rglob("*"):
        if caminho.is_file():
            with open(caminho, "rb") as arq:
                dados = arq.read()
            with open(caminho, "wb") as arq:
                arq.write(f.encrypt(dados))


def descriptografar_fernet(pasta: str, senha: str):
    chave = urlsafe_b64encode(gerar_chave(senha))
    f = Fernet(chave)
    for caminho in Path(pasta).rglob("*"):
        if caminho.is_file():
            with open(caminho, "rb") as arq:
                dados = arq.read()
            try:
                dados_decript = f.decrypt(dados)
            except InvalidToken:
                raise ValueError("Senha incorreta ou arquivo corrompido!")
            with open(caminho, "wb") as arq:
                arq.write(dados_decript)


# ----------------------------------------
# AES (CBC)
# ----------------------------------------
def criptografar_aes(pasta: str, senha: str, bits=256):
    chave = gerar_chave(senha, tamanho=bits//8)
    for caminho in Path(pasta).rglob("*"):
        if caminho.is_file():
            with open(caminho, "rb") as arq:
                dados = arq.read()
            padder = padding.PKCS7(128).padder()
            padded_data = padder.update(dados) + padder.finalize()
            iv = os.urandom(16)
            cipher = Cipher(algorithms.AES(chave), modes.CBC(iv), backend=default_backend())
            encryptor = cipher.encryptor()
            ciphertext = encryptor.update(padded_data) + encryptor.finalize()
            with open(caminho, "wb") as arq:
                arq.write(iv + ciphertext)


def descriptografar_aes(pasta: str, senha: str, bits=256):
    chave = gerar_chave(senha, tamanho=bits//8)
    for caminho in Path(pasta).rglob("*"):
        if caminho.is_file():
            with open(caminho, "rb") as arq:
                dados = arq.read()
            iv = dados[:16]
            ciphertext = dados[16:]
            cipher = Cipher(algorithms.AES(chave), modes.CBC(iv), backend=default_backend())
            decryptor = cipher.decryptor()
            padded_data = decryptor.update(ciphertext) + decryptor.finalize()
            try:
                unpadder = padding.PKCS7(128).unpadder()
                data = unpadder.update(padded_data) + unpadder.finalize()
            except:
                raise ValueError("Senha incorreta ou arquivo corrompido!")
            with open(caminho, "wb") as arq:
                arq.write(data)
