import random
import time
from chain_store import socket, HOST, PORT, threading


def generate_random_sale(store_id):
    return f"VENDA {store_id} {random.randint(1, 96)} {random.randint(1, 100)}"


def generate_random_purchase(store_id):
    return f"COMPRA {store_id} {random.randint(1, 96)} {random.randint(40, 500)}"


def connect_to_server(store_id):
    operations = 0
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        print(f"Conectado ao servidor {HOST}:{PORT}")
        while operations < 1500:

            # Recebe comando do usuário
            msg = random.choice([generate_random_sale(store_id), generate_random_sale(store_id), generate_random_sale(store_id), generate_random_sale(store_id), generate_random_sale(store_id), generate_random_purchase(store_id)])
            # Envia o comando ao servidor
            s.sendall(msg.encode())

            operations += 1
            time.sleep(random.uniform(0, 3))

            # Recebe a resposta do servidor
            response = s.recv(1024)
            response = response.decode()

            print(f"Resposta do servidor: {response}")


def run():
    for new_id in range(10):
        threading.Thread(target=connect_to_server, args=(new_id,)).start()