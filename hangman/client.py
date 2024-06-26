import socket
from hangman import *


def connect_to_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: # Cria um objeto de socket para comunicação TCP.
        s.connect((HOST, PORT)) # Conecta ao servidor usando o endereço HOST e a porta PORT.
        response = s.recv(1024) # Recebe a resposta inicial do servidor (até 1024 bytes) e imprime no console.
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
