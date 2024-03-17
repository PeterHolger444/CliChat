import socket
import threading

def handle_command(client_socket, command):
    if command[2:].split(',')[0] == 'exit':
        client_socket.send('exit ok'.encode())
        
        clients.remove(client_socket)
        client_socket.close()
        
        broadcast(command.encode(), client_socket)
    
def handle_client(client_socket, address):
    print(f"[+] Accepted connection from {address}")

    while True:
        try:
            data = client_socket.recv(1024).decode()
            if not data:
                break
            
            # client sends a command
            if data[0] == 'c':
                handle_command(client_socket, data)
                break
            
            # client sends a message
            else:
                broadcast(data.encode(), client_socket)
        except Exception as e:
            print(f"Error: {e}")
            clients.remove(client_socket)
            client_socket.close()
            break

    print(f"[-] Connection from {address} closed.")
    client_socket.close()

def broadcast(message, sender):
    for client in clients:
        if client != sender:
            try:
                client.send(message)
            except Exception as e:
                print(f"Error broadcasting message: {e}")
                client.close()
                clients.remove(client)

global clients
clients = []

# Server configuration
host = '127.0.0.1'
port = 9999

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
server_socket.listen(5)

print(f"[*] Listening on {host}:{port}")

while True:
    client_socket, address = server_socket.accept()

    clients.append(client_socket)

    client_thread = threading.Thread(target=handle_client, args=(client_socket, address))
    client_thread.start()
