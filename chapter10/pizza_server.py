from socket import socket, create_server

# 一度に受信するデータの最大量を設定
BUFFER_SIZE = 4096
# ホストマシンのアドレスとポートを定義
ADDRESS = ("127.0.0.1", 12345)


class Server:
    def __init__(self) -> None:
        try:
            print(f"Starting up at: {ADDRESS}")
            # 指定されたアドレスにバインドされたサーバーソケットオブジェクトを作成
            self.server_socket: socket = create_server(ADDRESS)
        except OSError:
            self.server_socket.close()
            print("\nServer stopped.")

    def accept(self) -> socket:
        # クライアントがサーバーソケットに接続するまでブロックされ、新しい接続とそのクライアントのソケットを返す
        conn, client_address = self.server_socket.accept()
        print(f"Connected to {client_address}")
        return conn

    def serve(self, conn: socket) -> None:
        try:
            while True:
                # クライアントからのデータを受信
                data = conn.recv(BUFFER_SIZE)
                # データが送信されてくるまでクライアントソケットから継続的にデータを受信
                if not data:
                    break
                try:
                    order = int(data.decode())
                    response = f"Thank you for ordering {order} pizzas!\n"
                except ValueError:
                    response = "Wrong number of pizzas, please try again\n"
                print(f"Sending message to {conn.getpeername()}")
                # クライアントソケットにレスポンスを送信
                conn.send(response.encode())
        finally:
            print(f"Connection with {conn.getpeername()} has been closed")
            # そのクライアントに対するserveメソッドの実行が終了したら、クライアントソケットを閉じる
            conn.close()

    def start(self) -> None:
        print("Server listening for incoming connections")
        # サーバーが停止するまで接続を受け入れながら各クライアントにサービスを提供
        try:
            while True:
                conn = self.accept()
                self.serve(conn)
        finally:
            self.server_socket.close()
            print("\nServer stopped.")


if __name__ == "__main__":
    server = Server()
    server.start()
