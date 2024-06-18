from operations import *
import socket


def sum(numbers):
    result = 0
    for num in numbers:
        result += num
    return result


def mult(numbers):
    result = 1
    for num in numbers:
        result *= num
    return result


def mean(numbers):
    return sum(numbers) / len(numbers)


def median(numbers):
    numbers.sort()
    n = len(numbers)
    if n % 2 == 0:
        return (numbers[n // 2 - 1] + numbers[n // 2]) / 2
    else:
        return numbers[n // 2]


def operations_commands(data):
    args = data.strip().split()
    print(args)
    if len(args) < 3:
        return 'Número insuficiente de argumentos'

    operation = args[0]

    # Verificando se é uma operação que está dentro das permitidas
    if operation not in ['SUM', 'MULT', 'MEAN', 'MEDIAN']:
        return 'Operação inválida'

    nums = args[:len(args) - 1] # Criando uma lista apenas com os números
    for i, num in enumerate(nums):
        try:
            nums[i] = int(args[i])
        except ValueError:
            return f'Argumento inválido na posição {i + 1}. Espera-se um valor inteiro.'

    if operation == 'SUM':
        return f'Resultado da soma: {sum(nums)}'
    elif operation == 'MULT':
        return f'Resultado da multiplicação: {mult(nums)}'
    elif operation == 'MEAN':
        return f'Resultado da média: {mean(nums)}'
    elif operation == 'MEDIAN':
        return f'Resultado da mediana: {median(nums)}'


def handle_client(conn, addr):
    with conn:
        print(f"Novo usuário: {addr}")
        while True:
            msg = conn.recv(8192)
            if not msg:
                break
            data = msg.decode('utf-8')

            # Processo a resposta para o usuário
            response = operations_commands(data)

            # Enviando resposta ao usuário
            conn.sendall(str(response).encode('utf-8'))
            break


def run():
    # Inicializa o servidor
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((HOST, PORT))
        server.listen(1) # Uma conexão por vez
        print(f"Servidor escutando em {HOST}:{PORT}")

        # Aceitando conexões de clientes
        while True:
            conn, addr = server.accept()
            if conn:
                handle_client(conn, addr)


