#!/usr/bin/env python3

import sys
import math
import statistics

GROUP_MS = 50

def group(ms):
    return ms // GROUP_MS

def piece_count(fen):
    board, _ = fen.split(" ", 1)
    return sum((ch in "PNBRQKpnbrqk") for ch in board)

groups = {}

for line in open(sys.argv[1]):
    fen, ms = line.split("\t")
    ms = int(ms)
    if True or piece_count(fen) == 5:
        groups[group(ms)] = groups.get(group(ms), 0) + 1

log_groups = {i: math.log(v) for i, v in groups.items()}

maximum = max(log_groups.values())

for i in range(30):
    val = log_groups.get(i, 0)
    width = round(val * 80 / maximum)
    print(str(i * GROUP_MS).rjust(5) + "ms", "=" * width, groups.get(i, 0))

print()
q = statistics.quantiles(groups.values(), n=100)
print(f"median: {q[49]}  p90: {q[89]}  p99: {q[98]}  max: {max(groups.values())}")
