# FTP Upload App

![image](https://github.com/user-attachments/assets/4ac1646e-fad7-4b90-9cb9-227e58b9d4ce)


Este é um aplicativo de interface gráfica (GUI) desenvolvido em Python usando `Tkinter` e `tkinterdnd2` que permite arrastar e soltar arquivos de vídeo (`.mp4`, `.mxf`) para fazer upload para um servidor FTP. O aplicativo também exibe uma barra de progresso que mostra o status do envio dos arquivos.

## Funcionalidades

- Arraste e solte arquivos diretamente na interface.
- Suporte para arquivos de vídeo `.mp4` e `.mxf`.
- Barra de progresso que acompanha o envio de cada arquivo e do total.
- Exibição da porcentagem total de upload.
- Limpeza automática da lista após o envio completo.
- Botão para limpar manualmente a lista de arquivos.

## Requisitos

- Python 3.x
- Bibliotecas Python:
  - `tkinterdnd2`
  - `tkinter` (geralmente incluído com Python)
  - `ftplib`
  - `threading`

## Instalação

1. Clone este repositório:

   ```bash
   git clone https://github.com/fabiocosta25/VANFTP.git
   cd seu-repositorio
