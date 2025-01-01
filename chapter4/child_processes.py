import os
from multiprocessing import Process


def run_child() -> None:
    print("Child: I am the child process")
    print(f"Child: Child's PID: {os.getpid()}")
    print(f"Child: Parent's PID: {os.getppid()}")


def start_parent(num_children: int) -> None:
    print("Parent: I am the parent process")
    print(f"Parent: Parent's PID: {os.getpid()}")

    # children = []

    for i in range(num_children):
        print(f"Starting Process {i}")
        child = Process(target=run_child)
        child.start()
        # children.append(child)
        # joinをすると親プロセスが子プロセスの終了を待つので、子プロセスをforで回していると直列になる。
        # コメントアウトしている処理を外すと、子プロセスのみで並列処理が行われる。
        # 親プロセスが先に終了してしまうと、子プロセスが孤児プロセスになるので、joinを使うことが一般的。
        # child.join()

    # for child in children:
    #     child.join()

    print("Parent: process exit")


if __name__ == "__main__":
    num_children = 3
    start_parent(num_children)
