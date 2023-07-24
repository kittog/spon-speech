#!/bin/python3
# -*- coding: utf-8 -*-

import glob
import os
import argparse
from pathlib import Path
from pydub import AudioSegment
from praatio import textgrid
from praatio import audio

# split wave and textgrid into multiple files (one per interval)
def divide(textgrids, waves):
    for i in range(len(textgrids)):
        # open textgrid and wav
        tg = textgrid.openTextgrid(textgrids[i], False)
        wave = AudioSegment.from_file(waves[i])
        # create new directories
        filename = Path(textgrids[i]).stem
        output_folder = f"../aligned/aligner-corpus/{filename}"
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
                # new textgrid file
                newtg = textgrid.Textgrid()
                newTier = tier.new(entries=[entry])
                newtg.addTier(newTier)
                newtg.save(f"{output_folder}/{tiers[itier]}_{entry.start}_{entry.end}.TextGrid",
                           format="long_textgrid", includeBlankSpaces=False)
                # wave
                newWave = wave[entry.start*1000:entry.end*1000]
                newWave.export(
                    f"{output_folder}/{tiers[itier]}_{entry.start}_{entry.end}.wav", format="wav")

# for webmaus (only accepts transcriptions through .txt files)
def label_to_txt(path_to_TextGrid):
    # path_to_TextGrid = filename, str
    tg = textgrid.openTextgrid(path_to_TextGrid, False)
    txt_file_name = path_to_TextGrid.split(".")[0] + ".txt"
    txt = open(txt_file_name, "w")
    tiers = tg.tierNames  # list
    # technically only one tier remains !
    for itier in range(len(tiers)):
        tier = tg.getTier(tiers[itier])
        for ientry in range(len(tier.entries)):
            entry = tier.entries[ientry]
            label = entry.label
            txt.write(label)
            txt.write("\n")
    txt.close()


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("tg")
    parser.add_argument("wave")
    args = parser.parse_args()
    return args 

def main():
    args = parse_args()
    tg_file = [args.tg]
    wave_file = [args.wave]
    divide(tg_file, wave_file)

if __name__ == '__main__':
    main()
