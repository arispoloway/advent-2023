import time
from contextlib import contextmanager

@contextmanager
def timer(name):
    print(name)
    start_time = time.time()
    try:
        yield
    finally:
        print(f'time taken: {time.time() - start_time:0.3f}s\n')

start_time = time.time()
with timer("all"):
    with timer("day01"):
        import solutions.day01.main
    with timer("day02"):
        import solutions.day02.main
    with timer("day03"):
        import solutions.day03.main
    with timer("day04"):
        import solutions.day04.main
    with timer("day05"):
        import solutions.day05.main
    with timer("day06"):
        import solutions.day06.main
    with timer("day07"):
        import solutions.day07.main
    with timer("day08"):
        import solutions.day08.main
    with timer("day09"):
        import solutions.day09.main
    with timer("day10"):
        import solutions.day10.main
    with timer("day11"):
        import solutions.day11.main
    with timer("day12"):
        import solutions.day12.main
    with timer("day13"):
        import solutions.day13.main
    with timer("day14"):
        import solutions.day14.main
    with timer("day15"):
        import solutions.day15.main
    with timer("day16"):
        import solutions.day16.main
    with timer("day17"):
        import solutions.day17.main
    with timer("day18"):
        import solutions.day18.main
    with timer("day19"):
        import solutions.day19.main
    with timer("day20"):
        import solutions.day20.main
    with timer("day21"):
        import solutions.day21.main
    with timer("day22"):
        import solutions.day22.main
    with timer("day23"):
        import solutions.day23.main
    with timer("day24"):
        import solutions.day24.main
    with timer("day25"):
        import solutions.day25.main
