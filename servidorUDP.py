import socket
import sre_yield
import hashlib
import time
from threading import Thread


senha = '12345678'
senha_hash = hashlib.md5(senha.encode('utf-8')).hexdigest()




#-------------------Variaveis de Controle----------------------------------------------------------------
listaDeClientes = {}
listaDeTempoDosClientes = {}
listaDeExpressoes = []
#-----------------------Gera listas de expressoes - (1000)--------------------------------------------------
for x in range(1000):
	listaDeExpressoes.append(str(x).zfill(3) + "[0-9]{6}")
#---------------



def controleDeClientes():
    while True:
        time.sleep(3)
        for cliente in list(listaDeClientes):
            if listaDeTempoDosClientes != []:
                if time.time() - listaDeTempoDosClientes.get(cliente) > 30:
                    print(cliente[0],"Desconectou")
                    express = listaDeClientes.get(cliente)
                    print("Lista reinserida")
                    listaDeExpressoes.append(express)
                    listaDeClientes.pop(cliente)
                    listaDeTempoDosClientes.pop(cliente)
                


def broadCast():
    HOST = ''              # Endereco IP do Servidor
    PORT = 5003            # Porta que o Servidor esta escutando
    udpBroadcast = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udpBroadcast.setsockopt(socket.SOL_SOCKET,socket.SO_BROADCAST, 1)
    origBroadCast = (HOST, PORT)
    udpBroadcast.bind(origBroadCast)

    while True:
        msg, cliente = udpBroadcast.recvfrom(1024)
        udpBroadcast.sendto("shazan".encode('utf-8'), cliente)


def main():
    
    HOST = ''
    PORT = 5000
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    orig = (HOST, PORT)
    udp.bind(orig)

    while True:
        
        msg, cliente = udp.recvfrom(1024)
        if msg.decode('utf-8') != 'ok':
            print (cliente, msg.decode('utf-8'))
        
    
    
        if msg.decode('utf-8') == 'hash':
            udp.sendto (senha_hash.encode('utf-8'), cliente)

        if msg.decode('utf-8') == 'listaDeSenhas':
            expressao = listaDeExpressoes.pop()
            udp.sendto (expressao.encode('utf-8'), cliente)
            listaDeClientes.update({cliente[0]:expressao})
            listaDeTempoDosClientes.update({cliente[0]:time.time()})

        if msg.decode('utf-8') == 'ok':
            listaDeTempoDosClientes.update({cliente:time.time()})
  
        if msg.decode('utf-8') == 'achei':
            print('Achou!')
            udp.close()




print('Iniciando o Servidor:')
print('Hash da senha - ' + senha_hash)


TMain = Thread(target=main)
TMain.start()

TBroadcast = Thread(target=broadCast)
TBroadcast.start()

TControleDeClientes = Thread(target=controleDeClientes)
TControleDeClientes.start()





