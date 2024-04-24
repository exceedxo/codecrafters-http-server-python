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
        print(f"[M] Parsed: {parsed}")
        path = parsed[1] if len(parsed) >= 1 else parsed[0]
        print(f"[M] Path: {path}")
        if path == "/":
            conn.send(b"HTTP/1.1 200 OK\r\n\r\n")
        elif "/echo/" in path:
            split_path = path.split("/echo/")
            print(f"[M] Split Path: {split_path}")
            string = split_path[1]
            print(f"[M] String: {string}")
            send_string = f"HTTP/1.1 200 OK\r\n\r\nContent-Type: text/plain\r\nContent length: {len(string)}\r\n\r\n{string}"
            print(f"[M] Send String:\n{send_string}")
            encoded_string = send_string.encode()
            conn.sendall(encoded_string)
        else:
            conn.send(b"HTTP/1.1 404 Not Found\r\n\r\n")

if __name__ == "__main__":
    main()
