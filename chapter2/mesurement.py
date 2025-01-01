import subprocess
import time
import statistics
from typing import Tuple


def measure_execution_time(script_path: str, trials: int = 5) -> Tuple[float, float]:
    """
    指定した Python スクリプトを与えられた回数 (trials) 実行し、
    平均実行時間 (seconds) と分散を返す。
    """
    elapsed_times = []

    for _ in range(trials):
        start = time.perf_counter()
        # Python スクリプトをサブプロセスとして実行
        subprocess.run(["python3", script_path], check=True)
        end = time.perf_counter()

        elapsed = end - start
        elapsed_times.append(elapsed)

    # 平均と不偏分散（母分散なら pvariance を使う）
    mean_time = statistics.mean(elapsed_times)
    variance_time = statistics.pvariance(elapsed_times)

    return mean_time, variance_time


def main():
    # 計測したい Python スクリプトをリスト化
    # 実際に計測したいスクリプトファイルのパスに置き換えてください
    scripts = [
        "password_cracking_sequential.py",
        "password_cracking_sequential_refactor.py",
        "password_cracking_async.py",
        "password_cracking_parallel.py",
        "password_cracking_concurrency.py",
    ]
    trials = 10  # 実行回数

    for script in scripts:
        mean_time, variance_time = measure_execution_time(script, trials)
        print(f"Script: {script}")
        print(f"  実行回数: {trials}")
        print(f"  平均実行時間: {mean_time:.6f} 秒")
        print(f"  分散: {variance_time:.6f}\n")


if __name__ == "__main__":
    main()
