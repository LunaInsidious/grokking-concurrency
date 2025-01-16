import time
import random
from threading import Thread
from rwlock import RWLock

counter = 0
lock = RWLock()


class User(Thread):
    def __init__(self, idx: int):
        super().__init__()
        self.idx = idx

    def run(self) -> None:
        while True:
            lock.acquire_read()
            print(f"User {self.idx} reading: {counter}")
            time.sleep(random.randrange(1, 3))
            lock.release_read()
            time.sleep(0.5)


class Librarian(Thread):
    def run(self) -> None:
        global counter
        while True:
            lock.acquire_write()
            print("Librarian writing...")
            counter += 1
            print(f"New value: {counter}")
            time.sleep(random.randrange(1, 3))
            lock.release_write()


if __name__ == "__main__":
    threads = [User(0), User(1), Librarian()]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()
