import socket
from threading import Thread
import os
import argparse
from argparse import Namespace

def decode_and_split(bytes: bytes):
    decoded = bytes.decode("utf-8")
    splitted = decoded.split()
    return splitted

def decode_and_find_contents(bytes: bytes):
    decoded = bytes.decode("utf-8")
    splitted = decoded.split("\r\n")
    return splitted

def new_connection(conn: socket, arguments: Namespace):
    print("New client connected.")
    while conn:
        receive = conn.recv(2048)
        parsed = decode_and_split(receive)
        print(parsed)
        method = parsed[0]
        path = parsed[1]
        if path == "/":
            conn.sendall(b"HTTP/1.1 200 OK\r\n\r\n")
        elif "/echo/" in path:
            split_path = path.split("/echo/")
            string = split_path[1]
            send_string = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(string)}\r\n\r\n{string}".encode()
            conn.sendall(send_string)
        elif path == "/user-agent":
            string = parsed[6]
            if string:
                send_string = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(string)}\r\n\r\n{string}".encode()
                conn.sendall(send_string)
            else:
                conn.sendall(b"HTTP/1.1 404 Not Found\r\n\r\n")
        elif "/files/" in path and method == "GET":
            split_path = path.split("/files/")
            file_name = split_path[-1]
            directory_path = arguments.directory
            if not directory_path:
                conn.sendall(b"HTTP/1.1 404 Not Found\r\nContent-Length: 0\r\n\r\n")
            full_file_path = os.path.join(directory_path, file_name)
            if os.path.exists(full_file_path):
                file = open(full_file_path, "r").read()
                send_string = f"HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream\r\nContent-Length: {len(file)}\r\n\r\n{file}".encode()
                conn.sendall(send_string)   
            else:
                conn.sendall(b"HTTP/1.1 404 Not Found\r\nContent-Length: 0\r\n\r\n") 
        elif "files" in path and method == "POST":
            split_path = path.split("/files/")
            file_name = split_path[-1]
            directory_path = arguments.directory
            contents = decode_and_find_contents(receive)[-1]
            print(contents)
            if not directory_path:
                conn.sendall(b"HTTP/1.1 404 Not Found\r\nContent-Length: 0\r\n\r\n")
            full_file_path = os.path.join(directory_path, file_name)
            if os.path.exists(full_file_path):
                file = open(full_file_path, "r").read()
                send_string = f"HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream\r\nContent-Length: {len(file)}\r\n\r\n{file}".encode()
                conn.sendall(send_string)   
            else:
                conn.sendall(b"HTTP/1.1 404 Not Found\r\nContent-Length: 0\r\n\r\n")            
        else:
            conn.sendall(b"HTTP/1.1 404 Not Found\r\n\r\n")

def main():
    print("Starting server...")
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    argument_parser: argparse.ArgumentParser = argparse.ArgumentParser()
    argument_parser.add_argument("--directory")
    arguments = argument_parser.parse_args()
    print("Server started!")
    while True:
        (conn, address) = server_socket.accept()
        thread = Thread(target=new_connection, args=(conn, arguments))
        thread.start()

if __name__ == "__main__":
    main()
