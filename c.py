import socket
import threading
def read_sok():
     while 1 :
         data = sor.recv(1024)
         print(data.decode('utf-8'))
server = '127.0.0.1', 80  # Данные сервера
 
a = ''
b = 0
alias = input("Enter your username:") # Вводим наш псевдоним
sor = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sor.bind(('', 0)) # Задаем сокет как клиент
sor.sendto((alias+' Connect to server').encode('utf-8'), server)# Уведомляем сервер о подключении
potok = threading.Thread(target= read_sok)
potok.start()
while 1 :
    try:
        mensahe = input("Message:")
        if mensahe == '0-1':
            sor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            break
        sor.sendto(('['+alias+']'+mensahe).encode('utf-8'), server)
    except:
        sor.close()
