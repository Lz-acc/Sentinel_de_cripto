import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
from encryptor import (
    criptografar_fernet, descriptografar_fernet,
    criptografar_aes, descriptografar_aes
)
from pathlib import Path

pasta_selecionada = ""

def selecionar_pasta():
    global pasta_selecionada
    pasta_selecionada = filedialog.askdirectory()
    if pasta_selecionada:
        lbl_pasta.config(text=f"Pasta selecionada: {pasta_selecionada}")

def criptografar():
    if not pasta_selecionada:
        messagebox.showwarning("Aviso", "Selecione uma pasta primeiro!")
        return
    senha = entry_senha.get()
    if not senha:
        messagebox.showwarning("Aviso", "Digite uma senha!")
        return
    threading.Thread(target=lambda: rodar_criptografia(senha, True)).start()

def descriptografar():
    if not pasta_selecionada:
        messagebox.showwarning("Aviso", "Selecione uma pasta primeiro!")
        return
    senha = entry_senha.get()
    if not senha:
        messagebox.showwarning("Aviso", "Digite uma senha!")
        return
    threading.Thread(target=lambda: rodar_criptografia(senha, False)).start()

def atualizar_progresso(valor, maximo):
    progress["maximum"] = maximo
    progress["value"] = valor
    root.update_idletasks()

def salvar_log():
    if txt_log.get("1.0", tk.END).strip():
        arquivo_log = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if arquivo_log:
            with open(arquivo_log, "w", encoding="utf-8") as f:
                f.write(txt_log.get("1.0", tk.END))
            messagebox.showinfo("Log salvo", f"Log salvo em {arquivo_log}")

def rodar_criptografia(senha, cript):
    tipo = combo_algoritmo.get()
    arquivos = [f for f in Path(pasta_selecionada).rglob("*") if f.is_file()]
    total = len(arquivos)
    txt_log.delete("1.0", tk.END)
    try:
        for i, caminho in enumerate(arquivos, 1):
            try:
                if cript:
                    if tipo == "Fernet":
                        criptografar_fernet(str(caminho.parent), senha)
                    elif tipo == "AES-128":
                        criptografar_aes(str(caminho.parent), senha, bits=128)
                    elif tipo == "AES-256":
                        criptografar_aes(str(caminho.parent), senha, bits=256)
                else:
                    if tipo == "Fernet":
                        descriptografar_fernet(str(caminho.parent), senha)
                    elif tipo == "AES-128":
                        descriptografar_aes(str(caminho.parent), senha, bits=128)
                    elif tipo == "AES-256":
                        descriptografar_aes(str(caminho.parent), senha, bits=256)
                # Log sucesso
                txt_log.insert(tk.END, f"✔ {caminho}\n", "sucesso")
            except ValueError as ve:
                txt_log.insert(tk.END, f"✖ {caminho} - {ve}\n", "erro")
            txt_log.see(tk.END)
            atualizar_progresso(i, total)
        messagebox.showinfo("Concluído", f"Pasta {'criptografada' if cript else 'descriptografada'} ({tipo}) finalizada!")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {e}")
    finally:
        progress["value"] = 0

# --- GUI ---
root = tk.Tk()
root.title("CriptoSentinel PIVACITY SECURE")
root.geometry("650x450")
root.configure(bg="black")

# Estilos dark
style = ttk.Style()
style.theme_use('default')
style.configure("TCombobox", fieldbackground="black", background="black", foreground="white")
style.configure("TProgressbar", troughcolor="#444", background="green")

# Botões e labels
btn_selecionar = tk.Button(root, text="Selecionar Pasta", command=selecionar_pasta, bg="#222", fg="white")
btn_selecionar.pack(pady=10)

lbl_pasta = tk.Label(root, text="Nenhuma pasta selecionada", bg="black", fg="white")
lbl_pasta.pack(pady=5)

tk.Label(root, text="Digite a senha:", bg="black", fg="white").pack()
entry_senha = tk.Entry(root, show="*", bg="#222", fg="white", insertbackground="white")
entry_senha.pack(pady=5)

tk.Label(root, text="Escolha a criptografia:", bg="black", fg="white").pack()
opcoes = ["Fernet", "AES-128", "AES-256"]
combo_algoritmo = ttk.Combobox(root, values=opcoes)
combo_algoritmo.current(0)
combo_algoritmo.pack(pady=5)

btn_cript = tk.Button(root, text="Criptografar Pasta", command=criptografar, bg="green", fg="white")
btn_cript.pack(pady=5)

btn_decript = tk.Button(root, text="Descriptografar Pasta", command=descriptografar, bg="red", fg="white")
btn_decript.pack(pady=5)

btn_salvar_log = tk.Button(root, text="Salvar Log", command=salvar_log, bg="#555", fg="white")
btn_salvar_log.pack(pady=5)

# Barra de progresso
progress = ttk.Progressbar(root, orient="horizontal", length=550, mode="determinate")
progress.pack(pady=10)

# Log de arquivos
txt_log = tk.Text(root, height=12, bg="#111", fg="white")
txt_log.pack(pady=5, fill="both", expand=True)

# Tags para cores do log
txt_log.tag_configure("sucesso", foreground="lime")
txt_log.tag_configure("erro", foreground="red")

root.mainloop()
