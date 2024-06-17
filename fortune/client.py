import socket
from fortune import *


def connect_to_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        print(f"Conectado ao servidor {HOST}:{PORT}")
        print('Comandos disponíveis:\n'
              '- GET-FORTUNE\n'
              '- ADD-FORTUNE <new fortune>\n'
              '- UPD-FORTUNE <pos> <new fortune>\n'
              '- LST-FORTUNE\n'
              '- exit\n')
        while True:
            # Recebe comando do usuário
            msg = input("Digite o comando: ")

            # Envia o comando ao servidor
            s.sendall(msg.encode())

            if msg == 'exit':
                print("Desconectando...")
                break

            # Recebe a resposta do servidor
            response = s.recv(8192)
            print(f"Resposta do servidor: {response.decode()}")


def run():
    connect_to_server()
