import socket
import os.path
import time
from threading import Thread, current_thread

SOCK_FILE = "./mailbox"
BUFFER_SIZE = 1024


class Sender(Thread):
    def run(self) -> None:
        self.name = "Sender"
        # Senderスレッド用の新しいソケットを作成。
        # AF_UNIX(UNIXドメインソケット)とSOCK_STREAMはそれぞれ
        # アドレスファミリとソケットタイプを表す定数
        client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        # Senderスレッドのソケットを「チャネル(UNIXソケットファイル)」に接続
        client.connect(SOCK_FILE)

        messages = ["Hello", " ", "world!"]
        for msg in messages:
            # Senderスレッドのソケット経由で一連のメッセージを送信
            print(f"{current_thread().name}: Send: '{msg}'")
            client.sendall(str.encode(msg))
            time.sleep(1)

        client.close()


class Receiver(Thread):
    def run(self) -> None:
        self.name = "Receiver"
        # Senderソケットと同じ設定でReceiverスレッド用の新しいソケットを作成
        server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        server.bind(SOCK_FILE)
        server.listen()
        print(f"{current_thread().name}: Listening for incoming messages...")

        # Receiverスレッド用のソケットで接続を受け入れ、新しい接続とSenderのアドレスを返す
        conn, _ = server.accept()

        while True:
            data = conn.recv(BUFFER_SIZE)
            if not data:
                break
            message = data.decode()
            print(f"{current_thread().name}: Received: '{message}'")

        server.close()


def main() -> None:
    if os.path.exists(SOCK_FILE):
        os.remove(SOCK_FILE)

    receiver = Receiver()
    receiver.start()
    time.sleep(1)
    sender = Sender()
    sender.start()

    for thread in [receiver, sender]:
        thread.join()

    os.remove(SOCK_FILE)


if __name__ == "__main__":
    main()
