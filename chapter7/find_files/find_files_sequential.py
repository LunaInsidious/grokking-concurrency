import os
import time
import glob
import typing as T


def search_file(file_location: str, search_string: str) -> bool:
    with open(file_location, "r", encoding="utf8") as file:
        return search_string in file.read()


def search_files_sequentially(file_locations: T.List[str], search_string: str) -> None:
    for file_name in file_locations:
        result = search_file(file_name, search_string)
        if result:
            print(f"Found word in file: {file_name}")


if __name__ == "__main__":
    # 検索するファイルの場所からなるリストを作成
    file_locations = list(glob.glob(f"{os.path.abspath(os.getcwd())}/books/*.txt"))
    # ユーザーが入力した検索キーワードを取得
    search_string = input("What word are you trying to find?: ")

    start_time = time.perf_counter()
    search_files_sequentially(file_locations, search_string)
    process_time = time.perf_counter() - start_time
    print(f"PROCESS TIME: {process_time}")
