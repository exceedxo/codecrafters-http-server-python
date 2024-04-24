import socket

def main():
    print("Starting server...")
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    print("Server started")
    print("Waiting for client...")
    (conn, address) = server_socket.accept() # wait for client
    print("Client connected.")
    while conn:
        receive = conn.recv(2048)
        print(f"raw: {receive}")
        decoded = str(receive, encoding='utf-8')
        print(f"decoded: {decoded}")
        splitted = receive.split()
        print(f"splitted: {splitted}")
        if receive[1] == "/":
            conn.send(b"HTTP/1.1 200 OK\r\n\r\n")
        else:
            conn.send(b"HTTP/1.1 404 Not Found\r\n\r\n")

if __name__ == "__main__":
    main()
