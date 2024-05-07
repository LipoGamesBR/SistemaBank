import os


extrato = ""

opc = ""
limite = 500
saldo = 500
credito = 600
saques = 0
LIMITE_SAQUES = 3

menu = """
    Bem-vindo ao seu banco
    [a] - Extrato
    [b] - Saque
    [c] - Deposito
    [d] - Empréstimo
    [e] - Sair

    
    Selecione uma opção.
 =>"""


menu_credito = f"""Você tem R${credito:.2f} de limite para empréstimo disponível.
    
    [a] - Contratar empréstimo
    [b] - Cancelar operação

            
Selecione uma opção.
=>"""

os.system('clear') or None

while(opc != "e" and opc != "E"):
    print(menu)
    opc = str(input())

    os.system('clear') or None
    
    if(opc == "a" or opc == "A"):
        print("\n================ EXTRATO ================")
        print("Não foram realizadas movimentações." if not extrato else extrato)
        print(f"\nSaldo: R$ {saldo:.2f}")
        print("==========================================")


    elif(opc == "b" or opc == "B"):
        os.system('clear') or None
        print("Digite o valor que deseja sacar: ")
        valor = int(input())
        os.system('clear') or None
        if(valor > limite):
            print("Falha ao efetuar o saque, valor solicitado maior que o seu limite.")
        elif(valor > saldo):
            print("Falha ao efetuar o saque, valor solicitado maior que o saldo disponível.")
        elif(LIMITE_SAQUES <= saques):
            print("Você atingiu seu limite de saques.")
        else:
            saldo -= valor
            extrato += f"Saque: R$ {valor:.2f}\n"
            print(f"Saque de R${valor:.2f} realizado com sucesso.")
            saques += 1


    elif(opc == "c" or opc=="C"):
        print("Digite o valor do seu depósito: ")
        valor = int(input())
        saldo += valor
        extrato += f"Depósito: R$ {valor:.2f}\n"



    elif(opc == "d" or opc == "D"):
        if(credito == 0): print("Você não tem limite de crédito disponível.")
        else:
            print(menu_credito)
            opc = input()
            while(opc != "b" and opc != "B"):
                if(opc == "a" or opc =="A"):
                    print("Digite o valor que deseja contratar: ")
                    valor = int(input())

                    if(valor > credito): print("Valor maior do que o crédito disponível.")
                    saldo += valor 
                    credito -= valor
                    extrato += f"Empréstimo: R${valor:.2f}\n"
                    opc="b"
                else:
                    print("Respota inválida.")




    elif(opc == "e" or opc == "E"):
        print("Obrigado pela preferência.")
        False
    else:
        print("Você precisa escolher uma das opções")
    