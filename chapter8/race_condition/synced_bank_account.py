from threading import Lock
from unsynced_bank_account import UnsyncedBankAccount


class SyncedBankAccount(UnsyncedBankAccount):
    def __init__(self, balance: float = 0):
        super().__init__(balance)
        self.mutex = Lock()

    def deposit(self, amount: float) -> None:
        # 共有リソースのミューテックスを取得。
        # これにより、ミューテックスを獲得している1つのスレッドだけが実行可能状態になる
        self.mutex.acquire()
        super().deposit(amount)
        # ミューテックスを解放
        self.mutex.release()

    def withdraw(self, amount: float) -> None:
        self.mutex.acquire()
        super().withdraw(amount)
        self.mutex.release()
