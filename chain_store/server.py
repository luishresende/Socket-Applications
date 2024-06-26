import shlex
from chain_store import *


def parse_message(msg):
    # shlex.split para dividir a mensagem em argumentos
    args = shlex.split(msg) # Ex: 'VENDA 1 10' -> ['VENDA', '1', '10']
    return args


def chain_commands(msg):
    # Parseando a mensagem
    args = parse_message(msg)
    if len(args) > 0:
        # O primeiro argumento é o comando
        command = args[0]
    else:
        return 'Comando inválido' # Se não houver argumentos, retorna uma mensagem de erro


    if command == 'VENDA': # Se o comando for 'VENDA'
        if len(args) != 4: # Se o número de argumentos for diferente de 4
            return 'O comando "VENDA" espera quatro argumentos. Ex: "VENDA <id_produto> <quantidade>"'
        threading.Thread(target=query.update_balance, args=(args[1], args[2], args[3], 'VENDA')).start() # Inicia uma nova thread para atualizar o balanço
        return 'Registro encaminhado' # Retorna uma mensagem de confirmação

    elif command == 'COMPRA': # Se o comando for 'COMPRA'
        if len(args) != 4: # Se o número de argumentos for diferente de 4
            return 'O comando "COMPRA" espera quatro argumentos. Ex: "COMPRA <id_produto> <quantidade>"'
        threading.Thread(target=query.update_balance, args=(args[1], args[2], args[3], 'COMPRA')).start() # Inicia uma nova thread para atualizar o balanço
        return 'Registro encaminhado' # Retorna uma mensagem de confirmação


    else:
        return 'Comando inexistente.' # Se o comando não for 'VENDA' ou 'COMPRA', retorna uma mensagem de erro


def handle_client(conn, addr): # Função para lidar com o cliente
    print(f"Novo usuário: {addr}")  # Exibe o endereço do cliente

    with conn:
        # Loop para interação com o cliente
        while True:
            # Recebe a mensagem do cliente
            msg = conn.recv(8192)
            if not msg: # Se não houver mensagem,
                break

            response = chain_commands(msg.decode()) # Executa o comando e armazena a resposta

            if response: # Se houver resposta,
                conn.sendall(response.encode()) # Envia a resposta ao cliente
            else:
                break # Se não houver resposta, encerra a conexão


def run():
    query.start() # Inicia a thread para exibir as movimentações
    # Inicializa o servidor
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: # Cria um socket
        s.bind((HOST, PORT)) # Associa o socket ao endereço e porta
        s.listen() # Habilita o servidor para aceitar conexões
        print(f"Servidor escutando em {HOST}:{PORT}")   # Exibe o endereço e porta do servidor

        # Aceitando conexões de clientes
        while True: # Loop para aceitar conexões
            conn, addr = s.accept() # Aceita a conexão

            # Cria uma nova thread para lidar com o cliente
            client_thread = threading.Thread(target=handle_client, args=(conn, addr)) # Cria uma nova thread
            client_thread.start() # Inicia a thread
