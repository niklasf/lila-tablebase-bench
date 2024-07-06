# lila-tablebase benchmark suite and results

For Lichess's tablebase server
[lila-tablebase](https://github.com/lichess-org/lila-tablebase).

Also see https://lichess.org/@/revoof/blog/optimizing-the-tablebase-server/MetV0ZQd

## Run benchmarks

```bash
unzstd fens.txt.zst
RAYON_NUM_THREADS=12 cargo run --release -- fens.txt | tee results.tsv
```

## `fens.txt`

1 million tablebase requests recorded in production. Sample:

```
1Q6/3kr3/8/3K4/8/8/8/8 b - - 1 1
8/3k4/3B4/3BK3/8/8/8/8 w - - 26 14
8/8/3k1Q2/8/8/3NK3/8/8 b - - 1 1
8/8/8/8/8/2K5/8/3k4 w - - 0 13
8/8/2Pr3k/p3P3/8/8/2K1B3/8 w - - 0 1
```

## `results`

FEN, tab, response time in milliseconds. Sample:

```
8/1R4k1/r7/5KPP/8/8/8/8 b - - 2 55	0
8/1R3k1p/5b2/4pK2/4P3/7P/8/8 b - - 5 57	0
8/2K5/3P4/2k2b2/8/8/6B1/8 w - - 20 11	1
8/8/4k3/4Pn1p/8/1K6/8/q7 w - - 0 42	0
```

* `pread`/`mmap`/`parallel-pread`: I/O method as described in blog
* `normal`/`random`: `PPOSIX_FADV_NORMAL`/`POSIX_FADV_RANDOM` or equivalent
* `no-prefix`/`hot-prefix`/`hot-prefix2`: Unused SSD, RAID 1 with many table prefixes, RAID 0 with all table prefixes

## License

CC0
