import socket

HOST = 'localhost' # maquina onde esta o par passivo
PORTA = 5000        # porta que o par passivo esta escutando

# cria socket
sock = socket.socket() # default: socket.AF_INET, socket.SOCK_STREAM 

print('Iniciando Conexao...')
# conecta-se com o par passivo
sock.connect((HOST, PORTA))
sock.send(b'Conexao Requisitada')
print(str(sock.recv(1024), encoding ='utf-8'))

msg_init = 'Digite o nome do arquivo e a palavra que deseja ser processada ou digite exit para sair\n' + 'Siga o formato: nome_arquivo palavra'

print(msg_init)

while True:
	msg_send = input().encode()

	# encerra a conexao
	if(str(msg_send, encoding='utf-8') == 'exit'):
		sock.close()
		break
	# continua a execucao ate exit
	if(str(msg_send, encoding='utf-8') == 'continue'):
		print(msg_init)
		msg_send = input().encode()
		# encerra apos a primeira execucao
		if(str(msg_send, encoding='utf-8') == 'exit'):
			sock.close()
			break

	# envia a entrada para o servidor
	sock.send(msg_send)

	msg_recv = sock.recv(1024)

	# imprime a resposta do servidor recebida, caso receba endProcessing volta a realizar novas requisicoes
	while(str(msg_recv,  encoding='utf-8') != 'endProcessing'):
		print(str(msg_recv,  encoding='utf-8'))
		msg_recv = sock.recv(1024)


