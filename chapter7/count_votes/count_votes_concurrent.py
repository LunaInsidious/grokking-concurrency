import typing as T
import random
import time
from multiprocessing.pool import ThreadPool

Summary = T.Mapping[int, int]


def process_votes(pile: T.List[int], worker_count: int = 4) -> Summary:
    vote_count = len(pile)
    vpw = vote_count // worker_count

    # votes per workerでスライスする
    vote_piles = [pile[i * vpw : (i + 1) * vpw] for i in range(worker_count)]

    with ThreadPool(worker_count) as pool:
        worker_summaries = pool.map(process_pile, vote_piles)

    total_summary = {}
    for worker_summary in worker_summaries:
        print(f"Votes from staff member: {worker_summary}")
        for candidate, count in worker_summary.items():
            if candidate in total_summary:
                total_summary[candidate] += count
            else:
                total_summary[candidate] = count

    return total_summary


def process_pile(pile: T.List[int]) -> Summary:
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
