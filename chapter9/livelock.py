import time
from threading import Thread
from deadlock.lock_with_name import LockWithName

dumplings = 20


class Philosopher(Thread):
    def __init__(
        self, name: str, left_chopstick: LockWithName, right_chopstick: LockWithName
    ):
        super().__init__()
        self.name = name
        self.left_chopstick = left_chopstick
        self.right_chopstick = right_chopstick

    def run(self) -> None:
        global dumplings

        while dumplings > 0:
            # 哲学者が左の箸を取る。哲学者は2人いて、それぞれがテーブルから1本ずつ箸を取る
            self.left_chopstick.acquire()
            print(
                f"{self.left_chopstick.name} grabbed by {self.name} "
                f"now needs {self.right_chopstick.name}"
            )
            if self.right_chopstick.locked():
                print(
                    f"{self.name} cannot get the "
                    f"{self.right_chopstick.name} chopstick, "
                    f"politely concedes..."
                )
            else:
                self.right_chopstick.acquire()
                print(f"{self.right_chopstick.name} chopstick grabbed by {self.name}")
                dumplings -= 1
                print(f"{self.name} eats a dumpling. Dumplings left: {dumplings}")
                time.sleep(1)
                self.right_chopstick.release()
            self.left_chopstick.release()


if __name__ == "__main__":
    chopstick_a = LockWithName("chopstick_a")
    chopstick_b = LockWithName("chopstick_b")

    philosopher_1 = Philosopher("Philosopher #1", chopstick_a, chopstick_b)
    philosopher_2 = Philosopher("Philosopher #2", chopstick_b, chopstick_a)

    philosopher_1.start()
    philosopher_2.start()
