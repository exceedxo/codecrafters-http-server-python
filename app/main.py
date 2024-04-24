import socket

def main():
    print("Starting server...")
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    print("Server started")
    print("Waiting for client...")
    (conn, address) = server_socket.accept() # wait for client
    print("Client connected")
    conn.send("HTTP/1.1 200 OK\r\n\r\n")

if __name__ == "__main__":
    main()
