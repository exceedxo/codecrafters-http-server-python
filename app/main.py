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
        path = parsed[1]
        string = path.split("/")[-1]
        if string:
            send_string = string.encode(f"HTTP/1.1 OK\r\nContent-Type: text/plain\r\nContent length: {len(string)}\r\n\r\n{string}")
            conn.send(send_string)

if __name__ == "__main__":
    main()
