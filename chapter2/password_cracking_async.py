# これ並列化できるよ！の例
# 非同期処理版
# 早いが、chunk単位でやってることで答えの8765421にたどり着くのが早かっただけで根本の高速化はしていないと思われる。
import asyncio
import hashlib
import math
import time
import typing as T


def get_crypto_hash(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def check_password(expected_crypto_hash: str, possible_password: str) -> bool:
    actual_crypto_hash = get_crypto_hash(possible_password)
    return expected_crypto_hash == actual_crypto_hash


async def worker_check_range(
    crypto_hash: str, length: int, start: int, end: int
) -> T.Optional[str]:
    for i in range(start, end):
        str_num = str(i)
        zeros = "0" * (length - len(str_num))
        combination = zeros + str_num

        if check_password(crypto_hash, combination):
            return combination

        # CPU バウンド処理中にもイベントループに制御を戻すため
        # 適度に await でスリープさせる。
        # （実際には非常に細かい頻度だとオーバーヘッド増、逆に少ないとブロック時間増）
        if i % 1000 == 0:
            await asyncio.sleep(0)

    return None


def make_chunks(
    min_number: int, max_number: int, chunk_size: int
) -> T.List[T.Tuple[int, int]]:
    chunks = []
    for start in range(min_number, max_number + 1, chunk_size):
        end = min(start + chunk_size, max_number + 1)
        chunks.append((start, end))
    return chunks


async def get_valid_combinations_async(
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

    tasks = [
        asyncio.create_task(worker_check_range(crypto_hash, length, start, end))
        for (start, end) in chunk_ranges
    ]

    found_password: T.Optional[str] = None
    for coro in asyncio.as_completed(tasks):
        result = await coro
        if result is not None:
            found_password = result
            # パスワードが見つかったら、他タスクはキャンセル
            for t in tasks:
                t.cancel()
            break

    return found_password


async def crack_password_async(crypto_hash: str, password_length: int) -> None:
    print("Processing number combinations asynchronously...")
    start_time = time.perf_counter()

    found = await get_valid_combinations_async(
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
    crypto_hash = "e24df920078c3dd4e7e8d2442f00e5c9ab2a231bb3918d65cc50906e49ecaef4"
    length = 8
    asyncio.run(crack_password_async(crypto_hash, length))
