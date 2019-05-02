import socket
import sre_yield
import hashlib



#Pegando o endereço do Servidor
udpBroadcast = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udpBroadcast.setsockopt(socket.SOL_SOCKET,socket.SO_BROADCAST, 1)
udpBroadcast.sendto("shazan".encode('utf-8'),('<broadcast>',5003))
msg, cliente = udpBroadcast.recvfrom(1024)

print(msg)

HOST = cliente[0]  # Endereco IP do Servidor
PORT = 5000            # Porta que o Servidor esta escutando
udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
dest = (HOST, PORT)

print('Endereco de IP do Servidor foi encontrado: ' + HOST)


senhas = []


while True:

    udp.sendto ('hash'.encode('utf-8'), dest)
    resposta, addr = udp.recvfrom(1024)
    senha = resposta.decode('utf-8')

    udp.sendto ('listaDeSenhas'.encode('utf-8'), dest)
    resposta, addr = udp.recvfrom(1024)
    expressao = resposta.decode('utf-8')

    print('Gerando listas de senhas......')
    senhas = list(sre_yield.AllStrings(expressao))
    cont = 0
    for key in senhas:
        cont = cont + 1
        print(key)
        keyhash = hashlib.md5(key.encode('utf-8')).hexdigest()
        if keyhash == senha:
            print('SENHAAAAAAAAAAAAAAAAAAAA - ' + key)
            udp.sendto ('achei'.encode('utf-8'), dest)
            break
        if cont == 100:
             udp.sendto ('ok'.encode('utf-8'), dest)
             cont = 0


    udp.sendto ('Erro'.encode('utf-8'), dest)


udp.close()
