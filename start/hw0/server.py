# Echo server program
import socket

HOST = ''
PORT = 8080         

def handle_client(client_socket):
    try: 
        # Устанавливаем небольшой таймаут, чтобы сервер не висел вечно
        # client_socket.settimeout(2)
        
        # отправляем сообщение клиенту
        data = "OK\n".encode('utf-8')
        client_socket.sendall(data)
    except socket.timeout:
        print("[!] Timeout waiting for request, just sending OK")
    finally:
        client_socket.close()


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # привязываем сокет к порту
    s.bind((HOST, PORT))
    
    # переводит сокет в режим ожидания. 
    # 1 — это размер очереди (сколько клиентов могут ждать, 
    # пока сервер занят первым).
    s.listen(5) 
    while True:
        # ждем соединение
        conn, addr = s.accept()
        print('Connected by', addr)
        handle_client(conn)

