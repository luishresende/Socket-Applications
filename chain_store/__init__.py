import threading
import os
import socket
import random
import time


# Obtém o caminho do diretório onde este script está localizado
script_dir = os.path.dirname(__file__)
file_path = os.path.join(script_dir, 'products.txt')

products = {}
# Lendo frases do banco de dados (arquivo txt)
with open(file_path, 'r') as arq:
    data = arq.read().split('\n')
    product_id = 1
    for i in range(0, len(data), 3):
        products[product_id] = {'name': data[i], 'price': float(data[i + 1])}
        product_id += 1
    arq.close()


HOST = "127.0.0.1"  # Endereço do servidor
PORT = 40004  # Porta para escutar


from .query import Query
query = Query()
print(products)
