import gzip
import itertools
import numpy as np
from pathlib import Path

alphabet = ["G", "A", "T", "C"]
all_kmers = np.array([''.join(p) for p in itertools.product(alphabet, repeat=10)], dtype=('str', 10))


Path("test").mkdir(exist_ok=True)
for i in range(10):
    with gzip.open(f"test/sample{i}.txt.gz", "wt") as f:
        for kmer in np.random.choice(all_kmers, size=100000, replace=False):
            f.write(kmer + "\n")
