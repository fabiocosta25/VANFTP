import os
import tkinter as tk
from tkinterdnd2 import TkinterDnD, DND_FILES
from tkinter import messagebox, filedialog
from tkinter import ttk
from ftplib import FTP
import threading

# Configurações FTP (defina suas credenciais aqui)
FTP_SERVER_IP = 'ip_servidorftp'
FTP_USERNAME = 'Usuario'
FTP_PASSWORD = 'Senha'

# Função para lidar com o evento de arrastar e soltar arquivos
def on_file_drop(event):
    file_paths = root.tk.splitlist(event.data)
    add_files_to_list(file_paths)

# Função para adicionar arquivos à lista
def add_files_to_list(file_paths):
    for file_path in file_paths:
        ext = os.path.splitext(file_path)[1].lower()
        
        if ext in ['.mp4', '.mxf', '.jpg', '.png', '.mkv']:
            # Adiciona apenas arquivos válidos
            label = tk.Label(frame, text=os.path.basename(file_path))
            label.pack(anchor='w', padx=10, pady=2)
            files.append(file_path)
        else:
            # Indica que o arquivo não é válido
            label = tk.Label(frame, text=f"{os.path.basename(file_path)} (Arquivo inválido)", fg='red')
            label.pack(anchor='w', padx=10, pady=2)

# Função para procurar arquivos manualmente
def browse_files():
    video_files = filedialog.askopenfilenames(
        title="Selecione os vídeos",
        filetypes=(("Arquivos de Vídeo", "*.mp4;*.mxf"), ("Todos os Arquivos", "*.*")),
    )
    add_files_to_list(video_files)

# Função para enviar os arquivos
def send_files_threaded():
    # Coloca o envio de arquivos em uma thread separada
    threading.Thread(target=send_files).start()

def send_files():
    folder_name = folder_name_entry.get().strip()  # Pega o nome da pasta da entrada
    if not folder_name:
        messagebox.showerror("Erro", "Por favor, insira o nome da pasta.")
        return
    
    try:
        # Conexão ao servidor FTP
        ftp = FTP(FTP_SERVER_IP)
        ftp.login(user=FTP_USERNAME, passwd=FTP_PASSWORD)
        
        # Tenta criar a pasta no servidor FTP
        try:
            ftp.mkd(folder_name)
        except Exception as e:
            print(f"A pasta já existe ou ocorreu um erro ao criar a pasta: {e}")
        
        ftp.cwd(folder_name)  # Navega para a nova pasta

        # Calcula o tamanho total de todos os arquivos para acompanhamento da porcentagem total
        total_size = sum(os.path.getsize(file_path) for file_path in files)
        total_sent = 0  # Quantidade total enviada

        for file_path in files:
            file_size = os.path.getsize(file_path)
            progress_bar["value"] = 0
            progress_bar["maximum"] = file_size

            # Enviar arquivo com barra de progresso visual
            def upload_callback(data):
                nonlocal total_sent
                progress_bar["value"] += len(data)  # Atualiza barra de progresso visual para o arquivo atual
                total_sent += len(data)  # Atualiza o total de bytes enviados
                total_percentage = (total_sent / total_size) * 100  # Calcula a porcentagem total
                percentage_label.config(text=f"Progresso Total: {total_percentage:.2f}%")  # Exibe porcentagem
                root.update_idletasks()  # Atualiza a interface do tkinter dinamicamente

            upload_with_progress(ftp, file_path, upload_callback)

        ftp.quit()
        messagebox.showinfo("Envio Concluído", "Todos os arquivos foram enviados com sucesso!")
        clear_files()  # Limpa os arquivos após o envio
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {e}")

# Função para fazer upload com barra de progresso
def upload_with_progress(ftp, file_path, callback):
    try:
        with open(file_path, 'rb') as f:
            # Envia o arquivo com callback para atualizar a barra de progresso
            ftp.storbinary(f'STOR {os.path.basename(file_path)}', f, 1024, callback)
    except Exception as e:
        print(f"Erro ao enviar o arquivo {file_path}: {e}")

# Função para limpar a lista de arquivos e o canvas
def clear_files():
    global files
    files = []  # Limpa a lista de arquivos
    for widget in frame.winfo_children():
        widget.destroy()  # Remove todos os labels da área de arquivos
    progress_bar["value"] = 0  # Reseta a barra de progresso
    percentage_label.config(text="Progresso Total: 0%")  # Reseta a porcentagem

# Janela principal
root = TkinterDnD.Tk()
root.title("VANFTP")
root.geometry("600x450")

# Lista para armazenar os arquivos a serem enviados
files = []

# Criação do canvas e do scrollbar
canvas = tk.Canvas(root, bg="lightgrey", highlightthickness=1, relief="sunken")
scrollbar = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)
frame = tk.Frame(canvas, bg="white")

# Configurações do canvas
frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

canvas.create_window((0, 0), window=frame, anchor='nw')
canvas.configure(yscrollcommand=scrollbar.set)

# Layout do canvas e do scrollbar
canvas.pack(side='left', fill='both', expand=True, padx=10, pady=10)
scrollbar.pack(side='right', fill='y')

# Área de arrastar e soltar
drop_area = tk.Label(root, text="Arraste e solte arquivos aqui", bg="lightblue", width=50, height=10,
                      relief="raised", bd=2, anchor='center')
drop_area.pack(pady=10)
drop_area.drop_target_register(DND_FILES)
drop_area.dnd_bind('<<Drop>>', on_file_drop)

# Campo para inserir o nome da pasta
tk.Label(root, text="Nome da pasta no servidor:").pack(pady=5)
folder_name_entry = tk.Entry(root, width=40)
folder_name_entry.pack(pady=5)

# Barra de progresso
progress_bar = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
progress_bar.pack(pady=10)

# Botão para procurar arquivos de vídeo
browse_button = tk.Button(root, text="Procurar Vídeos", command=browse_files)
browse_button.pack(pady=5)

# Botão para enviar
send_button = tk.Button(root, text="Enviar", command=send_files_threaded)
send_button.pack(pady=10)

# Label para exibir a porcentagem total de envio
percentage_label = tk.Label(root, text="Progresso Total: 0%")
percentage_label.pack(pady=5)

# Botão para limpar a lista de arquivos
clear_button = tk.Button(root, text="Limpar Lista", command=clear_files)
clear_button.pack(pady=5)

root.mainloop()
