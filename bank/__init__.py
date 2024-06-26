import os
from bank.account import Account
import threading
import socket


# Obtém o caminho do diretório onde este script está localizado
script_dir = os.path.dirname(__file__)
file_path = os.path.join(script_dir, 'accounts.txt')
accounts = []

# Lendo frases do banco de dados (arquivo txt)
with open(file_path, 'r') as arq:
    data = arq.read().split('\n')
    if data[-1] == '':
        data.pop()

    for account in data:
        accounts_data = account.split(' ')
        accounts.append(Account(int(accounts_data[0]), int(accounts_data[2]), str(accounts_data[1])))


clients = {}
HOST = "127.0.0.1"  # Endereço do servidor
PORT = 40009  # Porta para escutar
