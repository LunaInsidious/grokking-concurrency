import sys
import time
from threading import Thread
import typing as T

from bank_account import BankAccount
from unsynced_bank_account import UnsyncedBankAccount
from synced_bank_account import SyncedBankAccount

THREAD_DELAY = 1e-16


class ATM(Thread):
    def __init__(self, bank_account: BankAccount):
        super().__init__()
        self.bank_account = bank_account

    def transaction(self) -> None:
        # 1回の取引は銀行口座からの連続した預入と引出で構成される
        self.bank_account.deposit(10)
        time.sleep(0.001)
        self.bank_account.withdraw(10)

    def run(self) -> None:
        self.transaction()


def test_atms(account: BankAccount, atm_number: int = 1000) -> None:
    atms: T.List[ATM] = []
    # 銀行講座で取引を同時に実行するATMスレッドをいくつか作成
    for _ in range(atm_number):
        atm = ATM(account)
        atms.append(atm)
        atm.start()

    # ATMスレッドの実行が完了するまで待機
    for atm in atms:
        atm.join()


if __name__ == "__main__":
    atm_number = 1000
    # コンテキストの切り替えによって処理が中断される可能性が大幅に高まるため、同期を効果的にテスト
    sys.setswitchinterval(THREAD_DELAY)

    account = UnsyncedBankAccount()
    test_atms(account, atm_number)

    print("Balance of unsynced account after concurrent transactions:")
    print(f"Actual: {account.balance}\nExpected: 0")

    account = SyncedBankAccount()
    test_atms(account, atm_number)

    print("Balance of synced account after concurrent transactions:")
    print(f"Actual: {account.balance}\nExpected: 0")
