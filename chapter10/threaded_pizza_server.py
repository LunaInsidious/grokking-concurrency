from socket import socket, create_server
from threading import Thread

BUFFER_SIZE = 1024
ADDRESS = ("127.0.0.1", 12345)


class Handler(Thread):
    def __init__(self, conn: socket) -> None:
        super().__init__()
        self.conn = conn

    def run(self) -> None:
        print(f"Connected to {self.conn.getpeername()}")
        try:
            while True:
                data = self.conn.recv(BUFFER_SIZE)
                if not data:
                    break
                try:
                    order = int(data.decode())
                    response = f"Thank you for ordering {order} pizzas!\n"
                except ValueError:
                    response = "Wrong number of pizzas, please try again\n"
                print(f"Sending message to {self.conn.getpeername()}")
                self.conn.send(response.encode())
        finally:
            print(f"Connection with {self.conn.getpeername()} has been closed")
            self.conn.close()


class Server:
    def __init__(self) -> None:
        try:
            print(f"Starting up at: {ADDRESS}")
            self.server_socket: socket = create_server(ADDRESS)
        except OSError:
            self.server_socket.close()
            print("\nServer stopped.")

    def start(self) -> None:
        print("Server listening for incoming connections")
        try:
            while True:
                # クライアントからの接続リクエストを受信したら、クライアントごとに接続を処理するためのスレッドを作成
                conn, address = self.server_socket.accept()
                print(f"Client connection request from {address}")
                handler = Handler(conn)
                handler.start()
        finally:
            self.server_socket.close()
            print("\nServer stopped.")


if __name__ == "__main__":
    server = Server()
    server.start()
