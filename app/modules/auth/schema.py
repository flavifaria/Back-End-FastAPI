#Caixa Eletrônico

#VARIÁVEIS E TIPOS PRIMITIVOS
nome_usuario = "Flávio" #String
saldo = 1000.0 #float
programa_ativo = True #boolean

print("BEM-VINDO AO BANCO PYTHON ",nome_usuario)


#ESTRUTURA DE REPETIÇÃO
while programa_ativo :
    print("-----MENU-----")
    print("1.Verificar Saldo")
    print("2.Depositar")
    print("3.Sacar")
    print("4.SAIR")
    
    opcao = input("Escolha uma opção:")
    
    #IF/ELIF/ELSE
    if opcao == '1':
        print("Seu saldo atual é :" , saldo)
    elif opcao == '2':
        valor_deposito = float(input("Qual valor deseja depositar : "))
        saldo = valor_deposito + saldo
        print("Deposito realizado com sucesso!")
    