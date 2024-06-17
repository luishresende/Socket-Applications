import threading
from bank import *


class Account:
    def __init__(self, number: int, balance: int, password: str):
        super().__init__()
        self.number = number
        self.balance = balance
        self.account = threading.Condition()
        self.password = password

    def deposit(self, amount, transferencia=False):
        with self.account:
            self.balance += amount
            if not transferencia:
                response = (f'Depósito de R$ {amount} realizado com sucesso na conta {self.number}. '
                            f'Saldo atual: R$ {self.balance}')
            else:
                response = f'Conta 1 recebeu transferência de R$ {amount}. Saldo atual: R$ {self.balance}'
            self.account.notify()

        return response

    def withdraw(self, amount):
        with self.account:
            if self.balance >= amount:
                self.balance -= amount
                response = (f'Saque de R$ {amount} realizado com sucesso na conta {self.number}. '
                            f'Saldo atual: R$ {self.balance}')
            else:
                response = (f'Saldo insuficiente para saque de R$ {amount} na conta {self.number}. '
                            f'Saldo atual: R$ {self.balance}')

            self.account.notify()

        return response

    def transfer(self, amount, destination_account):
        with self.account:
            if self.balance >= amount:
                self.balance -= amount
                destination_account.deposit(amount, True)
                response = (f'Transferência de R$ {amount} realizada com sucesso na conta {self.number} '
                            f'para a conta {destination_account.number}. Saldo atual: R$ {self.balance}')
            else:
                response = (f'Saldo insuficiente para transferência de R$ {amount} na conta {self.number} '
                            f'para a conta {destination_account.number}. Saldo atual: R$ {self.balance}')

            self.account.notify()

        return response

    def get_balance(self):
        with self.account:
            response = f'Saldo da conta {self.number}: R$ {self.balance}'
            self.account.notify()

        if response:
            return response
