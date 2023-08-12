#!/bin/python3
# -*- coding: utf-8 -*-

import argparse
import os
from praatio import textgrid
from pathlib import Path
from pydub import AudioSegment
import tgt


def create_textgrid(interval, filename, tier_name):
    tg_part = tgt.TextGrid()
    tier_part = tgt.IntervalTier(name=tier_name,
                                 start_time=interval.start_time,
                                 end_time=interval.end_time,
                                 objects=[interval])
    tg_part.add_tier(tier_part)
    tgt.write_to_file(tg_part,
                      f"../aligned/aligner-corpus/{tier_name}/{filename}.TextGrid")
    tg_part = textgrid.openTextgrid(f"../aligned/aligner-corpus/{tier_name}/{filename}.TextGrid", 
                                    includeEmptyIntervals=False)
    tg_part.save(f"../aligned/aligner-corpus/{tier_name}/{filename}.TextGrid",
                 format="long_textgrid", 
                 includeBlankSpaces=True)


def create_wave(wave, interval, filename, tier_name):
    start = interval.start_time
    end = interval.end_time
    new_wave = wave[start*1000:end*1000]
    new_wave.export(
        f"../aligned/aligner-corpus/{tier_name}/{filename}.wav",
        format="wav"
    )

# spe. webmaus
def create_txt(interval, filename, tier_name):
    text = interval.text  # label
    with open(f"../aligned/aligner-corpus/{tier_name}/{filename}.txt", "w") as f:
        f.write(text)


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
    # binary file (praat)
    tg = textgrid.openTextgrid(args.textgrid, includeEmptyIntervals=False)
    tg.save(args.textgrid, format="long_textgrid", includeBlankSpaces=True)
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
            #create_txt(intr, filename, tier.name)


if __name__ == '__main__':
    main()
