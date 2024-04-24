import socket

def decode_and_split(bytes: bytes):
    decoded = bytes.decode("utf-8")
    splitted = decoded.split()
    return splitted

def main():
    print("Starting server...")
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    print("Server started")
    print("Waiting for client...")
    (conn, address) = server_socket.accept() # wait for client
    print("Client connected.")
    while conn:
        receive = conn.recv(2048)
        parsed = decode_and_split(receive)
        print(parsed)

if __name__ == "__main__":
    main()
