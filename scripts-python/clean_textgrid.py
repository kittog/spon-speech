#!/bin/python3
# -*- coding: utf-8 -*-

import tgt
import re
import glob
from pathlib import Path
import argparse


def clean_tier(tier):
    for ann in tier.annotations:
        label = ann.text
        # didascalies
        clean_label = re.sub("\[\w+\]", "", label)
        # pauses
        clean_label = re.sub("\++", "", clean_label)
        # mmm
        clean_label = re.sub("(m+h+)", "hm", clean_label)
        # clitiques
        clean_label = re.sub("c['] ", "ce", clean_label)
        clean_label = re.sub("j['] ", "je", clean_label)
        clean_label = re.sub("t['] ", "tu", clean_label)

        ann.text = clean_label


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('folder', type=str)  # path_to_folder
    parser.add_argument('output_folder', type=str, default="../TextGrid-clean")
    args = parser.parse_args()

    # process arg
    tg_files = glob.glob(args.folder + "/*.TextGrid")
    return args


def main():
    args = parse_args()
    tg_files = glob.glob(args.folder + "/*.TextGrid")

    for grid in tg_files:
        filename = Path(grid).stem
        tg = tgt.io.read_textgrid(grid)
        tiers = tg.tiers
        for i in range(len(tiers)):
            tier = tiers[i]
            clean_tier(tier)

        tgt.io.write_to_file(tg, f"{args.output_folder}/{filename}.TextGrid")


if __name__ == '__main__':
    main()