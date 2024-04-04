import os
import socket
import struct
import time
import json



def pack_data(data):
    """
    Упаковывает данные перед отправкой через сокет.
    """
    packed_data = json.dumps(data).encode()
    return packed_data

def send_changes(sock, folder):
    """
    Отправляет изменения в содержимом папки через сокет.
    """
    files1 = get_directory_structure(folder)
    packed_data = pack_data(files1)
    sock.sendall(packed_data)

def receive_changes(sock):
    data = b''  # Создаем пустой байтовый объект для хранения данных

while True:
    tmp = sock.recv(1024)  # Получаем данные от сокета
    if tmp:  # Если получены данные
        file_data = json.loads(tmp.decode())  # Декодируем JSON
        print(f"Received {len(file_data)} files with sizes: {file_data}")  # Выводим информацию о полученных файлах
    else:  # Если данные пусты
        break  # Прерываем цикл


if __name__ == "__main__":
    folder1 = input("Введите путь к первой папке: ")
    
    # Установить сокетное соединение с программой 1
    server_address = ('localhost', 10000)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    connected = False
    while not connected:
        try:
            sock.connect(server_address)
            connected = True
        except ConnectionRefusedError:
            print("Не удалось установить соединение. Повторная попытка через 10 секунд...")
            time.sleep(10)

    while True:
        def get_directory_structure(folder):
            """Получает структуру папки, возвращает список файлов и их размеры."""
            files = []
            for dirpath, _, filenames in os.walk(folder):
              for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                filesize = os.path.getsize(filepath)
                files.append((filename, filesize))
            return files
        # Отправить содержимое своей папки программе 1
        send_changes(sock, folder1)
        # Получить изменения из программы 1 и применить их к своей папке
        receive_changes(sock)
        # Дополнительно можно добавить логику ожидания или цикла проверки каждые n секунд
        time.sleep(5)
