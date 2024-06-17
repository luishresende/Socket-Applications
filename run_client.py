from fortune import client as fortune_client
from operations import client as operations_client
from hangman import client as hangman_client
from bank import client as bank_client
from chain_store import client as chain_store_client


print('Clientes: \n1 - Fortune\n2 - Operations\n3 - Jogo da Forca\n4 - Banco\n5 - Rede de Lojas\n')
client = input('Selecione o cliente: ')
while client not in ['1', '2', '3', '4', '5']:
    print('Cliente inválido')
    client = input('Selecione o cliente: ')

if client == '1':
    fortune_client.run()
elif client == '2':
    operations_client.run()
elif client == '3':
    hangman_client.run()
elif client == '4':
    bank_client.run()
elif client == '5':
    chain_store_client.run()
