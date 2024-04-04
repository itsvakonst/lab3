import socket
import json

HOST = '127.0.0.1'  # IP-адрес сервера
PORT = 8888  # порт сервера

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))
    print(f"Подключение к серверу {HOST}:{PORT} успешно!")

    try:
        while True:
            message = input("Введите сообщение для отправки на сервер (или 'exit' для выхода): ")
            if message == 'exit':
                break
            client_socket.sendall(message.encode())

            #data = client_socket.recv(1024)
            #print(f"Получен ответ от сервера: {data.decode()}")

            json_data = b""
            while True:
                chunk = client_socket.recv(1024)
                if not chunk:
                    break
                json_data += chunk
            programs_info = json.loads(json_data)

            # Выводим содержимое JSON с отступами для красивого форматирования
            print("Содержимое JSON:")
            print(json.dumps(programs_info, indent=4, ensure_ascii=False))
    finally:
        client_socket.close()

if __name__ == '__main__':
    main()
