#!/bin/python3
# -*- coding: utf-8 -*-

# arg parser
import click
# audio and textgrid
from praatio import textgrid
from praatio.utilities.constants import Interval
from pathlib import Path
from pydub import AudioSegment
import tgt
# files
import os
from pathlib import Path


def create_wave(wave, entry, filename, tier_name):
    '''Extracts audio portion corresponding to selected interval.'''
    new_wave = wave[entry.start*1000:entry.end*1000]
    new_wave.export(
        f"../aligner-corpus/{tier_name}/{filename}.wav",
        format="wav"
    )    


def create_textgrid(entry, tier, tg, tier_name, filename):
    # create new textgrid file from extracted interval object
    newtg = textgrid.Textgrid()
    duration = entry.end - entry.start
    new_intr = textgrid.IntervalTier(name=tier_name, entries=[('0', duration, entry.label), ],
                                  minT=0, maxT=duration)
    newtg.addTier(new_intr)
    newtg.save(f"../aligner-corpus/{tier_name}/{filename}.TextGrid",
               format="long_textgrid", includeBlankSpaces=False)

def create_txt(entry, filename, tier_name):
    '''Creates text file with corresponding transcription for Webmaus.'''
    text = entry.label  # label
    with open(f"../aligner-corpus/{tier_name}/{filename}.txt", "w") as f:
        f.write(text)

def create_output_folder(tg):
    '''Creates output folder for selected speaker.'''
    # output folder path
    output_folder = "../aligner-corpus"
    # format speaker name
    tiers = tg.tiers
    for tier in tiers:
        if os.path.isdir(f"{output_folder}/{tier.name}") == False:
            os.mkdir(f"{output_folder}/{tier.name}")

# arg parser
@click.command()
@click.option('--wav', type=str,
              help='wave file')
@click.option('--tg', type=str,
                help='textgrid file')
def path_to_files(wav, tg):
    click.echo(f"Processing files {wav} and {tg}...")
    return wav, tg

def main():
    wav_file, tg_file = path_to_files.main(standalone_mode=False)
    # binary file (praat)
    tg = textgrid.openTextgrid(tg_file, includeEmptyIntervals=False)
    tg.save(tg_file, format="long_textgrid", includeBlankSpaces=True)
    # open files
    tg = textgrid.openTextgrid(tg_file, False)
    # wav = AudioSegment.from_file(wav_file)
    wav = ffmpeg.input(wav_file)
    # create output folder
    create_output_folder(tg)
    # segment into files
    tiers = tg.tierNames
    for itier in range(len(tiers)):
        tier = tg.getTier(tiers[itier])
        # format speaker name
        speaker = "_".join(tiers[itier].split())
        for ientry in range(len(tier.entries)):
            entry = tier.entries[ientry]
            filename = f'''{speaker}_{round(entry.start,3)}_{round(entry.end,3)}'''
            # create wave file
            create_wave(wav, entry, filename, tier.name)
            # create txt file
            create_txt(entry, filename, tier.name)
            # create TextGrid
            create_textgrid(entry, tier, tg, tiers[itier], filename)


if __name__ == "__main__":
    main()
