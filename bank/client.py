from bank import *


def connect_to_server():
    # Cria um socket TCP/IP
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT)) # Conecta ao servidor usando HOST e PORT
        print(f"Conectado ao servidor {HOST}:{PORT}")

        response = s.recv(1024) # Recebe a resposta inicial do servidor
        print(f"Resposta do servidor: \n{response.decode()}") # Exibe a resposta decodificada
        while True:
            # Recebe comando do usuário
            msg = input("Digite o comando: ")

            # Envia o comando ao servidor
            s.sendall(msg.encode())

            if msg == 'exit': # Se o usuário digitar 'exit', encerra a conexão
                print("Desconectando...")
                break

            # Recebe a resposta do servidor
            response = s.recv(8192)
            print(f"Resposta do servidor: {response.decode()}")


def run(): # inicia a conexão com o servidor
    connect_to_server() # Chama a função para conectar ao servidor
