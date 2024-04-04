import os
import json
import socket


def get_programs_in_path(path):
    """
    Функция, получает список программ в указанной директории.
    принимает:
        path (str): путь к директории.
    возвращает:
        list: список программ.
    """
    programs = []

    # существует ли указанная директория и является ли она директорией
    if os.path.exists(path) and os.path.isdir(path):
        # получаем список файлов в директории
        files = os.listdir(path)
        # фильтруем файлы, чтобы остались только исполняемые программы
        programs = [file for file in files if
                    os.path.isfile(os.path.join(path, file)) and os.access(os.path.join(path, file), os.X_OK)]

    return programs


def get_programs_in_path_env():
    """
    Функция, получает информацию о директориях из переменной окружения PATH
    и список программ в каждой директории.
    возвращает: словарь с информацией о директориях и программах.
    """
    # значение переменной окружения PATH
    path_env = os.getenv("PATH")
    # делим значение на отдельные пути
    paths = path_env.split(os.pathsep)

    programs_info = {}

    # для каждого пути получаем список программ
    for path in paths:
        programs = get_programs_in_path(path)
        programs_info[path] = programs

    return programs_info


def save_programs_info_to_file(programs_info, filepath):
    """
    Функция, сохраняет информацию о программах в файл в формате JSON
        programs_info (dict): словарь с информацией о программах
        filepath (str): путь к файлу который JSON
    """
    with open(filepath, "w") as file:
        # сохраняем словарь в файл в формате JSON с отступами 4
        json.dump(programs_info, file, indent=4)


def handle_event(client_socket):
    """
    Событие по ключу 
    """
    # Получаем информацию о программах
    programs_info = get_programs_in_path_env()
    # Сохраняем информацию в файл
    save_programs_info_to_file(programs_info, "programs_info.json")
    # Ответ для клиента
    #response = f"Информация обновлена. Добавлено программ: {added_programs}, удалено программ: {removed_programs}"
    # Отправляем ответ клиенту
    #client_socket.sendall(response.encode())
    # Отправляем файл клиенту
    client_socket.sendall(json.dumps(programs_info).encode())
