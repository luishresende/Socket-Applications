import random
import time
from chain_store import socket, HOST, PORT, threading


def generate_random_sale(store_id): # Função para gerar uma venda aleatória
    return f"VENDA {store_id} {random.randint(1, 96)} {random.randint(1, 100)}"


def generate_random_purchase(store_id): # Função para gerar uma compra aleatória
    return f"COMPRA {store_id} {random.randint(1, 96)} {random.randint(40, 500)}"


def connect_to_server(store_id): # Função para conectar ao servidor
    operations = 0
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: # Cria um socket
        s.connect((HOST, PORT)) # Conecta ao servidor
        print(f"Conectado ao servidor {HOST}:{PORT}") # Exibe a mensagem de conexão
        while operations < 1500: # Loop para enviar comandos ao servidor

            # Recebe comando do usuário
            msg = random.choice([generate_random_sale(store_id), generate_random_sale(store_id), generate_random_sale(store_id), generate_random_sale(store_id), generate_random_sale(store_id), generate_random_purchase(store_id)])
            # Envia o comando ao servidor
            s.sendall(msg.encode()) # Envia a mensagem ao servidor

            operations += 1 # Incrementa o contador de operações
            time.sleep(random.uniform(0, 3)) # Espera um tempo aleatório

            response = s.recv(1024) # Recebe a resposta do servidor
            response = response.decode() # Decodifica a resposta

            print(f"Resposta do servidor: {response}")


def run():

    for new_id in range(10): # Loop para criar 10 lojas
        threading.Thread(target=connect_to_server, args=(new_id,)).start()

