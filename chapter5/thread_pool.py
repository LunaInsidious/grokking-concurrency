import time
import queue
import typing as T
from threading import Thread, current_thread

# 可変長引数を取り、Noneを返す
Callback = T.Callable[..., None]
Task = T.Tuple[Callback, T.Any, T.Any]
TaskQueue = queue.Queue


class Worker(Thread):
    def __init__(self, tasks: queue.Queue[Task]) -> None:
        super().__init__()
        self.tasks = tasks

    def run(self) -> None:
        while True:
            # ワーカースレッドがキューからタスクを取り出し、
            # タスクに関連付けられた関数を実行し、完了時にタスクに完了のマークを付ける。
            # この処理を延々と繰り返す。
            func, args, kargs = self.tasks.get()
            try:
                # *,**について: https://note.nkmk.me/python-args-kwargs-usage/
                func(*args, **kargs)
            except Exception as e:
                print(e)
            self.tasks.task_done()


class ThreadPool:
    def __init__(self, num_threads: int) -> None:
        # スレッドプールに送信されたタスクをキューに格納
        self.tasks: TaskQueue = queue.Queue(num_threads)
        self.num_threads = num_threads

        for _ in range(self.num_threads):
            # 複数のワーカースレッドを作成し、それらをデーモンモードに設定することで、
            # メインスレッドの終了時に自動的に終了させる。
            # 最後に、スレッドを開始して、キュー内のタスクの実行を開始できるようにする
            worker = Worker(self.tasks)
            worker.daemon = True
            worker.start()

    def submit(self, func: Callback, *args, **kargs) -> None:
        self.tasks.put((func, args, kargs))

    def wait_completion(self) -> None:
        # キューに配置されたタスクがすべて完了するまで、呼び出し元のスレッドをブロック
        self.tasks.join()


def cpu_waster(i: int) -> None:
    name = current_thread().name
    print(f"{name} doing {i} work")
    time.sleep(3)


def main() -> None:
    # ワーカースレッドが5つ含まれたスレッドプールを作成
    pool = ThreadPool(num_threads=5)
    for i in range(20):
        # スレッドプールに20個のタスクを送信
        pool.submit(cpu_waster, i)

    print("All work requests sent")
    pool.wait_completion()
    print("All work completed")


if __name__ == "__main__":
    main()
