import pika, sys, os, time

def main():
	run = True
	connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
	channel = connection.channel()
	channel.queue_declare(queue='E2', durable = True)
	while(run):
		print('Escolha uma das opcoes, digitando as letras: E, L ou S ')
		print('[E]nviar mensagem')
		print('[L]er mensagem')
		print('[S]air ou Aperte CTRL+C')
		option = input()
		if option == 'E' or option == 'e':
			def callbackE2(ch, method, props, body):
				print(body.decode())
				channel.stop_consuming()
			channel.basic_publish(exchange='', routing_key='qm', body='E2['+'*e*[',properties=pika.BasicProperties(delivery_mode=2))
			channel.basic_consume(queue='E2', on_message_callback=callbackE2, auto_ack = True)
			channel.start_consuming()
			print('Para quem deseja enviar sua msng? Basta especificar seu numero')
			dest = input()
			print('Digite sua mensagem: ')
			msg = input()
			channel.basic_publish(exchange='', routing_key='qm', body='E2['+msg+'[E'+dest,properties=pika.BasicProperties(delivery_mode=2))
			print('Mensagem Enviada')
		if option == 'L' or option == 'l':
			method, prop, body = channel.basic_get(queue='E2')
			try:
				msg_recv = body.decode().split('[')
			except AttributeError:
				print('Nao ha mensagens a serem lidas')
			else:
				print('Mensagem enviada por ' + msg_recv[1])
				print(msg_recv[0])
				channel.basic_ack(delivery_tag = method.delivery_tag)
		if option == 'S' or option == 's':
			run = False
		else:
			print('\nSelecione E, L, S ou Aperte CTRL+C para sair\n')
	connection.close() # fecha conexao com RabbitMQ, fecha o canal
	sys.exit(0)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Exit')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)