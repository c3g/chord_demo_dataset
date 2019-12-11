#!/usr/bin/env python3

import os
import subprocess

from divide_samples import datasets


CHROMOSOME_DIR = "/media/dlougheed/ITGENOME/demo_vcfs/ftp-trace.ncbi.nlm.nih.gov/1000genomes/ftp/release/20130502"

CHROMOSOME_FILES = [
    "ALL.chr1.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.vcf.gz",
    "ALL.chr2.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.vcf.gz",
    "ALL.chr3.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.vcf.gz",
    "ALL.chr4.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.vcf.gz",
    "ALL.chr5.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.vcf.gz",
    "ALL.chr6.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.vcf.gz",
    "ALL.chr7.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.vcf.gz",
    "ALL.chr8.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.vcf.gz",
    "ALL.chr9.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.vcf.gz",
    "ALL.chr10.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.vcf.gz",
    "ALL.chr11.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.vcf.gz",
    "ALL.chr12.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.vcf.gz",
    "ALL.chr13.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.vcf.gz",
    "ALL.chr14.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.vcf.gz",
    "ALL.chr15.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.vcf.gz",
    "ALL.chr16.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.vcf.gz",
    "ALL.chr17.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.vcf.gz",
    "ALL.chr18.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.vcf.gz",
    "ALL.chr19.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.vcf.gz",
    "ALL.chr20.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.vcf.gz",
    "ALL.chr21.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.vcf.gz",
    "ALL.chr22.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.vcf.gz",
    # "ALL.chrX.phase3_shapeit2_mvncall_integrated_v1b.20130502.genotypes.vcf.gz",
    # "ALL.chrY.phase3_integrated_v1b.20130502.genotypes.vcf.gz",
]

DATASETS_OUT = os.path.join(CHROMOSOME_DIR, "datasets")


for chr_f in CHROMOSOME_FILES:
    c = chr_f.split(".")[1]
    print(f"Chromosome: {c}")

    for i, d in enumerate(datasets):
        out_f = os.path.join(DATASETS_OUT, f"dataset_{i}_{c}.vcf.gz")
        cmd = f"bcftools view -s {','.join(d)} {os.path.join(CHROMOSOME_DIR, chr_f)} -c 1 -O z -o {out_f}"
        print(f"    {cmd}")
        subprocess.run(cmd, shell=True, check=True)
