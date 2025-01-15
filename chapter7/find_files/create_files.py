import os
import random
import string


def generate_random_string(length) -> str:
    """
    指定された長さのランダムな文字列を生成する。
    文字列は英字、数字、記号から構成される。

    Args:
        length (int): ランダム文字列の長さ。

    Returns:
        str: ランダムな文字列。
    """
    characters = string.ascii_letters + string.digits + string.punctuation
    return "".join(random.choices(characters, k=length))


def create_files_with_random_content(directory, filenames, content_length) -> None:
    """
    指定したディレクトリにランダムな文字列を含むファイルを作成する。

    Args:
        directory (str): ファイルを作成するディレクトリのパス。
        filenames (list): 作成するファイル名のリスト。
        content_length (int): 各ファイルに書き込むランダム文字列の長さ。
    """
    # ディレクトリが存在しない場合は作成
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"ディレクトリを作成しました: {directory}")

    for filename in filenames:
        file_path = os.path.join(directory, filename)
        try:
            # ランダムな文字列を生成
            random_content = generate_random_string(content_length)

            # ファイルにランダム文字列を書き込み
            with open(file_path, "w") as f:
                f.write(random_content)
            print(f"ファイルを作成しました: {file_path} (内容: {content_length}文字)")
        except Exception as e:
            print(f"ファイルの作成に失敗しました: {file_path}. エラー: {e}")


# 使用例
if __name__ == "__main__":
    # 作成するディレクトリ
    target_directory = "./books"

    # ディレクトリ内のファイルを削除
    if os.path.exists(target_directory):
        for file in os.listdir(target_directory):
            file_path = os.path.join(target_directory, file)
            os.remove(file_path)
        os.rmdir(target_directory)

    # 各ファイルの内容に書き込むランダム文字列の長さ
    content_length = 5000

    # 作成するファイルの個数を指定
    file_count = input("作成するファイルの個数を入力してください: ")

    # 作成するファイル名のリスト
    file_names = []
    for i in range(int(file_count)):
        file_names.append(f"book_{i}.txt")

    create_files_with_random_content(target_directory, file_names, content_length)
