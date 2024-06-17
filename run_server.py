from fortune import server as fortune_server
from operations import server as operations_server
from hangman import server as hangman_server
from bank import server as bank_server
from chain_store import server as chain_store_server


print('Servidores: \n1 - Fortune\n2 - Operations\n3 - Jogo da Forca\n4 - Banco\n5 - Rede de Lojas\n')
server = input('Selecione o servidor: ')
while server not in ['1', '2', '3', '4', '5']:
    print('Servidor inválido')
    server = input('Selecione o servidor: ')

if server == '1':
    fortune_server.run()
elif server == '2':
    operations_server.run()
elif server == '3':
    hangman_server.run()
elif server == '4':
    bank_server.run()
elif server == '5':
    chain_store_server.run()
