import socket

def main():
    print("Starting server...")
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    print("Server started")
    print("Waiting for client...")
    server_socket.accept() # wait for client

if __name__ == "__main__":
    main()
