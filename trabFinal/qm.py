import pika, sys, os, time

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel() # abre um canal com o RabbitMQ
    channel.queue_declare(queue='qm', durable = True) # declara 4 filas onde mensagens serao recebidas e enviadas
    channel.queue_declare(queue='E1', durable = True) # durable, torna a fila persistente mesmo se RabbitMQ parar
    channel.queue_declare(queue='E2', durable = True)
    channel.queue_declare(queue='E3', durable = True)
    def callbackQM(ch, method, props, body):
        id_sen, msg , id_dest = body.decode().split('[')# divide a msgn que chega em body em uma lista com 3 elementos separados por '['
        if(msg == '*e*' and id_sen == 'E1'):
            channel.basic_publish(exchange='',routing_key= id_sen, body = 'E2 e E3 disponíveis', properties=pika.BasicProperties(delivery_mode=2))
            channel.basic_ack(delivery_tag = method.delivery_tag)# confirma o recebimento da mensagem
        elif (msg == '*e*' and id_sen == 'E2'):
            channel.basic_publish(exchange='',routing_key= id_sen, body = 'E1 e E3 disponíveis', properties=pika.BasicProperties(delivery_mode=2))
            channel.basic_ack(delivery_tag = method.delivery_tag)# confirma o recebimento da mensagem
        elif (msg == '*e*' and id_sen == 'E3'):
            channel.basic_publish(exchange='',routing_key= id_sen, body = 'E1 e E2 disponíveis', properties=pika.BasicProperties(delivery_mode=2))
            channel.basic_ack(delivery_tag = method.delivery_tag)# confirma o recebimento da mensagem

        else:
            print('Mensagem Recebida da Entidade ' + id_sen)# id_sen = remetente, msg = msgn recebida, id_dest = destinatario
            channel.basic_publish(exchange='',routing_key = id_dest, body = msg+'['+id_sen,properties=pika.BasicProperties(delivery_mode=2)) #envia msg para fila do is_dest com modo de entrega persistente (delivery_mode = 2)
            print('Mensagem Enviada da Entidade ' + id_sen + ' para Entidade ' + id_dest)
            channel.basic_ack(delivery_tag = method.delivery_tag)# confirma o recebimento da mensagem


    channel.basic_consume(queue='qm', on_message_callback=callbackQM) # recebe mensagens da fila qm, e toda vez que recebe executa callbackQM
    print('Esperando requisicoes... Para sair aperte CTRL+C')
    channel.start_consuming() # loop de consumo


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt: #para sair usando CTRL+C
        print('Exit')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)