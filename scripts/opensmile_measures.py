#!/bin/python3
# -*- coding: utf-8 -*-

# arg parser
import click
# data
import pandas as pd
# files
import glob
from pathlib import Path
# audio
from pydub import AudioSegment
import librosa
import opensmile

def create_metadata(wave_files):
    # informations we are keeping for opensmile
    speakers = []
    vowels = []
    times = []

    for wav in wave_files:
        split = Path(wav).stem.split("_")
        speakers.append(split[0])
        vowels.append(split[-1])
        times.append(librosa.get_duration(path=wav))
    # setting up dictionnary to create dataframe
    data = {"files":pd.Series(wave_files),
            "speaker":pd.Series(speakers),
            "vowel":pd.Series(vowels),
            "duration":pd.Series(times)}
    df = pd.DataFrame(data)
    # save to .csv file
    df.to_csv("vowel_speaker.csv")

@click.command()
@click.option("--folder", type=str, help="folder with vowels.")
def path_to_folder(folder):
    click.echo(f"Processing folder {folder}.")
    return folder

def main():
    folder = path_to_folder.main(standalone_mode=False)
    waves = sorted(glob.glob(folder + "/*.wav"))

    create_metadata(waves)

    # opensmile
    df = pd.read_csv("vowel_speaker.csv")
    df.drop("Unnamed: 0", axis=1)
    df.set_index("files")
    print(df.head())
    print(df.columns)

    smile = opensmile.Smile(
    feature_set=opensmile.FeatureSet.GeMAPSv01b,
    feature_level=opensmile.FeatureLevel.Functionals,
    )

    df_feats = smile.process_files(df['files'])
    df_feats.to_csv("opensmile_measures.csv")

if __name__ == "__main__":
    main()
