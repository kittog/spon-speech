#!/bin/python3
# -*- coding: utf-8 -*-

import argparse
import sys
import os
import glob

from praatio import textgrid
import tgt

def overlap(tiers):
    for i in range(len(tiers) - 1):
        over = tgt.util.get_overlapping_intervals(tiers[i], tiers[i+1])

        tier = tiers[i]
        for j in range(len(over)):
            start = over[j].start_time
            end = over[j].end_time
            # del nth overlap
            tier.delete_annotations_between_timepoints(start, end, left_overlap=True, right_overlap=True)
    

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--folder', type=str)
    args = parser.parse_args()
    return args

def main():
    path_to_folder = parse_args()
    path_to_files = glob.glob(path_to_folder + "/" + "*.TextGrid")
    for f in path_to_files:
        # binary format
        tg = textgrid.openTextgrid(f, False)
        tg.save(f, format="long_textgrid", includeBlankSpaces=True)

        tg = tgt.io.read_textgrid(f)

        tiers = tg.tiers
        overlap(tiers)

        tgt.io.write_to_file(tg, f, format="TextGrid")
    

if __name__ == '__main__':
    main()