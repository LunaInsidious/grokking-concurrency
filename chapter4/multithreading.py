import os
import time
import threading
from threading import Thread


def cpu_waster(i: int) -> None:
    name = threading.current_thread().name
    print(f"{name} doing {i} work")
    time.sleep(3)
    print(f"{name} executed")


def display_threads() -> None:
    print("-" * 10)
    print(f"Current process PID: {os.getpid()}")
    print(f"Thread Count: {threading.active_count()}")
    print("Active threads")
    for thread in threading.enumerate():
        print(thread)


def main(num_threads: int) -> None:
    display_threads()

    print(f"Starting {num_threads} CPU wasters...")
    for i in range(num_threads):
        thread = Thread(target=cpu_waster, args=(i))
        thread.start()

    display_threads()
    print("main exit")


if __name__ == "__main__":
    num_threads = 5
    main(num_threads)
