from pika import ConnectionParameters,BlockingConnection

connection_params = ConnectionParameters(host="localhost", port=5672)


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body.decode())
    ch.basic_ack(delivery_tag=method.delivery_tag)


def main() -> None:
    with BlockingConnection(connection_params) as connection:
        with connection.channel() as channel:
            channel.queue_declare(queue="messages")
            channel.basic_consume(queue="messages", on_message_callback=callback)
            print("Waiting for messages...")
            channel.start_consuming()


main()
