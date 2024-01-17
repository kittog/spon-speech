#!/bin/python3
# -*- coding: utf-8 -*-

import glob
import os
import argparse
from pathlib import Path
from pydub import AudioSegment
from praatio import textgrid
from praatio.utilities.constants import Interval

def write_tg(entry, tier, tg, path_to_output_file):
    # create new textgrid file from extracted interval object
    newtg = textgrid.Textgrid()
    if entry.end == tg.maxTimestamp:
        newEntries = [Interval(tg.minTimestamp, entry.start, ""), entry]
    else:
        newEntries = [Interval(tg.minTimestamp, entry.start, ""), entry, Interval(
            entry.end, tg.maxTimestamp, "")]
    newTier = tier.new(entries=newEntries)
    newtg.addTier(newTier)
    newtg.save(f"{path_to_output_file}.TextGrid",
               format="long_textgrid", includeBlankSpaces=False)

def write_txt(entry, path_to_output_file):
    # write interval label in text file
    # needed if doing aligmnent w Webmaus
    txt_filename = f'''{path_to_output_file}.txt'''
    txt = open(txt_filename, 'w')
    label = entry.label
    txt.write(label)
    txt.write("\n")
    txt.close()

def split_wav(entry, wave, path_to_output_file):
    # extract audio segment
    newWave = wave[entry.start*1000:entry.end*1000]
    newWave = newWave.set_channels(1)  # stereo to mono
    newWave.export(
        f"{path_to_output_file}.wav", format="wav")

# split wave and textgrid into multiple files (one per interval)
def divide(txg, wave):
    # open textgrid and wav
    tg = textgrid.openTextgrid(txg, False)
    wav = AudioSegment.from_file(wave)
     # create new directories
    folder = Path(txg).stem
    output_folder = f"../aligned/aligner-corpus/{folder}"
       # check if dir exists
    if os.path.isdir(output_folder) == False:
            # if not, mkdir
        os.mkdir(output_folder)
        # get tier names
    tiers = tg.tierNames
    for itier in range(len(tiers)):
        tier = tg.getTier(tiers[itier])
        print(len(tier.entries))
        for ientry in range(len(tier.entries)):
            entry = tier.entries[ientry]
            path_to_output_file = f'''{output_folder}/{tiers[itier]}_{entry.start}_{entry.end}'''

            write_txt(entry, path_to_output_file)
            split_wav(entry, wav, path_to_output_file)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("tg")
    parser.add_argument("wave")
    args = parser.parse_args()
    return args 

def main():
    args = parse_args()
    tg_file = args.tg
    wave_file = args.wave
    divide(tg_file, wave_file)

if __name__ == '__main__':
    main()
