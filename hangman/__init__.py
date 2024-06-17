import os
import random

# Obtém o caminho do diretório onde este script está localizado
script_dir = os.path.dirname(__file__)
file_words_path = os.path.join(script_dir, 'words.txt')
words = []

# Lendo frases do banco de dados (arquivo txt)
with open(file_words_path, 'r') as arq:
    data = arq.read().split('\n')
    if data[-1] == '':
        data.pop()

    for line in data:
        line_data = line.split()
        word = line_data[0]
        tip = line_data[-1]
        words.append({
            'content': word,
            'tip': tip
        })

# Obtendo o desenho de cada estágio do jogo
file_stages_path = os.path.join(script_dir, 'stages.txt')
with open(file_stages_path, 'r') as arq:
    stages = arq.read().split('STAGE\n')
    if stages[-1] == '':
        stages.pop()

    stages.reverse()


HOST = "127.0.0.1"  # Endereço do servidor
PORT = 40002  # Porta para escutar

