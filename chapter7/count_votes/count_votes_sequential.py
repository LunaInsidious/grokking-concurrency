import typing as T
import random
import time

Summary = T.Mapping[int, int]


def process_votes(pile: T.List[int]) -> Summary:
    summary = {}
    for vote in pile:
        if vote in summary:
            summary[vote] += 1
        else:
            summary[vote] = 1
    return summary


if __name__ == "__main__":
    num_candidates = 3
    num_voters = 100000
    start_time = time.perf_counter()
    pile = [random.randint(1, num_candidates) for _ in range(num_voters)]
    counts = process_votes(pile)
    process_time = time.perf_counter() - start_time
    print(f"PROCESS TIME: {process_time}s")
    print(f"Total number of votes: {counts}")
