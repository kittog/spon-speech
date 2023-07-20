#!/bin/python3
# -*- coding: utf-8 -*-
import argparse
import tgt
from praatio import textgrid
from pathlib import Path


def overlaps(textgrid):
    tiers = textgrid.tiers
    for i in range(len(tiers)-1):
        tier = tiers[i]
        over = tgt.util.get_overlapping_intervals(tiers[i], tiers[i+1])
        for j in range(len(over)):
            start = over[j].start_time
            end = over[j].end_time
            tier.delete_annotations_between_timepoints(
                start, end, left_overlap=True, right_overlap=True)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('input', type=str)  # input file
    parser.add_argument('output', type=str)  # output folder
    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    filename = Path(args.input).stem
    tg = tgt.io.read_textgrid(args.input)
    overlaps(tg)
    tgt.io.write_to_file(tg, f"{args.output}/{filename}")


if __name__ == '__main__':
    main()
