from chain_store import *
import threading


class Query(threading.Thread):
    def __init__(self):
        super().__init__()
        self.querys = []
        self.balance = [0, 0] # [Vendas, Compras]
        self.semaphore = threading.Semaphore(1)

    def run(self):
        while True:
            with self.semaphore:
                if self.querys:
                    print('\n\nMovimentações: ')
                    for msg in self.querys:
                        print(msg)

                    balance = self.balance[0] - self.balance[1]

                    # Se o balanço geral for maior ou igual a 0, saldo fica verde, caso contrário, vermelho
                    if balance >= 0:
                        balance_code = '\033[32m'
                    else:
                        balance_code = '\033[31m'

                    print(f'\nCompras: R$ {self.balance[1]}     Vendas: R$ {self.balance[0]}     Saldo: {balance_code}R$ {self.balance[0] - self.balance[1]}\033[0m')
                    self.querys.clear()
            time.sleep(2)

    def update_balance(self, store_id, product_id, units, movement_type):
        with self.semaphore:
            if movement_type == 'COMPRA':
                # Calculando preço para uma compra do fornecedor
                price = products[int(product_id)]['price'] * int(units)
                self.balance[1] += price

                self.querys.append(f'Compra realizada na loja {store_id}. {units} unidade(s) do produto {products[int(product_id)]["name"]}: \033[31mR$ {price}\033[0m')
            elif movement_type == 'VENDA':
                # Calculando preço com margem de 50%
                price = (products[int(product_id)]['price'] * int(units)) * 1.5
                self.balance[0] += price

                self.querys.append(f'Venda realizada na loja {store_id}. {units} unidade(s) do produto {products[int(product_id)]["name"]}: \033[32mR$ {price}\033[0m')

