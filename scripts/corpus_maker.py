#!/bin/python3
# -*- coding: utf-8 -*-

# arg parser
import click
# audio and textgrid
from praatio import textgrid
from pathlib import Path
from pydub import AudioSegment
import tgt
# files
import os
from pathlib import Path


def create_wave(wave, interval, filename, tier_name):
    '''Extracts audio portion corresponding to selected interval.'''
    start = interval.start_time
    end = interval.end_time
    new_wave = wave[start*1000:end*1000]
    new_wave.export(
        f"aligner-corpus/{tier_name}/{filename}.wav",
        format="wav"
    )

def create_txt(interval, filename, tier_name):
    '''Creates text file with corresponding transcription for Webmaus.'''
    text = interval.text  # label
    with open(f"aligner-corpus/{tier_name}/{filename}.txt", "w") as f:
        f.write(text)

def create_output_folder(tg):
    '''Creates output folder for selected speaker.'''
    # output folder path
    output_folder = "aligner-corpus"
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
    tg = tgt.io.read_textgrid(tg_file)
    wav = AudioSegment.from_file(wav_file)
    # create output folder
    create_output_folder(tg)
    # segment into files
    tiers = tg.tiers
    for itier in range(len(tiers)):
        tier = tiers[itier]
        # format speaker name
        speaker = "_".join(tier.name.split())
        for intr in tier.annotations:
            if intr.end_time - intr.start_time > 8:
                # format filename
                filename = f"{speaker}_{round(intr.start_time, 3)}_{round(intr.end_time, 3)}"
                # create wave file
                create_wave(wav, intr, filename, tier.name)
                # create txt file
                create_txt(intr, filename, tier.name)


if __name__ == "__main__":
    main()