import typing as T
from socket import socket, create_server

BUFFER_SIZE = 1024
ADDRESS = ("127.0.0.1", 12345)


class Server:
    clients: T.Set[socket] = set()

    def __init__(self) -> None:
        try:
            print(f"Starting up at: {ADDRESS}")
            self.server_socket: socket = create_server(ADDRESS)
            # サーバーソケットをノンブロッキングモードに設定し、接続を待っている間にブロックされないようにする
            self.server_socket.setblocking(False)
        except OSError:
            self.server_socket.close()
            print("\nServer stopped.")

    def accept(self) -> None:
        try:
            conn, client_address = self.server_socket.accept()
            print(f"Connected to {client_address}")
            # クライアントソケットをノンブロッキングモードに設定し、データを受信する際にブロックされないようにする
            conn.setblocking(False)
            self.clients.add(conn)
        # この例外は、ソケットから読み込めるデータがない場合に、ノンブロッキングソケットに対処するためにキャッチされる
        # このようにすると、プログラムがブロッキングを回避し、読み込めるデータを待つ他のクライアントの実行を継続できるようになる
        except BlockingIOError:
            pass

    def serve(self, conn: socket) -> None:
        try:
            while True:
                data = conn.recv(BUFFER_SIZE)
                if not data:
                    break
                try:
                    order = int(data.decode())
                    response = f"Thank you for ordering {order} pizzas!\n"
                except ValueError:
                    response = "Wrong number of pizzas, please try again\n"
                print(f"Sending message to {conn.getpeername()}")
                conn.send(response.encode())
        except BlockingIOError:
            print(f"No data to read from {conn.getpeername()}")
            pass

    def start(self) -> None:
        print("Server listening for incoming connections")
        try:
            while True:
                self.accept()
                for client in self.clients.copy():
                    self.serve(client)
        finally:
            self.server_socket.close()
            print("\nServer stopped.")


if __name__ == "__main__":
    server = Server()
    server.start()
