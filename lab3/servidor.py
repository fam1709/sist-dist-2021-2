from pathlib import Path

import socket, time, select, sys, threading

HOST = ''    # '' possibilita acessar qualquer endereco alcancavel da maquina local
PORT = 1025  # porta onde chegarao as mensagens para essa aplicacao

entradas = [sys.stdin]

def iniciaServidor():
	'''Cria um socket de servidor e o coloca em modo de espera por conexoes
	Saida: o socket criado'''
	# cria o socket 
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Internet( IPv4 + TCP) 

	# vincula a localizacao do servidor
	sock.bind((HOST, PORT))

	# coloca-se em modo de espera por conexoes
	sock.listen(5) 

	# configura o socket para o modo nao-bloqueante
	sock.setblocking(False)

	# inclui o socket principal na lista de entradas de interesse
	entradas.append(sock)

	return sock

def aceitaConexao(sock):
	'''Aceita o pedido de conexao de um cliente
	Entrada: o socket do servidor
	Saida: o novo socket da conexao e o endereco do cliente'''

	# estabelece conexao com o proximo cliente
	clisock, endr = sock.accept() 

	return clisock, endr

def atendeRequisicoes(clisock, endr):
		while True:
			msg = clisock.recv(1024) # argumento indica a qtde maxima de dados
			if not msg:
				clisock.close()
				return
			elif(str(msg, encoding='utf-8') == 'exit'):
				clisock.send(b'Encerrando conexao')
				clisock.close()
				return
			else:
				clisock.send(b'Verificando arquivo...\n')
				input_list = str(msg, encoding='utf-8').split()
				try: # tenta apos o split, colocar os elementos da entrada do cliente em duas variaveis
					file_name = input_list[0]
					word_name = input_list[1]
				except IndexError:# falha se cliente digitar uma entrada apenas ao inves de 2, a 1ª seguida de espaço e a 2ª
					clisock.send(b'Entrada invalida\n' + b'Nao esqueca de dar espaco entre o nome do arquivo e a palavra desejada')
					time.sleep(0.5)
					clisock.send(b'endProcessing')
				else:
						
					p = Path(__file__).with_name(file_name+'.txt')
					try: # tenta abrir o arquivo
						file = open(p,'r')
					except OSError:
						clisock.send(b'Arquivo = ' + file_name.encode() + b'.txt invalido\n' + b'Favor seguir o formato: nome_arquivo palavra\n' + b'Tente novamente ou digite exit para sair.')
						time.sleep(0.5)
						clisock.send(b'endProcessing')
					else:
						clisock.send(b'Arquivo aberto com sucesso!\n')
						clisock.send(b'Contando ocorrencias da palavra ' + word_name.encode()+b' ...\n')
						data = file.read()
						words_file = data.split()
						count = 0
						clisock.send(b'Processando...\n')
						for x in words_file:
							if(x == word_name):
								count = count + 1
						# envia mensagem de resposta
						clisock.send(b'Numero de ocorrencias da palavra ' + word_name.encode() + b' = '+ str(count).encode()+b'\n')
						file.close()
						clisock.send(b'Para continuar digite: continue\n' +b'Para sair digite: exit\n')
						# necessario um delay para fazer a comparacao no lado do cliente que o processamento acabou usando esta msgn em particular
						# sem o delay o servidor manda um pacote de mensagens ao cliente e a comparacao nao sera bem sucedida
						time.sleep(1)
						clisock.send(b'endProcessing')
			

def main():
	sock = iniciaServidor()
	print("Pronto para receber conexoes...")
	print("Digite end para sair")
	clientes=[]
	while True:
		#espera por qualquer entrada de interesse
		leitura, escrita, excecao = select.select(entradas, [], [])
		#tratar todas as entradas prontas
		for pronto in leitura:
			if pronto == sock:  #pedido novo de conexao
				clisock, endr = aceitaConexao(sock)
				print ('Conectado com: ', endr)			
				cliente = threading.Thread(target=atendeRequisicoes, args=(clisock,endr))
				cliente.start()
				clientes.append(cliente)
			elif pronto == sys.stdin: #entrada padrao
				cmd = input()
				if cmd == 'end': #solicitacao de finalizacao do servidor
					for c in clientes:
						c.join()					
					sock.close()
					sys.exit()
main()