# Echo client program
import socket

TARGET_HOST = 'localhost'    # The remote host
TARGET_PORT = 8080              # The same port as used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((TARGET_HOST, TARGET_PORT))
    s.sendall(b'Hello, world')
    data = s.recv(1024)

response = data.decode('utf-8')

if response == "OK\n":
    print("Сервер возвращает корректный ответ 'OK'")
else:
    print(f"Неверный ответ сервера. Ожидался 'OK\\n', получен: {response}")