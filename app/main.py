import socket
from threading import Thread
import os
import argparse
from argparse import Namespace

def decode_and_split(bytes: bytes):
    decoded = bytes.decode("utf-8")
    splitted = decoded.split()
    return splitted

def new_connection(conn: socket, arguments: Namespace):
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
            send_string = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(string)}\r\n\r\n{string}".encode()
            conn.sendall(send_string)
        elif path == "/user-agent":
            string = parsed[6]
            if string:
                send_string = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(string)}\r\n\r\n{string}".encode()
                conn.sendall(send_string)
            else:
                conn.sendall(b"HTTP/1.1 404 NOT FOUND\r\n\r\n")
        elif "/files/" in path:
            if not arguments:
                conn.sendall(b"HTTP/1.1 404 NOT FOUND\r\n\r\n")
            split_path = path.split("/files/")
            file_name = split_path[-1]
            full_file_path = arguments.directory + file_name
            if not os.path.exists(full_file_path):
                conn.sendall(b"HTTP/1.1 404 NOT FOUND\r\n\r\n")
            file = open(full_file_path, "r").read()
            send_string = f"HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream\r\nContent-Length: {len(file)}\r\n\r\n{file}".encode()
            conn.sendall(send_string)               
        else:
            conn.sendall(b"HTTP/1.1 404 NOT FOUND\r\n\r\n")

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
