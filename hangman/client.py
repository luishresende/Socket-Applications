import socket
from hangman import *


def connect_to_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        response = s.recv(1024)
        print(f"Resposta do servidor: \n{response.decode()}")
        while True:
            # Recebe comando do usuário
            msg = input("Digite a letra desejada: ")

            # Envia o comando ao servidor
            s.sendall(msg.encode())

            if msg == 'exit':
                print("Desconectando...")
                break

            # Recebe a resposta do servidor
            response = s.recv(1024)
            response = response.decode()

            print(f"Resposta do servidor: {response}")

            # Verificando se o jogo acabou atrvés da primeira linha da mensagem
            if response.split('\n')[0][:27] in ['Parabéns! Você ganhou!', 'Você perdeu! A palavra era:']:
                break


def run():
    connect_to_server()
