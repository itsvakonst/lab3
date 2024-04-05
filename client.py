import socket

def send_data(server_socket, data):
    server_socket.send(data.encode())

def receive_data(server_socket):
    data = server_socket.recv(1024).decode()
    return data

def main():
    host = "127.0.0.1"
    port = 12345

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.connect((host, port))
    print("Подключено к серверу")

    server_socket.send('2'.encode('utf-8'))

    while True:
        user_input = input("Введите число (или 'GET_FILE' для запроса файла): ")
        '''if user_input == "END" :
            send_data(server_socket, "END")
            break'''
        if user_input == "":
            send_data(server_socket, "")
            break
        elif user_input == "GET_FILE":
            folder_name = input("Введите номер запуска программы: ")
            file_number = input("Введите номер дерева: ")
            send_data(server_socket, "GET_FILE")
            send_data(server_socket, f"{folder_name},{file_number}")
            file_data = receive_data(server_socket)
            print("Полученный файл:")
            print(file_data)
        else:
            send_data(server_socket, user_input)

    server_socket.close()

if __name__ == "__main__":
    main()
