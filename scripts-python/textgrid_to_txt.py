#!/bin/python3
# -*- coding: utf-8 -*-

import argparse
import glob
import os
from pathlib import Path
from pydub import AudioSegment
import tgt
from praatio import textgrid
from praatio import audio

def create_textgrid(interval, tier, speaker, filename):
    tg_cut = tgt.core.TextGrid() # new textgrid

    # create tier
    tier_part = tgt.IntervalTier(
        name=tier.name,
        start_time=tier.start_time,
        end_time=tier.end_time,
        objects=interval)
    # add tier to new textgrid
    tg_cut.add_tier(tier_part)

    # save textgrid
    tgt.io.write_to_file(tg_cut, f"../corpus-cut/TextGrid-cut/{speaker}/{filename}.TextGrid")

def create_wave(interval, speaker, filename):
    # wave
    newWave = wave[entry.start*1000:entry.end*1000]
    newWave.export(
        f"../corpus-cut/waves-cut/{filename}/{new_filename}.wav", format="wav")

def label_to_txt(path_to_textgrid, folder):
    # extract label from textgrid and save to text file
    tg = tgt.io.read_textgrid(path_to_textgrid)
    filename = Path(path_to_textgrid).stem
    txt = open(f"../corpus-cut/txt-cut/{folder}/{filename}.txt", "w")
    tiers = tg.tierNames
    # technically only one remains !
    for itier in range(len(tiers)):
        tier = tg.getTier(tiers[itier])
        for ientry in range(len(tier.entries)):
            entry = tier.entries[ientry]
            label = entry.label
            txt.write(label)
            txt.write("\n")
        txt.close()

def divide_and_write(textgrid, wave):
    tg = tgt.io.read_textgrid(textgrid)
    wav = AudioSegment.from_file(wave)
    # create new directories
    filename = Path(textgrid).stem
    is_tg = os.path.isdir(f"../corpus-cut/TextGrid-cut/{filename}")
    is_w = os.path.isdir(f"../corpus-cut/waves-cut/{filename}")
    if is_tg + is_w == 0:
        os.mkdir(f"../corpus-cut/TextGrid-cut/{filename}")
        os.mkdir(f"../corpus-cut/waves-cut/{filename}")
        # os.mkdir(f"../corpus-cut/txt-cut/{filename}")
    # get tiers
    tiers = tg.tiers
    for itier in range(len(tiers)):
        tier = tiers[itier]
        # format speaker name
        speaker = "_".join(tier.name.split())
        for ientry in range(len(tier.annotations)):
            # format filename
            new_filename = f"{speaker}_{round(tier.start_time,3)}_{round(tier.end_time,3)}"
            # get interval
            intr = tier.annotations[ientry] # n-th annotation object
            print(type(intr))
            print(intr)
            print(intr.start_time)
            create_textgrid(intr, tier, speaker, new_filename)


            # cut
            # divide(entry, wave, filename, new_filename, tier)

            # label_to_txt
            # label_to_txt(f"../corpus-cut/TextGrid-cut/{filename}/{new_filename}.TextGrid", filename)

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-tg', '--textgrid', type=str) # input textgrid file
    parser.add_argument('-w', '--wave', type=str) # input wave file
    args = parser.parse_args()
    return args

def main():
    args = parse_args()
    divide_and_write(args.textgrid, args.wave)

if __name__ == '__main__':
    main()