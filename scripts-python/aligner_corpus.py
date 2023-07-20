#!/bin/python3
# -*- coding: utf-8 -*-

import argparse
import glob
import os
from pathlib import Path
from pydub import AudioSegment
import tgt

def create_textgrid():
    pass

def create_wave(wave, interval, filename, tier.name):
    start = interval.start_time
    end = interval.end_time
    new_wave = wave[start*1000:end*1000]
    new_wave.export(
        f"../aligned/aligner-corpus/{tier.name}/{filename}",
        format="wav"
    )

# spe. webmaus
def create_txt():
    pass

def create_output_folder(tg):
    # output folder path
    output_folder = "../aligned/aligner-corpus"
    # format speaker name
    tiers = tg.tiers
    for tier in tiers:
        if os.path.isdir(f"{output_folder}/{tier.name}") == False:
            os.mkdir(f"{output_folder}/{tier.name}")


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-tg', '--textgrid', type=str)  # textgrid file
    parser.add_argument('-w', '--wave', type=str)  # wave file
    args = parser.parse_args()
    return args


def main():
    # process args
    args = parse_args()
    # open files
    tg = tgt.io.read_textgrid(args.textgrid)
    wav = AudioSegment.from_file(args.wave)
    # create output folder
    create_output_folder(tg)
    # segment into files
    tiers = tg.tiers
    for itier in range(len(tiers)):
        tier = tiers[itier]
        # format speaker name
        speaker = "_".join(tier.name.split())
        for intr in tier.annotations:
            # format filename
            filename = f"{speaker}_{round(intr.start_time, 3)}_{round(intr.end_time, 3)}"
            # create textgrid
            create_textgrid(intr, filename, tier.name)
            # create wave
            create_wave(wav, intr, filename, tier.name)
            # create txt


if __name__ == '__main__':
    main()
