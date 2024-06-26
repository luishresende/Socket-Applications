import shlex
from chain_store import *


def parse_message(msg):
    # shlex.split para dividir a mensagem em argumentos
    args = shlex.split(msg)
    return args


def chain_commands(msg):
    # Parseando a mensagem
    args = parse_message(msg)
    if len(args) > 0:
        # O primeiro argumento é o comando
        command = args[0]
    else:
        return 'Comando inválido'

    if command == 'VENDA':
        if len(args) != 4:
            return 'O comando "VENDA" espera quatro argumentos. Ex: "VENDA <id_loja> <id_produto> <quantidade>"'
        threading.Thread(target=query.update_balance, args=(args[1], args[2], args[3], 'VENDA')).start()
        return 'Registro encaminhado'

    elif command == 'COMPRA':
        if len(args) != 4:
            return 'O comando "COMRA" espera quatro argumentos. Ex: "COMPRA <id_loja> <id_produto> <quantidade>"'
        threading.Thread(target=query.update_balance, args=(args[1], args[2], args[3], 'COMPRA')).start()
        return 'Registro encaminhado'

    else:
        return 'Comando inexistente.'


def handle_client(conn, addr):
    print(f"Novo usuário: {addr}")

    with conn:
        # Loop para interação com o cliente
        while True:
            # Recebe a mensagem do cliente
            msg = conn.recv(8192)
            if not msg:
                break

            response = chain_commands(msg.decode())

            if response:
                conn.sendall(response.encode())
            else:
                break


def run():
    query.start()
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
