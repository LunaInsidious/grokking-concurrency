# これ並列化できるよ！の例
# 並列処理版(スレッドプール)
import hashlib
import math
import time
import typing as T
import os
from multiprocessing import Pool


ChunkRange = T.Tuple[int, int]


def get_chunks(num_ranges: int, length: int) -> T.Iterator[ChunkRange]:
    max_number = int(math.pow(10, length) - 1)
    chunk_starts = [int(max_number / num_ranges * i) for i in range(num_ranges)]
    chunk_ends = [start_point - 1 for start_point in chunk_starts[1:]] + [max_number]
    return zip(chunk_starts, chunk_ends)


def get_combinations(
    *, length: int, min_number: int = 0, max_number: T.Optional[int] = None
) -> T.List[str]:
    combinations = []
    if max_number is None:
        max_number = int(math.pow(10, length) - 1)
    for i in range(min_number, max_number + 1):
        str_num = str(i)
        zeros = "0" * (length - len(str_num))
        combinations.append("".join([zeros, str_num]))
    return combinations


def get_crypto_hash(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def check_password(expected_crypto_hash: str, possible_password: str) -> bool:
    actual_crypto_hash = get_crypto_hash(possible_password)
    return expected_crypto_hash == actual_crypto_hash


def crack_chunk(
    crypto_hash: str, length: int, chunk_start: int, chunk_end: int
) -> T.Union[str, None]:
    print(f"Processing {chunk_start} to {chunk_end}")
    combinations = get_combinations(
        length=length, min_number=chunk_start, max_number=chunk_end
    )
    for combination in combinations:
        if check_password(crypto_hash, combination):
            return combination
    return


def crack_password_parallel(crypto_hash: str, length: int) -> None:
    num_cores = os.cpu_count()
    print("Processing number combinations concurrently")
    start_time = time.perf_counter()

    # https://zenn.dev/k41531/articles/9c566a778b79ca
    with Pool() as pool:
        arguments = {
            (crypto_hash, length, chunk_start, chunk_end)
            for chunk_start, chunk_end in get_chunks(num_cores, length)
        }
        # https://qiita.com/uesseu/items/791d918c5a076a5b7265
        results = pool.starmap(crack_chunk, arguments)
        print("Waiting for chunks to finish")
        pool.close()
        pool.join()

    result = [res for res in results if res]
    print(f"PASSWORD CRACKED: {result[0]}")
    process_time = time.perf_counter() - start_time
    print(f"PROCESS TIME: {process_time}s")


if __name__ == "__main__":
    crypto_hash = "e24df920078c3dd4e7e8d2442f00e5c9ab2a231bb3918d65cc50906e49ecaef4"
    length = 8
    crack_password_parallel(crypto_hash, 8)
