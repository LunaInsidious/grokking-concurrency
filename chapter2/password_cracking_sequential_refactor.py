# これ並列化できるよ！の例
# 一旦計算量改善
import hashlib
import math
import time
import typing as T


def get_crypto_hash(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def check_password(expected_crypto_hash: str, possible_password: str) -> bool:
    actual_crypto_hash = get_crypto_hash(possible_password)
    return expected_crypto_hash == actual_crypto_hash


def get_valid_combinations(
    *,
    length: int,
    crypto_hash: str,
    min_number: int = 0,
    max_number: T.Optional[int] = None,
) -> T.List[str]:
    if max_number is None:
        max_number = int(math.pow(10, length) - 1)
    for i in range(min_number, max_number + 1):
        str_num = str(i)
        zeros = "0" * (length - len(str_num))
        combination = "".join([zeros, str_num])
        if check_password(crypto_hash, combination):
            print(f"PASSWORD CRACKED: {combination}")
            return combination
    return None


def crack_password(crypto_hash: str, password_length: int) -> None:
    print("Processing number combinations sequentially")
    start_time = time.perf_counter()
    get_valid_combinations(length=password_length, crypto_hash=crypto_hash)

    process_time = time.perf_counter() - start_time
    print(f"PROCESS TIME: {process_time}s")


if __name__ == "__main__":
    crypto_hash = "e24df920078c3dd4e7e8d2442f00e5c9ab2a231bb3918d65cc50906e49ecaef4"
    length = 8
    crack_password(crypto_hash, 8)
