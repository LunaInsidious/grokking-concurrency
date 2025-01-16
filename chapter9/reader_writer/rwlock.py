from threading import Lock


class RWLock:
    def __init__(self) -> None:
        self.readers = 0
        self.read_lock = Lock()
        self.write_lock = Lock()

    # 現在のスレッドの読み取りロックをを獲得
    # ライターがロックを待っている場合は、ライターがロックを解放するまでブロックされる
    def acquire_read(self) -> None:
        self.read_lock.acquire()
        self.readers += 1
        if self.readers == 1:
            self.write_lock.acquire()
        self.read_lock.release()

    # 現在のスレッドが所有している読み取りロックを解放
    # ロックを所有しているリーダーが無くなったら、書き込みロックを解放
    def release_read(self) -> None:
        assert self.readers >= 1
        self.read_lock.acquire()
        self.readers -= 1
        if self.readers == 0:
            self.write_lock.release()
        self.read_lock.release()

    # 現在のスレッドの書き込みロックを獲得
    # リーダーまたはライターがロックを所有している場合は、ロックが解放されるまでブロック
    def acquire_write(self) -> None:
        self.write_lock.acquire()

    # 現在のスレッドが所有している空きこみロックを解放
    def release_write(self) -> None:
        self.write_lock.release()
