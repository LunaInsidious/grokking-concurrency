import time
from queue import Queue
from threading import Thread

Washload = str


class Washer(Thread):
    def __init__(self, in_queue: Queue[Washload], out_queue: Queue[Washload]) -> None:
        super().__init__()
        self.in_queue = in_queue
        self.out_queue = out_queue

    def run(self) -> None:
        while True:
            # 前のステップから洗濯物を受け取る
            washload = self.in_queue.get()
            print(f"Washer: washing {washload}...")
            # 実際の作業をシミュレート
            time.sleep(4)
            # 洗濯物を次のステップに送る
            self.out_queue.put(washload)
            self.in_queue.task_done()


class Dryer(Thread):
    def __init__(self, in_queue: Queue[Washload], out_queue: Queue[Washload]) -> None:
        super().__init__()
        self.in_queue = in_queue
        self.out_queue = out_queue

    def run(self) -> None:
        while True:
            washload = self.in_queue.get()
            print(f"Dryer: drying {washload}...")
            time.sleep(2)
            self.out_queue.put(washload)
            self.in_queue.task_done()


class Folder(Thread):
    def __init__(self, in_queue: Queue[Washload]) -> None:
        super().__init__()
        self.in_queue = in_queue

    def run(self) -> None:
        while True:
            washload = self.in_queue.get()
            print(f"Folder: folding {washload}...")
            time.sleep(1)
            print(f"Folder: {washload} done!")
            self.in_queue.task_done()


class Pipeline:
    def assemble_laundry_for_washing(self) -> Queue[Washload]:
        washload_count = 4
        washloads_in: Queue[Washload] = Queue(washload_count)
        for washload_num in range(washload_count):
            washloads_in.put(f"Washload #{washload_num}")
        return washloads_in

    def run_concurrently(self) -> None:
        to_be_washed = self.assemble_laundry_for_washing()
        to_be_dried: Queue[Washload] = Queue()
        to_be_folded: Queue[Washload] = Queue()

        # 洗濯物のキューを組み立て、キューによってリンクされたスレッドを正しい順序で開始
        Washer(to_be_washed, to_be_dried).start()
        Dryer(to_be_dried, to_be_folded).start()
        Folder(to_be_folded).start()

        # キューに配置された選択物が全て処理されるまで待機
        to_be_washed.join()
        to_be_dried.join()
        to_be_folded.join()
        print("All done!")


if __name__ == "__main__":
    pipeline = Pipeline()
    pipeline.run_concurrently()
