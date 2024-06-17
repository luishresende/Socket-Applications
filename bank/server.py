import random
import shlex
from bank import *
import uuid


# Divide os argumentos da mensagem
def parse_message(msg):
    # shlex.split para dividir a mensagem em argumentos
    args = shlex.split(msg)
    return args


# Retorna uma conta pelo seu número
def get_account(requested_account_number):
    for acc in accounts:
        if acc.number == requested_account_number:
            return acc
    return None


def bank_commands(session_id, msg):
    # Parseando a mensagem
    args = parse_message(msg)
    if len(args) > 0:
        # O primeiro argumento é o comando
        command = args[0]
    else:
        return 'Comando inválido'

    # Validação
    if command == 'SALDO':
        if len(args) != 1:
            return 'O comando "SALDO" não espera argumentos.'
        print(clients[session_id])
        return clients[session_id]['account'].get_balance()

    elif command == 'SAQUE':
        if len(args) != 2:
            return 'O comando "SAQUE" espera um argumento. Ex: "SAQUE <valor>"'
        try:
            amount = float(args[1])
        except TypeError as e:
            return 'O argumento para o comando deve ser um valor numérico.'

        if amount < 0:
            return 'Não é possível realizar o saque de um valor negativo.'

        return clients[session_id]['account'].withdraw(amount)

    elif command == 'DEPOSITO':
        if len(args) != 2:
            return 'O comando "DEPOSITO" espera um argumento. Ex: "DEPOSITO <valor>"'
        try:
            amount = float(args[1])
        except TypeError as e:
            return 'O argumento 1 para o comando deve ser um valor numérico.'

        if amount < 0:
            return 'Não é possível realizar o depósito de um valor negativo.'

        return clients[session_id]['account'].deposit(amount)

    elif command == 'TRANSFERENCIA':
        if len(args) != 3:
            return 'O comando "TRANSFERENCIA" espera dois argumentos. Ex: "TRANSFERENCIA <valor> <número da conta>"'
        try:
            amount = float(args[1])
        except TypeError as e:
            return ('O argumento 1 para o comando "TRANSFERENCIA" deve ser um valor numérico, representando a '
                    'quantidade desejada para a transferencia.')

        try:
            requested_account_number = int(args[2])
        except TypeError as e:
            return ('O argumento 2 para o comando "TRANSFERENCIA" deve ser um valor inteiro, representando o número de '
                    'uma conta.')

        if amount < 0:
            return 'Não é possível realizar o depósito de um valor negativo.'

        destination_account = get_account(requested_account_number)

        if not destination_account:
            return 'Conta destino não encontrada!'

        return clients[session_id]['account'].transfer(amount, destination_account)

    else:
        return 'Comando inexistente.'


def login(session_id, msg):
    # Parseando a mensagem
    args = parse_message(msg)
    if len(args) > 0:
        # O primeiro argumento é o comando
        command = args[0]
    else:
        return 'Comando inválido'

    if command == 'LOGIN':
        if len(args) != 3:
            return 'O comando "LOGIN" deve ter 3 argumentos: LOGIN <número da conta> <senha>'
        account_number = int(args[1])
        password = args[2]
        acc = get_account(account_number)
        if acc:
            if acc.password == password:
                clients[session_id]['account'] = acc
                return (f'Login realizado com sucesso!\n\n'
                        f'Comandos disponíveis:\n'
                        f'- SALDO\n'
                        f'- SAQUE <valor>\n'
                        f'- DEPOSITO <valor>\n'
                        f'- TRANSFERENCIA <valor> <número da conta>\n')
            else:
                return 'Senha incorreta. Tente novamente.\n'
        else:
            return 'Conta não encontrada. Tente novamente.\n'
    else:
        return 'Comando inválido. Utilize o comando "LOGIN <número da conta> <senha>"\n'


def handle_client(conn, addr):
    print(f"Novo usuário: {addr}")
    session_id = str(uuid.uuid4())
    clients[session_id] = {
        'addr': addr,
        'session': session_id,
        'account': None
    }

    with conn:
        start_message = ('Bem-vindo ao banco!\n'
                         'Para realizar o login em sua conta, utilize o seguinte comando:\n'
                         'LOGIN <número da conta> <senha>\n\n')
        conn.sendall(start_message.encode())

        # Loop para login do cliente
        while True:
            # Recebe a mensagem do cliente
            msg = conn.recv(8192)
            if not msg:
                break

            if not clients[session_id]['account']:
                # Processa a mensagem e envia a resposta
                response = login(session_id, msg.decode())
            else:
                response = bank_commands(session_id, msg.decode())

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

