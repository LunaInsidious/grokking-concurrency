import time
from threading import Thread, current_thread

SIZE = 5
# サイズがSIZEの共有メモリを準備
shared_memory = [-1] * SIZE


# Thread クラスを継承し、run() メソッドに処理を実装する
class Producer(Thread):
    def run(self) -> None:
        self.name = "Producer"

        # 値の再代入を行う際にはglobal宣言をする
        # globalとローカルの区別がつかないため
        global shared_memory

        for i in range(SIZE):
            print(f"{current_thread().name}: Writing {int(i)}")
            # プロジューサースレッドが共有メモリにデータを書き込む
            shared_memory[i] = i


class Consumer(Thread):
    def run(self) -> None:
        self.name = "Consumer"

        for i in range(SIZE):
            # コンシューマースレッドが共有メモリから連続的にデータを読み取る。
            # データがまだ利用できない場合は待機
            while True:
                line = shared_memory[i]

                # -1 の場合はまだデータが書き込まれていないので、読み取りをリトライ
                if line == -1:
                    print(
                        f"{current_thread().name}: Data not available\n"
                        "Sleeping for 1 second before retrying"
                    )
                    time.sleep(1)
                    continue

                print(f"{current_thread().name}: Read: {int(line)}")
                break


def main() -> None:
    threads = [Consumer(), Producer()]

    # すべての子スレッドを開始
    for thread in threads:
        thread.start()

    # 全ての子スレッドが終了するのを待つ
    for thread in threads:
        thread.join()


if __name__ == "__main__":
    main()
