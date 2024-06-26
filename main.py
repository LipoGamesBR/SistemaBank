from datetime import datetime


class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf


class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    def saldo(self):
        return self._saldo

    def numero(self):
        return self._numero

    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    def historico(self):
        return self._historico

    def sacar(self, valor):
        saldo = self.saldo()
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")

        elif valor > 0:
            self._saldo -= valor
            print("\n=== Saque realizado com sucesso! ===")
            return True

        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

        return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("\n=== Depósito realizado com sucesso! ===")
        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
            return False

        return True


class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico().transacoes if transacao["tipo"] == Saque.__name__]
        )

        excedeu_limite = valor > self.limite
        excedeu_saques = numero_saques >= self.limite_saques

        if excedeu_limite:
            print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")

        elif excedeu_saques:
            print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")

        else:
            return super().sacar(valor)

        return False

    def __str__(self):
        return f"""\
            Agência:\t{self.agencia()}
            C/C:\t\t{self.numero()}
            Titular:\t{self.cliente.nome}
        """


class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor(),
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%s"),
            }
        )


class Transacao:
    def valor(self):
        pass

    def registrar(self, conta):
        pass


class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor())

        if sucesso_transacao:
            conta.historico().adicionar_transacao(self)


class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor())

        if sucesso_transacao:
            conta.historico().adicionar_transacao(self)


def menu():
    print("\n### Menu ###")
    print("1. Criar conta")
    print("2. Realizar saque")
    print("3. Realizar depósito")
    print("4. Visualizar saldo")
    print("5. Sair")


def main():
    cliente_nome = input("Digite o nome do cliente: ")
    cliente_data_nascimento = input("Digite a data de nascimento do cliente (DD-MM-AAAA): ")
    cliente_cpf = input("Digite o CPF do cliente: ")
    cliente_endereco = input("Digite o endereço do cliente: ")
    
    cliente = PessoaFisica(cliente_nome, cliente_data_nascimento, cliente_cpf, cliente_endereco)
    conta = None

    while True:
        menu()
        escolha = input("Escolha uma opção: ")

        if escolha == "1":
            numero_conta = input("Digite o número da conta: ")
            conta = ContaCorrente.nova_conta(ContaCorrente, cliente, numero_conta)
            print("\nConta criada com sucesso!")
        elif escolha == "2":
            if conta is not None:
                valor_saque = float(input("Digite o valor do saque: "))
                transacao = Saque(valor_saque)
                conta.cliente.realizar_transacao(conta, transacao)
            else:
                print("\n@@@ Operação falhou! Crie uma conta antes de realizar um saque. @@@")
        elif escolha == "3":
            if conta is not None:
                valor_deposito = float(input("Digite o valor do depósito: "))
                transacao = Deposito(valor_deposito)
                conta.cliente.realizar_transacao(conta, transacao)
            else:
                print("\n@@@ Operação falhou! Crie uma conta antes de realizar um depósito. @@@")
        elif escolha == "4":
            if conta is not None:
                print(f"\nSaldo atual: R$ {conta.cliente.saldo():.2f}")
            else:
                print("\n@@@ Operação falhou! Crie uma conta antes de visualizar o saldo. @@@")
        elif escolha == "5":
            print("\nSaindo...")
            break
        else:
            print("\nOpção inválida! Por favor, escolha uma opção válida.")

main()
