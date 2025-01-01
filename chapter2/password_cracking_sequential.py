# これ並列化できるよ！の例
import hashlib
import math
import time
import typing as T


# *:=キーワード引数(https://qiita.com/junkoda/items/bfd35793c5cd33c600bc)
def get_combinations(
    *, length: int, min_number: int = 0, max_number: T.Optional[int] = None
) -> T.List[str]:
    combinations = []
    if max_number is None:
        max_number = int(math.pow(10, length) - 1)
    # 指定された範囲で、指定された桁数の、考えられる限りのパスワードのリストを生成
    # パスワードは、半角数字のみであることを想定
    for i in range(min_number, max_number + 1):
        str_num = str(i)
        zeros = "0" * (length - len(str_num))
        combinations.append("".join([zeros, str_num]))
    return combinations


def get_crypto_hash(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def check_password(expected_crypto_hash: str, possible_password: str) -> bool:
    # 考えられる限りのパスワードの暗号学的ハッシュ値をシステムに格納されているものと比較
    actual_crypto_hash = get_crypto_hash(possible_password)
    return expected_crypto_hash == actual_crypto_hash


def crack_password(crypto_hash: str, password_length: int) -> None:
    print("Processing number combinations sequentially")
    start_time = time.perf_counter()
    combinations = get_combinations(length=password_length)
    for combination in combinations:
        if check_password(crypto_hash, combination):
            print(f"PASSWORD CRACKED: {combination}")
            break

    process_time = time.perf_counter() - start_time
    print(f"PROCESS TIME: {process_time}s")


if __name__ == "__main__":
    crypto_hash = "e24df920078c3dd4e7e8d2442f00e5c9ab2a231bb3918d65cc50906e49ecaef4"
    length = 8
    crack_password(crypto_hash, 8)
