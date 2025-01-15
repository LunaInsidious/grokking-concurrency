import time
from threading import Thread, Lock
from lock_with_name import LockWithName

dumplings = 20


class Waiter:
    def __init__(self) -> None:
        self.mutex = Lock()

    def ask_for_chopsticks(
        self, left_chopsticks: LockWithName, right_chopsticks: LockWithName
    ) -> None:
        # クリティカルセクションを保護するための内部ミューテックス。
        # 一度に1つのスレッドだけがアクセスできるようにする
        with self.mutex:
            # 箸の獲得と解放を管理するのはウェイター
            left_chopsticks.acquire()
            print(f"{left_chopsticks.name} grabbed")
            right_chopsticks.acquire()
            print(f"{right_chopsticks.name} grabbed")

    def release_chopsticks(
        self, left_chopsticks: LockWithName, right_chopsticks: LockWithName
    ) -> None:
        right_chopsticks.release()
        print(f"{right_chopsticks.name} released")
        left_chopsticks.release()
        print(f"{left_chopsticks.name} released\n")


class Philosopher(Thread):
    def __init__(
        self,
        name: str,
        left_chopstick: LockWithName,
        right_chopstick: LockWithName,
        waiter: Waiter,
    ):
        super().__init__()
        self.name = name
        self.left_chopstick = left_chopstick
        self.right_chopstick = right_chopstick
        self.waiter = waiter

    def run(self) -> None:
        global dumplings

        while dumplings > 0:
            print(f"{self.name} asks waiter for chopsticks")
            # 哲学者がウェイターに箸を要求
            self.waiter.ask_for_chopsticks(self.left_chopstick, self.right_chopstick)
            dumplings -= 1
            print(f"{self.name} eats a dumpling. Dumplings left: {dumplings}")
            print(f"{self.name} returns chopsticks to waiter")
            # 哲学者は食べ終えるとウェイターに箸を返す
            self.waiter.release_chopsticks(self.left_chopstick, self.right_chopstick)
            time.sleep(0.1)


if __name__ == "__main__":
    chopstick_a = LockWithName("chopstick_a")
    chopstick_b = LockWithName("chopstick_b")

    waiter = Waiter()

    philosopher_1 = Philosopher("Philosopher #1", chopstick_a, chopstick_b, waiter)
    philosopher_2 = Philosopher("Philosopher #2", chopstick_b, chopstick_a, waiter)

    philosopher_1.start()
    philosopher_2.start()
