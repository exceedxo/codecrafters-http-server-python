import socket
import asyncio

async def decode_and_split(bytes: bytes):
    decoded = bytes.decode("utf-8")
    splitted = decoded.split()
    return splitted

async def new_connection(conn: socket):
    print("Client connected.")
    while conn:
        receive = await conn.recv(2048)
        parsed = decode_and_split(receive)
        path = parsed[1]
        if path == "/":
            await conn.sendall(b"HTTP/1.1 200 OK\r\n\r\n")
        elif "/echo/" in path:
            split_path = path.split("/echo/")
            string = split_path[1]
            send_string = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(string)}\r\n\r\n{string}"
            encoded_string = send_string.encode()
            await conn.sendall(encoded_string)
        elif path == "/user-agent":
            string = parsed[6]
            if string:
                send_string = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(string)}\r\n\r\n{string}"
                encoded_string = send_string.encode()
                await conn.sendall(encoded_string) #
            else:
                await conn.sendall(b"HTTP/1.1 404 NOT FOUND\r\n\r\n")        
        else:
            await conn.sendall(b"HTTP/1.1 404 NOT FOUND\r\n\r\n")

async def main():
    print("Starting server...")
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    print("Server started")
    print("Waiting for client...")
    while True:
        (conn, address) = await server_socket.accept()
        asyncio.create_task(new_connection(conn))
    
if __name__ == "__main__":
    asyncio.run(main())
