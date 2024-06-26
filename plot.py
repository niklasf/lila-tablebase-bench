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
data = []

for i, line in enumerate(open(sys.argv[1])):
    fen, ms = line.split("\t")
    ms = int(ms)
    if i > 800_000 and (True or piece_count(fen) == 5):
        data.append(ms)
        groups[group(ms)] = groups.get(group(ms), 0) + 1

log_groups = {i: math.log(v) for i, v in groups.items()}
max_val = max(log_groups.values())
for i in range(30):
    val = log_groups.get(i, 0)
    width = round(val * 80 / max_val)
    print(str(i * GROUP_MS).rjust(5) + "ms", "=" * width, groups.get(i, 0))

print()
p = statistics.quantiles(data, n=1000, method="inclusive")
avg = statistics.fmean(data)
print(f"samples: {len(data)}  avg: {avg:.1f}  median: {p[500-1]:.1f}  p90: {p[900-1]:.1f}  p99: {p[990-1]:.1f}  p99.9: {p[999-1]:.1f}  max: {max(data):.1f}")
