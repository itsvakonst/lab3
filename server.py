#!/usr/bin/python3

import socket
import asyncio
import threading


class Handler:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.__setattr__('handlers', {})
            cls._instance.__setattr__('async_handlers', {})
        return cls._instance

    def __init__(self):
        pass

    def route(self, is_async, event):
        def decorator(func):
            if is_async:
                self.async_handlers[event] = func
            else:
                self.handlers[event] = func
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            return wrapper
        return decorator

    async def async_handle_event(self, reader, writer):
        addr = writer.get_extra_info('peername')
        print(f"Подключился клиент {addr}")
        data = await reader.read(100)
        event = data.decode()
        #event = event[:-2] #Потому что я тестил с `telnet 127.0.0.1 8888`
        print(f'Handshake "{event}"')
        if event in self.async_handlers:
            await self.async_handlers[event](reader, writer)
        else:
            print(f"No handler for event: {event}")

    def handle_event(self, client_socket):
        print(f"Подключился клиент")
        data = client_socket.recv(100)
        event = data.decode()
        #event = event[:-2] #Потому что я тестил с `telnet 127.0.0.1 8888`
        print(f'Handshake "{event}"')
        if event in self.handlers:
            self.handlers[event](client_socket)
        else:
            print(f"No handler for event: {event}")
        client_socket.close()


class Server:
    def __init__(self, host, port):
        self._host = host
        self._port = port

    def start(self, is_async=True):
        if is_async:
            asyncio.run(self._async_start())
        else:
            self._thread_start()

    async def _async_start(self):
        server = await asyncio.start_server(
            Handler().handle_event, self._host, self._port)
    
        addr = server.sockets[0].getsockname()
        print(f'Сервер запущен на {addr}')
    
        async with server:
            await server.serve_forever()

    def _thread_start(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self._host, self._port))
        server_socket.listen(1)
        print(f"Сервер запущен и слушает на {self._host}:{self._port}")
    
        try:
            while True:
                client_sock, address = server_socket.accept()
                print(f"Принято соединение от {address}")
                client_handler = threading.Thread(
                    target=Handler().handle_event,
                    args=(client_sock,)  # Передаем сокет клиента в поток
                )
                client_handler.start()
        finally:
            server_socket.close()





