# これ並列化できるよ！の例
# 並列処理版
import hashlib
import math
import time
import typing as T
from concurrent.futures import ProcessPoolExecutor, as_completed


def get_crypto_hash(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def check_password(expected_crypto_hash: str, possible_password: str) -> bool:
    actual_crypto_hash = get_crypto_hash(possible_password)
    return expected_crypto_hash == actual_crypto_hash


def worker_check_range(
    crypto_hash: str, length: int, start: int, end: int
) -> T.Optional[str]:
    for i in range(start, end):
        str_num = str(i)
        zeros = "0" * (length - len(str_num))
        combination = zeros + str_num

        if check_password(crypto_hash, combination):
            return combination

    return None


def make_chunks(
    min_number: int, max_number: int, chunk_size: int
) -> T.List[T.Tuple[int, int]]:
    chunks = []
    for start in range(min_number, max_number + 1, chunk_size):
        end = min(start + chunk_size, max_number + 1)
        chunks.append((start, end))
    return chunks


def get_valid_combinations_parallel(
    *,
    length: int,
    crypto_hash: str,
    min_number: int = 0,
    max_number: T.Optional[int] = None,
    chunk_size: int = 10_000,
) -> T.Optional[str]:
    if max_number is None:
        max_number = int(math.pow(10, length)) - 1

    chunk_ranges = make_chunks(min_number, max_number, chunk_size)

    found_password: T.Optional[str] = None

    # プロセスプールを使って並列実行
    with ProcessPoolExecutor() as executor:
        futures = [
            executor.submit(worker_check_range, crypto_hash, length, start, end)
            for (start, end) in chunk_ranges
        ]
        for future in as_completed(futures):
            result = future.result()
            if result is not None:
                found_password = result
                for f in futures:
                    f.cancel()
                break

    return found_password


def crack_password_parallel(crypto_hash: str, password_length: int) -> None:
    print("Processing number combinations in parallel using ProcessPoolExecutor...")
    start_time = time.perf_counter()

    found = get_valid_combinations_parallel(
        length=password_length,
        crypto_hash=crypto_hash,
    )

    process_time = time.perf_counter() - start_time
    if found:
        print(f"PASSWORD CRACKED: {found}")
    else:
        print("PASSWORD NOT FOUND")
    print(f"PROCESS TIME: {process_time:.3f}s")


if __name__ == "__main__":
    crypto_hash = "e24df920078c3dd4e7e8d2442f00e5c9ab2a231bb3918d65cc50906e49ecaef4"
    length = 8
    crack_password_parallel(crypto_hash, length)
