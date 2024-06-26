import random
import shlex
from fortune import *
import socket


def parse_message(msg):
    # shlex.split para dividir a mensagem em argumentos
    args = shlex.split(msg)
    return args


def get_fortune():
    # Retorna uma frase aleatória do banco de dados
    with DATABASE:
        message_id = random.randint(0, len(data) - 1)
        return data[message_id]


def add_fortune(fortune):
    # Adicionando a frase ao banco de dados
    with DATABASE:
        with open(file_path, 'w') as db:
            data.append(fortune)
            db.write('\n'.join(data))
    return f'Fortune adicionado com sucesso: <{fortune}>'


def update_fortune(pos, fortune):
    with DATABASE:
        # Se a posição for igual a -1, a posição assume o valor da última frase
        if pos == -1:
            pos = len(data) - 1

        # Se a posição estiver fora do intervalo, retorna uma mensagem de erro
        elif pos < 1 or pos > len(data):
            return f'Posição inválida: {pos}'

        # Se nenhum erro é econtrado, a posição é ajustada para o índice da lista
        else:
            pos -= 1

        # Atualizando a frase no banco de dados
        data[pos] = fortune
        with open(file_path, 'w') as db:
            db.write('\n'.join(data))
    return f'Fortune atualizado com sucesso na posição {pos + 1}: <{fortune}>'


def list_fortunes():
    # Retorna todas as frases do banco de dados
    with DATABASE:
        return '\n'.join(data)


def fortune_commands(msg):
    # Parseando a mensagem
    args = parse_message(msg)
    if len(args) > 0:
        # O primeiro argumento é o comando
        command = args[0]
    else:
        return 'Comando inválido'

    if command == 'GET-FORTUNE':
        if len(args) > 1:
            return 'O comando "GET-FORTUNE" não aceita argumentos'
        return get_fortune()

    elif command == 'ADD-FORTUNE':
        # Verifica se há um segundo argumento
        if len(args) < 2:
            return 'É esperado um segundo argumento para a função "ADD-FORTUNE"'

        # Verifica se há mais de um argumento
        elif len(args) > 2:
            return ('A função "ADD-FORTUNE" aceita apenas um argumento, que deve ser uma frase entre aspas simples ou '
                    'duplas')
        else:
            return add_fortune(args[1])

    elif command == 'UPD-FORTUNE':
        # Verifica se há mais de 3 argumentos
        if len(args) > 3:
            return ('A função "UPD-FORTUNE" aceita apenas dois argumentos, o primeiro é a posição da frase a ser '
                    'atualizada e o segundo é a nova frase')

        # Verifica se o segundo argumento é um número
        elif not args[1].isnumeric() and args[1] != '-1':
            return 'A posição da frase a ser atualizada deve ser um número inteiro'

        else:
            return update_fortune(int(args[1]), args[2])

    elif command == 'LST-FORTUNE':
        # Verifica se há mais de um argumento
        if len(args) > 1:
            return 'O comando "LST-FORTUNE" não aceita argumentos'
        return list_fortunes()

    elif command == 'exit':
        return None
    else:
        return f'Comando inválido: {msg}'


def handle_client(conn, addr):
    print(f"Novo usuário: {addr}")
    with conn:
        while True:
            # Recebe a mensagem do cliente
            msg = conn.recv(8192)
            if not msg:
                print(f"Cliente desconectado {addr}")
                break
            # Processa a mensagem e envia a resposta
            response = fortune_commands(msg.decode())

            if response:
                conn.sendall(response.encode())
            else:
                break


def run():
    # Inicializa o servidor
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Servidor escutando em {HOST}:{PORT}")

        # Aceitando conexões de clientes
        while True:
            conn, addr = s.accept()

            # Cria uma nova thread para lidar com o cliente
            client_thread = threading.Thread(target=handle_client, args=(conn, addr))
            client_thread.start()


