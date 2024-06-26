import random
import shlex
from bank import *
import uuid


# Divide os argumentos da mensagem
def parse_message(msg):
    # Utiliza shlex.split para dividir a mensagem em argumentos, preservando os espaços entre aspas
    args = shlex.split(msg)
    return args


# Retorna uma conta pelo seu número
def get_account(requested_account_number):
    for acc in accounts: # Itera sobre a lista de contas
        if acc.number == requested_account_number: # Verifica se o número da conta corresponde ao solicitado
            return acc
    return None # Retorna None se não encontrar a conta


def bank_commands(session_id, msg): # Função que processa os comandos do banco
    # Parseia a mensagem em argumentos
    args = parse_message(msg)
    if len(args) > 0:
        # O primeiro argumento é o comando
        command = args[0]
    else:
        return 'Comando inválido'

    # Validação dos comandos
    if command == 'SALDO':
        if len(args) != 1:
            return 'O comando "SALDO" não espera argumentos.'

        print(clients[session_id])
        # Retorna o saldo da conta associada ao session_id

        main
        return clients[session_id]['account'].get_balance()

    elif command == 'SAQUE':
        if len(args) != 2:
            return 'O comando "SAQUE" espera um argumento. Ex: "SAQUE <valor>"'
        try:
            amount = float(args[1]) # Converte o argumento para float
        except TypeError as e:
            return 'O argumento para o comando deve ser um valor numérico.'

        if amount < 0:
            return 'Não é possível realizar o saque de um valor negativo.'

        return clients[session_id]['account'].withdraw(amount) # Realiza o saque

    elif command == 'DEPOSITO':
        if len(args) != 2:
            return 'O comando "DEPOSITO" espera um argumento. Ex: "DEPOSITO <valor>"'
        try:
            amount = float(args[1]) # Converte o argumento para float
        except TypeError as e:
            return 'O argumento 1 para o comando deve ser um valor numérico.'

        if amount < 0:
            return 'Não é possível realizar o depósito de um valor negativo.'

        return clients[session_id]['account'].deposit(amount) # Realiza o depósito

    elif command == 'TRANSFERENCIA':
        if len(args) != 3:
            return 'O comando "TRANSFERENCIA" espera dois argumentos. Ex: "TRANSFERENCIA <valor> <número da conta>"'
        try:
            amount = float(args[1]) # Converte o primeiro argumento para float
        except TypeError as e:
            return ('O argumento 1 para o comando "TRANSFERENCIA" deve ser um valor numérico, representando a '
                    'quantidade desejada para a transferencia.')

        try:
            requested_account_number = int(args[2]) # Converte o segundo argumento para int
        except TypeError as e:
            return ('O argumento 2 para o comando "TRANSFERENCIA" deve ser um valor inteiro, representando o número de '
                    'uma conta.')

        if amount < 0:
            return 'Não é possível realizar a transferência de um valor negativo.'

        destination_account = get_account(requested_account_number) # Obtém a conta de destino

        if not destination_account:
            return 'Conta destino não encontrada!'


        return clients[session_id]['account'].transfer(amount, destination_account) # Realiza a transferência

        if destination_account == clients[session_id]['account']:
            return 'Não é possível realizar transferência para a mesma conta.'




    else:
        return 'Comando inexistente.'


def login(session_id, msg): # Função que processa os comandos de login
    # Parseia a mensagem em argumentos
    args = parse_message(msg)
    if len(args) > 0:
        # O primeiro argumento é o comando
        command = args[0]
    else:
        return 'Comando inválido'

    if command == 'LOGIN':
        if len(args) != 3:
            return 'O comando "LOGIN" deve ter 3 argumentos: LOGIN <número da conta> <senha>'
        account_number = int(args[1]) # Converte o segundo argumento para int
        password = args[2] # Terceiro argumento é a senha
        acc = get_account(account_number) # Obtém a conta pelo número
        if acc:
            if acc.password == password:  # Verifica a senha
                clients[session_id]['account'] = acc # Associa a conta ao session_id
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
    session_id = str(uuid.uuid4()) # Gera ID único aleatório para a sessão
    clients[session_id] = {
        'addr': addr,
        'session': session_id,
        'account': None
    }

    with conn: # Cliente solicita conexão com o servidor e recebe uma mensagem de boas-vindas
        start_message = ('Bem-vindo ao banco!\n'
                         'Para realizar o login em sua conta, utilize o seguinte comando:\n'
                         'LOGIN <número da conta> <senha>\n\n')
        conn.sendall(start_message.encode()) # Envia a mensagem inicial para o cliente

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
                conn.sendall(response.encode()) # Envia a resposta para o cliente
            else:
                break


def run(): # Função que inicializa o servidor
    # Inicializa o servidor
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Servidor escutando em {HOST}:{PORT}")

        # Aceitando conexões de clientes
        while True:
            conn, addr = s.accept() # Aceita uma nova conexão de cliente

            # Cria uma nova thread para lidar com o cliente
            client_thread = threading.Thread(target=handle_client, args=(conn, addr))
            client_thread.start() # Inicia a thread

