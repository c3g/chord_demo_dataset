#!/usr/bin/env python3

datasets = (
    ["NA19648"],  # Female with breast cancer
    ["NA19658"],  # Male 1 with BRCA1 variant
    ["NA20509"],  # Male 2 with BRCA1 variant
)

with open("./samples.tsv", "r") as sf:
    i = 0
    for s in sf.readlines():
        if s in ("NA19648", "NA19658", "NA20509"):
            continue

        sample = s.split("\t")[0]
        datasets[i].append(sample)

        i = (i + 1) % 3

if __name__ == "__main__":
    print(datasets)
