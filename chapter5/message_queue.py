import time
from queue import Queue
from threading import Thread, current_thread


class Worker(Thread):
    def __init__(self, queue: Queue, id: int) -> None:
        super().__init__(name=str(id))
        self.queue = queue

    def run(self) -> None:
        while not self.queue.empty():
            # 次に処理するアイテムをキューから取り出す。
            # このメソッドはキューにアイテムが配置されるまでブロックされる。
            item = self.queue.get()
            print(
                f"Thread {current_thread().name}: "
                f"processing item {item} from the queue"
            )
            time.sleep(2)


def main(thread_num: int) -> None:
    # スレッドで処理するための値が配置されるキューを作成
    q = Queue()
    for i in range(10):
        q.put(i)

    threads = []
    for i in range(thread_num):
        thread = Worker(q, i + 1)
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()


if __name__ == "__main__":
    thread_num = 4
    main(thread_num)
