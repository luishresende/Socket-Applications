import threading
import os


# Obtém o caminho do diretório onde este script está localizado
script_dir = os.path.dirname(__file__)
file_path = os.path.join(script_dir, 'fortune-cookies.txt')

# Lendo frases do banco de dados (arquivo txt)
with open(file_path, 'r') as arq:
    data = arq.read().split('\n')
    if data[-1] == '':
        data.pop()
    arq.close()


HOST = "127.0.0.1"  # Endereço do servidor
PORT = 40000  # Porta para escutar
DATABASE_UPDATE = threading.Semaphore(value=1) # Semáforo para controlar o acesso ao banco de dados
