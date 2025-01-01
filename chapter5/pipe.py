from threading import Thread, current_thread
from multiprocessing import Pipe
from multiprocessing.connection import Connection


class Writer(Thread):
    def __init__(self, conn: Connection) -> None:
        super().__init__()
        self.conn = conn
        self.name = "Writer"

    def run(self) -> None:
        print(f"{current_thread().name}: Sending rubber duck...")
        # パイプにメッセージを書き込む
        self.conn.send("Rubber duck")


class Reader(Thread):
    def __init__(self, conn: Connection) -> None:
        super().__init__()
        self.conn = conn
        self.name = "Reader"

    def run(self) -> None:
        print(f"{current_thread().name}: Reading...")
        msg = self.conn.recv()
        print(f"{current_thread().name}: Received: {msg}")


def main() -> None:
    # 読み取り用と書き込み用の2つのパイプ接続を使って、
    # 2つのスレッドが通信するための名前なしパイプを作成
    reader_conn, writer_conn = Pipe()
    reader = Reader(reader_conn)
    writer = Writer(writer_conn)
    threads = [
        writer,
        reader,
    ]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()


if __name__ == "__main__":
    main()
