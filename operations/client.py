import socket
from operations import *


def connect_to_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Conecta com o servidor
        s.connect((HOST, PORT))
        print(f"Conectado ao servidor {HOST}:{PORT}")
        print('Envie uma lista de inteiros separadas por espaço, com a especificação da operação no final.\n'
              'Operações disponíveis:\n'
              '- SUM\n'
              '- MULT\n'
              '- MEAN\n'
              '- MEDIAN\n')
        # Recebe comando do usuário
        msg = input("Digite o comando: ")

        # Envia o comando ao servidor
        s.sendall(msg.encode())

        # Recebe a resposta do servidor
        response = s.recv(8192)
        print(f"Resposta do servidor: {response.decode()}")

        # Fecha a conexão
        s.close()


def run():
    connect_to_server()
