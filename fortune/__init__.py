import threading
import os


# Obtém o caminho do diretório onde este script está localizado
script_dir = os.path.dirname(__file__)
file_path = os.path.join(script_dir, 'fortune-cookies.txt')

# Lendo frases do banco de dados (arquivo txt)
with open(file_path, 'r') as arq:
    data = arq.read().split('\n')  # Lê o conteúdo do arquivo e divide por linhas
    if data[-1] == '':  # Remove a última linha se estiver vazia
        data.pop()
    arq.close() # Fecha o arquivo após a leitura


HOST = "127.0.0.1"  # Endereço do servidor
PORT = 40000  # Porta para escutar
DATABASE = threading.Semaphore(value=1) # Semáforo para controlar o acesso ao banco de dados
