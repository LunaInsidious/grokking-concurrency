# これ並列化できるよ！の例
# 並行処理版
# 非同期より遅いが、今回のケースが向いていないだけであると思われる。
import math
import time
import typing as T
import hashlib
import concurrent.futures


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


def get_valid_combinations(
    *,
    length: int,
    crypto_hash: str,
    min_number: int = 0,
    max_number: T.Optional[int] = None,
    chunk_size: int = 50_000,
) -> T.Optional[str]:
    if max_number is None:
        max_number = int(math.pow(10, length)) - 1

    chunk_ranges = make_chunks(min_number, max_number, chunk_size)

    found_password: T.Optional[str] = None

    # スレッドプールを使って並行（厳密には擬似的に並行）処理
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(worker_check_range, crypto_hash, length, start, end)
            for (start, end) in chunk_ranges
        ]

        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result is not None:
                found_password = result
                for f in futures:
                    f.cancel()
                break

    return found_password


def crack_password(crypto_hash: str, password_length: int) -> None:
    print("Processing number combinations concurrently (ThreadPoolExecutor)...")
    start_time = time.perf_counter()

    found = get_valid_combinations(
        length=password_length,
        crypto_hash=crypto_hash,
    )

    process_time = time.perf_counter() - start_time
    if found:
        print(f"PASSWORD CRACKED: {found}")
    else:
        print("PASSWORD NOT FOUND")
    print(f"PROCESS TIME: {process_time}s")


if __name__ == "__main__":
    test_crypto_hash = (
        "e24df920078c3dd4e7e8d2442f00e5c9ab2a231bb3918d65cc50906e49ecaef4"
    )
    length = 8

    crack_password(test_crypto_hash, length)
