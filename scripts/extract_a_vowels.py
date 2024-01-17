#!/bin/python3
# -*- coding: utf-8 -*-

# arg parser
import click
# files
import glob
from pathlib import Path
# data
import pandas as pd
# audio and textgrid
import tgt
from praatio import textgrid
from pydub import AudioSegment

def create_wave(wave, interval, speaker):
    '''Extracts audio portion corresponding to selected interval.'''
    start = interval.start_time
    end = interval.end_time
    vowel = interval.text
    new_wave = wave[start*1000:end*1000]
    new_wave.export(
        f"vowels/{speaker}_{vowel}.wav",
        format="wav"
    )

@click.command()
@click.option('--folder', type=str, help='speaker folder')
def path_to_folder(folder):
    speaker = Path(folder).stem
    click.echo(f"Extracting vowels for {speaker}")
    return folder

def main():
    folder = path_to_folder.main(standalone_mode=False)
    textgrids = glob.glob(folder + "*.TextGrid")
    for grid in textgrids:
        print(grid)
        filename = Path(grid).stem
        speaker = filename.split("_")[0]
        tg = tgt.io.read_textgrid(grid)
        phones_tier = tg.get_tier_by_name('MAU') # phones alignment (webmaus)
        for intr in phones_tier.annotations:
            if intr.text == "a" or intr.text == "A":
                # open wave
                wave = AudioSegment.from_file(folder + filename + ".wav")
                # extract phoneme
                create_wave(wave, intr, filename)


if __name__ == "__main__":
    main()
