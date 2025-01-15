import time
from threading import Thread
from deadlock.lock_with_name import LockWithName

dumpings = 1000


class Philosopher(Thread):
    def __init__(
        self, name: str, left_chopstick: LockWithName, right_chopstick: LockWithName
    ):
        super().__init__()
        self.name = name
        self.left_chopstick = left_chopstick
        self.right_chopstick = right_chopstick

    def run(self) -> None:
        global dumpings

        # 変数dumplings_eatenは、この哲学者が食べた小籠包の数を追跡する
        dumplings_eaten = 0
        while dumpings > 0:
            self.left_chopstick.acquire()
            self.right_chopstick.acquire()
            if dumpings > 0:
                dumpings -= 1
                dumplings_eaten += 1
                time.sleep(1e-16)
            self.right_chopstick.release()
            self.left_chopstick.release()
        print(f"{self.name} took {dumplings_eaten} pieces")


if __name__ == "__main__":
    chopstick_a = LockWithName("chopstick_a")
    chopstick_b = LockWithName("chopstick_b")

    threads = []
    for i in range(10):
        threads.append(Philosopher(f"Philosopher #{i}", chopstick_a, chopstick_b))

    for t in threads:
        t.start()

    for t in threads:
        t.join()
