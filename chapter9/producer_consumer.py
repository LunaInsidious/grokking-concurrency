import time
from threading import Thread, Semaphore, Lock

SIZE = 5
# 共有バッファ
BUFFER = ["" for _ in range(SIZE)]
producer_idx: int = 0

mutex = Lock()
empty = Semaphore(SIZE)
full = Semaphore(0)


class Producer(Thread):
    def __init__(self, name: str, maximum_items: int = 5):
        super().__init__()
        self.counter = 0
        self.name = name
        self.maximum_items = maximum_items

    def next_index(self, index: int) -> int:
        return (index + 1) % SIZE

    def run(self) -> None:
        global producer_idx
        while self.counter < self.maximum_items:
            # バッファに空きスロットが少なくとも1つある
            empty.acquire()
            # 共有バッファを変更するクリティカルセクションに入る
            mutex.acquire()
            self.counter += 1
            BUFFER[producer_idx] = f"{self.name}-{self.counter}"
            print(
                f"{self.name} produced: "
                f"'{BUFFER[producer_idx]}' into slot {producer_idx}"
            )
            producer_idx = self.next_index(producer_idx)
            mutex.release()
            # バッファに新しいアイテムが追加され、空きスロットが1つ減る
            full.release()
            time.sleep(1)


class Consumer(Thread):
    def __init__(self, name: str, maximum_items: int = 10):
        super().__init__()
        self.name = name
        self.idx = 0
        self.counter = 0
        self.maximum_items = maximum_items

    # 消費する次のバッファインデックスを取得
    def next_index(self) -> int:
        return (self.idx + 1) % SIZE

    def run(self) -> None:
        while self.counter < self.maximum_items:
            # バッファに消費可能なアイテムが少なくとも1つある
            full.acquire()
            # 共有バッファを変更するクリティカルセクションに入る
            mutex.acquire()
            item = BUFFER[self.idx]
            print(f"{self.name} consumed: '{item}' from slot {self.idx}")
            self.idx = self.next_index()
            self.counter += 1
            mutex.release()
            # アイテムが消費された後、バッファに新しい空きスロットができる
            empty.release()
            time.sleep(2)


if __name__ == "__main__":
    threads = [Producer("SpongeBob"), Producer("Patrick"), Consumer("Squidward")]

    for t in threads:
        t.start()

    for t in threads:
        t.join()
