import typing as T
import time
import random
from threading import Thread, Semaphore, Lock

TOTAL_SPOTS = 3


class Garage:
    def __init__(self) -> None:
        # セマフォは駐車場の空いている駐車スペースの数を制御
        self.semaphore = Semaphore(TOTAL_SPOTS)
        # 駐車場ん車のリストを変更できるのは一度に1つのスレッドだけ
        self.cars_lock = Lock()
        self.parked_cars: T.List[str] = []

    def count_parked_cars(self) -> int:
        return len(self.parked_cars)

    def enter(self, car_name: str) -> None:
        self.semaphore.acquire()
        self.cars_lock.acquire()
        self.parked_cars.append(car_name)
        print(f"{car_name} parked")
        self.cars_lock.release()

    def exit(self, car_name: str) -> None:
        self.cars_lock.acquire()
        self.parked_cars.remove(car_name)
        print(f"{car_name} leaving")
        self.cars_lock.release()
        self.semaphore.release()


def park_car(garage: Garage, car_name: str) -> None:
    garage.enter(car_name)
    time.sleep(random.uniform(1, 2))
    garage.exit(car_name)


def test_garage(garage: Garage, number_of_cars: int = 10) -> None:
    threads = []
    for car_num in range(number_of_cars):
        t = Thread(target=park_car, args=(garage, f"Car #{car_num}"))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()


if __name__ == "__main__":
    number_of_cars = 10
    garage = Garage()
    test_garage(garage, number_of_cars)

    print("Number of parked cars after a busy day:")
    print(f"Actual: {garage.count_parked_cars()}\nExpected: 0")
