import threading
from bank import *


class Account:
    def __init__(self, number: int, balance: int, password: str):
        super().__init__()
        self.number = number # Número da conta
        self.balance = balance # Saldo inicial da conta
        self.account = threading.Condition() # Cria uma condição de threading para sincronização
        self.password = password # Senha da conta

    def deposit(self, amount, transferencia=False):
        with self.account: # Bloqueia a condição para operações enquanto a thread está em execução
            self.balance += amount # Adiciona o valor ao saldo
            if not transferencia:
                response = (f'Depósito de R$ {amount} realizado com sucesso na conta {self.number}. '
                            f'Saldo atual: R$ {self.balance}')
            else:
                response = f'Conta {self.number} recebeu transferência de R$ {amount}. Saldo atual: R$ {self.balance}'
            self.account.notify() # Notifica as threads aguardando nesta condição

        return response

    def withdraw(self, amount):
        with self.account: # Bloqueia a condição para operações enquanto a thread está em execução
            if self.balance >= amount:
                self.balance -= amount # Subtrai o valor do saldo
                response = (f'Saque de R$ {amount} realizado com sucesso na conta {self.number}. '
                            f'Saldo atual: R$ {self.balance}')
            else:
                response = (f'Saldo insuficiente para saque de R$ {amount} na conta {self.number}. '
                            f'Saldo atual: R$ {self.balance}')

            self.account.notify() # Notifica as threads aguardando nesta condição

        return response

    def transfer(self, amount, destination_account):
        with self.account: # Bloqueia a condição para operações enquanto a thread está em execução
            if self.balance >= amount:
                self.balance -= amount # Subtrai o valor do saldo
                destination_account.deposit(amount, True) # Deposita o valor na conta de destino
                response = (f'Transferência de R$ {amount} realizada com sucesso na conta {self.number} '
                            f'para a conta {destination_account.number}. Saldo atual: R$ {self.balance}')
            else:
                response = (f'Saldo insuficiente para transferência de R$ {amount} na conta {self.number} '
                            f'para a conta {destination_account.number}. Saldo atual: R$ {self.balance}')

            self.account.notify() # Notifica as threads aguardando nesta condição

        return response

    def get_balance(self):
        with self.account: # Bloqueia a condição para operações enquanto a thread está em execução
            response = f'Saldo da conta {self.number}: R$ {self.balance}'
            self.account.notify() # Notifica as threads aguardando nesta condição

        if response:
            return response
