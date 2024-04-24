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
        if path == "/":
            conn.send(b"HTTP/1.1 200 OK\r\n\r\n")
        else:
            split_path = path.split("/")
            is_echo = split_path[0] == "echo"
            if not is_echo:
                conn.send(b"HTTP/1.1 404 Not Found\r\n\r\n")
            string = split_path[1]
            send_string = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent length: {len(string)}\r\n\r\n{string}"
            print(f"Sending response: {send_string}")
            encoded_string = send_string.encode()
            conn.send(encoded_string)

if __name__ == "__main__":
    main()
