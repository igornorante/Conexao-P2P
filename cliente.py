import socket 
import threading #Biblioteca para troca de mensagens
import sys #Biblioteca para encerrar o sistema
import time



host = '200.235.131.66' #Endereço IP do servidor central    
porta = 10000           #Porta para comunicação com o servidor central 

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Cria a comunicação do socket com importacao do modelo TCP 
s.connect((host, porta)) #Faz a conexão do socket cliente com o socket do servidor de IP e porta fornecidos pelo professor 

#Envio das informações do usuário para o servidor central

nome = input("Digite o seu nome: ")
nome=nome.strip()  
portadeacesso = input("Digite sua porta de acesso ao servidor: ")
msg_usuario =  "USER {}:{}\r\n".format(nome, portadeacesso)
s.send(msg_usuario.encode())
s.send(str.encode("LIST\r\n"))
data = s.recv(1024)


#Socket local que funcionará como um servidor responsavel pela conexão de cada peer

chat_recebe = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
chat_recebe.bind(('localhost', int(portadeacesso))) #Utilizado para receber mensagens de outro usuário conectado ao servidor central
chat_recebe.listen()

#Função responsável pelo recebimento das mensagens 

def receber_mensagem(chat):
        try:
            conn, addr = chat.accept()
            nome_recebido = conn.recv(1024) #Primeira mensagem que recebe é o nome do usuário que fará a conexão
            print("\nConexão estabelecida com <{}>\n".format(nome_recebido.decode()))
            while True:
                try:
                    mensagem_recebida = conn.recv(1024) #As próximas mensagens chegarão aqui
                    if mensagem_recebida.decode() == "/bye":
                        print("\n<{}> encerrou a conexão".format(nome_recebido.decode()))
                        break
                    elif mensagem_recebida.decode() == "":
                        print("\n<{}> encerrou a conexão".format(nome_recebido.decode()))
                        break
                    print("<{}>:".format(nome_recebido.decode()), mensagem_recebida.decode())
                except:
                    break
        except:
            print("Usuário desconectou")


#Função responsável por enviar as mensagens keepalive para o servidor central 

def keep_alive():
    while 1:
        time.sleep(5)
        s.send(str.encode("KEEP\r\n"))
        
#Thread do keep alive

thread_keep_alive = threading.Thread(target=keep_alive, args=()) 
thread_keep_alive.start() #Start do envio de keep


print("\n----------------------------Lista de comandos------------------------------ ")
print("-Use /list para ter uma lista de usuários online no servidor")
print("-Use /chat para se conectar e trocar mensagens com outro usuário do servidor")
print("-Use /exit para se desconectar do servidor central\n")

#Looping principal de escolhas do usuário 
while 1: 

    #Thread que executa o recebimento de mensagens o tempo todo

    thread_receber = threading.Thread(target=receber_mensagem, args=(chat_recebe,)) 
    thread_receber.start() #Start do recebimento 
    
    comando = input("Digite o comando que deseja: ")

    if(comando == "/list"):
        s.send(str.encode("LIST\r\n"))
        data2 = s.recv(1024)
        usuarios_online = data2.decode().split("LIST") #Vai retirar o LIST enviado pelo servidor quando a lista de usuários for recebida
        usuarios_online_momento = usuarios_online[1] #Vai pegar somente a informação dos nomes dos usuários 
        usuarios_online_momento.strip() #Tira os espaços
        print("Usuários online além de você:", usuarios_online_momento.replace(":",",")) #Troca ";" por ","
        print("\n")
  

    if(comando == "/chat"):
        #Primeira parte da conexão onde o usuário fornece o nome do outro par que deseja conectar diretamente 
        
        nomeconexao = input("Digite o nome do usuário da conexão: ")
        nomeconexao = nomeconexao.strip()
        s.send(str.encode("ADDR {}\r\n".format(nomeconexao)))
        data4 = s.recv(1024)
        mensagem = data4.decode()

        #COLETA DE DADOS ENVIADOS PELO SERVIDOR CENTRAL PARA A CONEXÃO DE UM NOVO SOCKET PARA A CONEXÃO P2P
        
        #Só irá avançar aqui se o nome enviado para conexão for valido. Caso não seja vai entrar no except 
        try: 
                # Dividindo a mensagem pelo ":" e armazenando em uma lista
                partes = mensagem.split(":")

                # Atribuindo os números antes e depois do ":" a variáveis separadas
                primeira_parte = partes[0].split()[1]  # Obtendo a primeira parte após o ":"
                segunda_parte = int(partes[1])  # Obtendo a segunda parte após o ":", removendo espaços em branco


                #Estabelecendo conexão com o usuário requisitado com as informações de porta enviadas pelo servidor central 
                chat_envia = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
                chat_envia.connect(('localhost', segunda_parte))
                chat_envia.send(nome.encode()) #Envio do nome que será recebido como primeira mensagem no socket de receber_mensagem USER <nome>  
                mensagem_enviada = " "
            
                #Looping de envio de mensagens
                while 1: 
                    try: 
                        if mensagem_enviada != "/bye":
                            mensagem_enviada = input("Envie uma mensagem para <{}>:".format(nomeconexao))
                            print("\n")
                            chat_envia.send(mensagem_enviada.encode())
                        else:
                            print("\nConexão encerrada com <{}>".format(nomeconexao))
                            chat_envia.close()
                            break
                    except: 
                        print("\n<{}> não está mais online".format(nomeconexao))
                        chat_envia.close()
                        break
        except:
            print(mensagem)
            continue
        

    if(comando == "/exit"):
        s.close()
        chat_recebe.close()
        sys.exit("Desconectando do servidor central...") #Encerramento do programa
        
    
            
