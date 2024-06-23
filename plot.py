#!/usr/bin/env python3

import sys
import math
import statistics

GROUP_MS = 10

def group(ms):
    return ms // GROUP_MS

groups = {}

for line in open(sys.argv[1]):
    fen, ms = line.split("\t")
    ms = int(ms)
    groups[group(ms)] = groups.get(group(ms), 0) + 1

log_groups = {i: math.log(v) for i, v in groups.items()}

maximum = max(log_groups.values())

for i in range(30):
    val = log_groups.get(i, 0)
    width = round(val * 80 / maximum)
    print(str(i * GROUP_MS).rjust(5), "=" * width, groups.get(i, 0))

print()
q = statistics.quantiles(groups.values(), n=100)
print(f"median: {q[49]}  p90: {q[89]}  p99: {q[98]}  max: {max(groups.values())}")
