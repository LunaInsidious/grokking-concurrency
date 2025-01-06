import typing as T
from threading import Thread, Event

from pacman import get_user_input, compute_game_world, render_next_screen

# 1つのプロセッサ/スレッド環境をシミュレート
processor_free = Event()
processor_free.set()


class Task(Thread):
    def __init__(self, func: T.Callable[..., None]) -> None:
        super().__init__()
        self.func = func

    def run(self) -> None:
        while True:
            # 内部フラグがtrueになるまで待機するが、プロセス中でsetを呼んでいないので、停止する。
            processor_free.wait()
            processor_free.clear()
            # 関数を独自の無限ループ内で実行。
            # このループはプログラムが停止するかスレッドが終了するまで継続的に実行される。
            self.func()


def arcade_machine() -> None:
    # 別々のスレッドでタスクを同時に定義して実行
    get_user_input_task = Task(get_user_input)
    compute_game_world_task = Task(compute_game_world)
    render_next_screen_task = Task(render_next_screen)

    # 1つめのスレッドから抜け出せない！
    get_user_input_task.start()
    compute_game_world_task.start()
    render_next_screen_task.start()


if __name__ == "__main__":
    arcade_machine()
