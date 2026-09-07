from pika import ConnectionParameters, BlockingConnection

connection_params = ConnectionParameters(host="localhost", port=5672)


def main() -> None:
    with BlockingConnection(connection_params) as connection:
        with connection.channel() as channel:
            channel.queue_declare(queue="messages")
            channel.basic_publish(exchange="", routing_key="messages", body="Hello World!")
            print("OKEY LETS GO")


main()
