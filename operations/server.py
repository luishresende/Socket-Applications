from operations import *
import socket

# Função para calcular a soma dos números na lista
def sum(numbers):
    result = 0
    for num in numbers:
        result += num
    return result

# Função para calcular a multiplicação dos números na lista
def mult(numbers):
    result = 1
    for num in numbers:
        result *= num
    return result

# Função para calcular a média dos números na lista
def mean(numbers):
    return sum(numbers) / len(numbers)

# Função para calcular a mediana dos números na lista
def median(numbers):
    numbers.sort()
    n = len(numbers)
    if n % 2 == 0:
        return (numbers[n // 2 - 1] + numbers[n // 2]) / 2
    else:
        return numbers[n // 2]

# Função para processar os comandos recebidos do cliente
def operations_commands(data):

    args = data.strip().split() # Divide a entrada do cliente em argumentos
    print(args)

    if len(args) < 3:
        return 'Número insuficiente de argumentos'

    operation = args[0] # Primeiro argumento é a operação

    # Verificando se é uma operação que está dentro das permitidas
    if operation not in ['SUM', 'MULT', 'MEAN', 'MEDIAN']:
        return 'Operação inválida'

    nums = args[1:] # Criando uma lista apenas com os números

    for i, num in enumerate(nums):
        try:

            nums[i] = int(args[i]) # Converte os números para inteiros

        except ValueError:
            return f'Argumento inválido na posição {i + 1}. Espera-se um valor inteiro.'

    # Chama a função apropriada com os números fornecidos
    if operation == 'SUM':
        return f'Resultado da soma: {sum(nums)}'
    elif operation == 'MULT':
        return f'Resultado da multiplicação: {mult(nums)}'
    elif operation == 'MEAN':
        return f'Resultado da média: {mean(nums)}'
    elif operation == 'MEDIAN':
        return f'Resultado da mediana: {median(nums)}'


# Função para lidar com cada cliente que se conecta ao servidor
def handle_client(conn, addr):
    with conn:
        print(f"Novo usuário: {addr}")
        while True:
            msg = conn.recv(8192) # Recebe mensagem do cliente (até 8192 bytes)
            if not msg:
                break
            data = msg.decode('utf-8') # Decodifica a mensagem

            # Processa a mensagem do cliente e obtém a resposta
            response = operations_commands(data)

            # Envia a resposta de volta ao cliente
            conn.sendall(str(response).encode('utf-8'))
            break

# Função principal que inicializa o servidor
def run():
    # Inicializa o servidor
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((HOST, PORT)) # Liga o servidor ao endereço HOST e PORT
        server.listen(1) # Aceita uma conexão por vez
        print(f"Servidor escutando em {HOST}:{PORT}")

        # Aceitando conexões de clientes
        while True:
            conn, addr = server.accept() # Aceita uma conexão do cliente
            if conn:
                handle_client(conn, addr) # Inicia uma thread para lidar com o cliente


