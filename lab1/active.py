# Exemplo basico socket (lado ativo)

import socket

HOST = 'localhost' # maquina onde esta o par passivo
PORTA = 5000        # porta que o par passivo esta escutando

# cria socket
sock = socket.socket() # default: socket.AF_INET, socket.SOCK_STREAM 

# conecta-se com o par passivo
sock.connect((HOST, PORTA)) 

print('Digite uma mensagem para ser enviada ou digite exit para sair')
while True:
	msg_send = input().encode()

	# envia uma mensagem para o par conectado
	sock.send(msg_send)

	#espera a resposta do par conectado (chamada pode ser BLOQUEANTE)
	msg_recv = sock.recv(1024) # argumento indica a qtde maxima de bytes da mensagem

	# imprime a mensagem recebida
	print('Resposta Echo: ' + str(msg_recv,  encoding='utf-8'))
	# encerra a conexao
	if(str(msg_send, encoding='utf-8') == 'exit'):
		sock.close()
		break

