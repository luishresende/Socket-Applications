import os
from bank.account import Account
import threading
import socket


# Obtém o caminho do diretório onde este script está localizado
script_dir = os.path.dirname(__file__)
file_path = os.path.join(script_dir, 'accounts.txt')
accounts = [] # Lista que armazenará as contas bancárias

# Lendo frases do banco de dados (arquivo txt)
with open(file_path, 'r') as arq:
    data = arq.read().split('\n') # Lê o conteúdo do arquivo e divide por linhas
    if data[-1] == '': # Remove a última linha se estiver vazia
        data.pop()

    for account in data:
        accounts_data = account.split(' ') # Divide cada linha em partes separadas por espaço
        # Cria uma instância de Account e adiciona à lista de contas
        accounts.append(Account(int(accounts_data[0]), int(accounts_data[2]), str(accounts_data[1])))


clients = {} # Dicionário que armazenará os clientes conectados
HOST = "127.0.0.1"  # Endereço do servidor
PORT = 40003  # Porta para escutar as conexões