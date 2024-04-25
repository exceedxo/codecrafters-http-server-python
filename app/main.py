import socket
from threading import Thread
import os

def decode_and_split(bytes: bytes):
    decoded = bytes.decode("utf-8")
    splitted = decoded.split()
    return splitted

def new_connection(conn: socket):
    print("New client connected.")
    while conn:
        receive = conn.recv(2048)
        parsed = decode_and_split(receive)
        path = parsed[1]
        if path == "/":
            conn.sendall(b"HTTP/1.1 200 OK\r\n\r\n")
        elif "/echo/" in path:
            split_path = path.split("/echo/")
            string = split_path[1]
            send_string = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(string)}\r\n\r\n{string}"
            encoded_string = send_string.encode()
            conn.sendall(encoded_string)
        elif path == "/user-agent":
            string = parsed[6]
            if string:
                send_string = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(string)}\r\n\r\n{string}"
                encoded_string = send_string.encode()
                conn.sendall(encoded_string) #
            else:
                conn.sendall(b"HTTP/1.1 404 NOT FOUND\r\n\r\n")
        elif "/files/" in path:
            split_path = path.split("/files/")
            file_name = split_path[-1]
            if os.path.exists(file_name):
                file = os.open(file_name)
                send_string = f"HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream\r\nContent-Length: {len(file)}\r\n\r\n{file}".encode()
                print(send_string)
                conn.sendall(send_string)
            else:
                conn.sendall(b"HTTP/1.1 404 NOT FOUND\r\n\r\n")  
                 
        else:
            conn.sendall(b"HTTP/1.1 404 NOT FOUND\r\n\r\n")

def main():
    print("Starting server...")
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    print("Server started!")
    while True:
        (conn, address) = server_socket.accept()
        thread = Thread(target=new_connection, args=(conn,))
        thread.start()

if __name__ == "__main__":
    main()
