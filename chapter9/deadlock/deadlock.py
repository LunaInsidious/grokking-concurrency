import time
from threading import Thread

from lock_with_name import LockWithName

dumplings = 20


class Philosopher(Thread):
    def __init__(
        self, name: str, left_chopstick: LockWithName, right_chopstick: LockWithName
    ):
        super().__init__()
        self.name = name
        # それぞれの哲学者に、左に1本、右に1本の合計2本の橋を関連付ける
        self.left_chopstick = left_chopstick
        self.right_chopstick = right_chopstick

    def run(self) -> None:
        global dumplings

        # 小籠包が無くなるまで食事をする
        while dumplings > 0:
            # 左の橋を手に取る
            self.left_chopstick.acquire()
            print(
                f"{self.left_chopstick.name} grabbed by {self.name} "
                f"now needs {self.right_chopstick.name}"
            )
            # 右の橋を手に取る
            self.right_chopstick.acquire()
            print(f"{self.right_chopstick.name} grabbed by {self.name}")
            # 小籠包が1つ減る
            dumplings -= 1
            print(f"{self.name} eats a dumpling. " f"Dumplings left: {dumplings}")
            # 右の橋を置く
            self.right_chopstick.release()
            print(f"{self.right_chopstick.name} released by {self.name}")
            # 左の橋を置く
            self.left_chopstick.release()
            print(f"{self.left_chopstick.name} released by {self.name}")
            print(f"{self.name} is thinking...")
            time.sleep(0.1)


if __name__ == "__main__":
    chopstick_a = LockWithName("chopstick_a")
    chopstick_b = LockWithName("chopstick_b")

    philosopher_1 = Philosopher("Philosopher #1", chopstick_a, chopstick_b)
    philosopher_2 = Philosopher("Philosopher #2", chopstick_b, chopstick_a)

    philosopher_1.start()
    philosopher_2.start()
