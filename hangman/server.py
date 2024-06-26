import socket
import threading
from unidecode import unidecode
import random
from hangman import *


# Retorna uma palavra do banco de dados
def get_word():
    return words[random.randint(0, len(words))] # # Seleciona uma palavra aleatória do banco de palavras


def process_word(player):
    # Salvando a palavra do jogo antes de processar a letra
    init = player['word_game']

    new_word_game = []
    for letter in player['word']['content']:
        # Verificando se a letra do usuário está na palavra
        if unidecode(letter).upper() in player['letters']: # Verifica se a letra (sem acento) está nas letras escolhidas
            # Se estiver, adiciono a letra na lista de letras do jogo
            new_word_game.append(letter.upper())
        else:
            # Caso contrário, adiciono um traço, indicando uma letra faltante
            new_word_game.append('_')

    # Com as letras e traços, monto a palavra do jogo adicionando um espaço entre os caracteres
    player['word_game'] = ' '.join(new_word_game)

    # Se a palavra selecionada pelo servidor, for igual aos caracteres da palavra do jogo unidos por um '', o usuário venceu
    if player['word']['content'].upper() == ''.join(new_word_game):
        win = True
    else:
        win = False

    # Se o jogador acertou uma letra, retorno True, caso contrário, False
    if init != player['word_game']:
        return True, win
    else:
        return False, win


# Constóri a mensagem do jogo
def build_game_state(server_msg, player):
    return (f'{server_msg}\n\n'
            f'Dica: {player["word"]["tip"]}\n\n'
            f'Letras já escolhidas: {", ".join(player["letters"])}\n\n'
            f'Vidas: {player["lifes"]}\n'
            f'{stages[player["lifes"]]}\n\n'
            f'Palavra: {player["word_game"]}\n')


def process_response(msg, player):
    # Verificando se possui mais do que uma letra na mensagem
    if len(msg) > 1 or not str(msg).isalpha():
        server_message = 'É esperado apenas uma letra na mensagem!'
        return build_game_state(server_message, player), False

    # Verificando se a letra que o usuário informou já não foi escolhida
    elif msg.upper() in player['letters']:
        server_message = 'Você já tentou esta letra!'
        return build_game_state(server_message, player), False

    # Caso seja uma entrada válida, adiciono a letra informada na lista de letras do jogador
    else:
        player['letters'].append(msg.upper())

    # Verificando se o usuário acertou a letra e se venceu
    got_a_letter, win = process_word(player)

    if win:
        server_message = 'Parabéns! Você ganhou!'
        return build_game_state(server_message, player), win
    else:
        # Se o usuário não acertou a letra, decremento uma vida
        if not got_a_letter:
            player['lifes'] -= 1

            # Se o jogador ainda possui vidas, informo que a letra não existe na palavra
            if player['lifes'] > 0:
                server_message = 'Essa letra não existe na palavra!'
                return build_game_state(server_message, player), win

            # Se o jogador não possui mais vidas, informo que ele perdeu
            else:
                server_message = 'Você perdeu! A palavra era: ' + player['word']['content']
                return build_game_state(server_message, player), win
        else:
            # Se o jogador acertou a letra, informo que ele acertou
            server_message = "Você encontrou uma letra existente na palavra!"
            return build_game_state(server_message, player), win


def handle_client(conn, addr):
    print(f'{conn}') # Imprime a conexão do cliente para controle
    word_player = get_word() # Obtém uma palavra do banco de palavras
    word_game = ('_ ' * len(word_player['content']))[:-1] # Obtendo a palavra do jogo com traços no lugar das letras
    player = {
        'addr': addr, # Endereço do cliente conectado
        'lifes': 7, # Número inicial de vidas
        'letters': [], # Lista de letras escolhidas pelo jogador
        'word': word_player, # Palavra selecionada para o jogo
        'word_game': word_game # Estado inicial da palavra do jogo com traços
    }
    with (conn):
        # Construindo a mensagem inicial e enviando para o usuário
        msg_start = build_game_state('BEM-VINDO AO JOGO DA FORCA!', player)
        conn.sendall(msg_start.encode())

        while True:
            # Recebe a mensagem do cliente
            msg = conn.recv(1024)
            if not msg:
                break

            # Processa a mensagem e envia a resposta
            response, win = process_response(msg.decode(), player)

            # Se o usuário ganhou, encerro o loop do usuário
            if win:
                conn.sendall(response.encode())
                break
            else:
                conn.sendall(response.encode())


def run():
    # Inicializa o servidor
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT)) # Associa o servidor ao endereço HOST e porta PORT
        s.listen() # Aguarda por conexões de clientes
        print(f"Servidor escutando em {HOST}:{PORT}")

        # Aceitando conexões de clientes
        while True:
            conn, addr = s.accept() # Aceita uma conexão

            # Cria uma nova thread para lidar com o cliente
            client_thread = threading.Thread(target=handle_client, args=(conn, addr))
            client_thread.start()
