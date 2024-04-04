
from server import *

handler = Handler()

@handler.route(event='echo', is_async=True)
async def handle_echo(reader, writer):
    while True:
        data = await reader.read(100)
        if not data:
            break
        message = data.decode()

        print(f"Отправка эхо-ответа: {message}")
        writer.write(data)
        await writer.drain()


    print(f"Handling disconnect with data: {data}")


@handler.route(event='echo', is_async=False)
def handle_echo(client_socket):
    while True:
        data = client_socket.recv(100)
        if not data:
            break
        message = data.decode()

        print(f"Отправка эхо-ответа: {message}")
        client_socket.send(data)


    print(f"Handling disconnect with data: {data}")


