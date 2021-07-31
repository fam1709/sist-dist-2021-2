from pathlib import Path

import socket, time

HOST = ''    # '' possibilita acessar qualquer endereco alcancavel da maquina local
PORTA = 5000  # porta onde chegarao as mensagens para essa aplicacao

# cria um socket para comunicacao
sock = socket.socket() # valores default: socket.AF_INET, socket.SOCK_STREAM  

# vincula a interface e porta para comunicacao
sock.bind((HOST, PORTA))

# define o limite maximo de conexoes pendentes e coloca-se em modo de espera por conexao
sock.listen(5) 

# aceita a primeira conexao da fila (chamada pode ser BLOQUEANTE)
novoSock, endereco = sock.accept() # retorna um novo socket e o endereco do par conectado
msg_connect_req = novoSock.recv(1024)
print ( str(msg_connect_req, encoding='utf-8') + ' Conectado com: ', endereco)
novoSock.send(b'Conexao feita com sucesso!')

while True:
	# depois de conectar-se, espera uma mensagem (chamada pode ser BLOQUEANTE))
	msg = novoSock.recv(1024) # argumento indica a qtde maxima de dados
	if not msg: break
	if(str(msg, encoding='utf-8') == 'exit'):
		novoSock.send(b'Encerrando conexao')
		break
	else:
		novoSock.send(b'Verificando arquivo...\n')
		input_list = str(msg, encoding='utf-8').split()
		file_name = input_list[0]
		word_name = input_list[1]
		p = Path(__file__).with_name(file_name+'.txt')
		try:
			file = open(p,'r')
		except OSError:
			novoSock.send(b'Arquivo = ' + file_name.encode() + b' invalido\n' + b'Favor seguir o formato: nome_arquivo palavra\n' + b'Tente novamente ou digite exit para sair.')
			time.sleep(0.5)
			novoSock.send(b'endProcessing')
		else:
			novoSock.send(b'Arquivo aberto com sucesso!\n')
			novoSock.send(b'Contando ocorrencias da palavra ' + word_name.encode()+b' ...\n')
			data = file.read()
			words_file = data.split()
			count = 0
			novoSock.send(b'Processando...\n')
			for x in words_file:
				if(x == word_name):
					count = count + 1
			# envia mensagem de resposta
			novoSock.send(b'Numero de ocorrencias da palavra ' + word_name.encode() + b' = '+ str(count).encode()+b'\n')
			file.close()
			novoSock.send(b'Para continuar digite: continue\n' +b'Para sair digite: exit\n')
			# necessario um delay para fazer a comparacao no lado do cliente que o processamento acabou usando esta msgn em particular
			# sem o delay o servidor manda um pacote de mensagens ao cliente e a comparacao nao sera bem sucedida
			time.sleep(1)
			novoSock.send(b'endProcessing')


# fecha o socket da conexao
novoSock.close() 
# fecha o socket principal
sock.close()

