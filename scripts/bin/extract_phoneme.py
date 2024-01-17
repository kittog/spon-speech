#!/bin/python3
# -*- coding: utf-8 -*-

import argparse
import glob
from pathlib import Path
import pandas as pd
import tgt
from praatio import textgrid
from pydub import AudioSegment
import opensmile

def process_df(features):
    # preprocess dataframe and save to csv
    # drop start and end indexes
    features.rest_index(inplace=True, level=['start', 'end'])
    # convert timedelta to seconds
    features['start'] = features['start'].dt.total_seconds()
    features['end'] = features['end'].dt.total_seconds()
    # save to csv
    features.to_csv('file.csv')

def extract_audio_features(filename, start, end):
    # filename : corresponding wav (to textgrid)
    # start - end : phoneme
    seg = AudioSegment.from_file(filename)
    # extract segment
    phone = seg[start*1000:end*1000]
    phone_filename = "" # TODO create needed arborescence /phones/phoneme/features/.csv
    # save file
    phone.export(phone_filename, format="wav")
    # extract features w opensmile
    smile = opensmile.Smile(
        feature_set=opensmile.FeatureSet.GeMAPSv01b,
        feature_level=opensmile.FeatureLevel.LowLevelDescriptors
    )
    features = smile.process_file(phone_filename) # dataframe
    return features

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('phone', type=str)
    parser.add_argument('folder', type=str) # folder w segmented waves and textgrids
    args = parser.parse_args()
    return args

def main():
    args = parse_args() # namespace
    phone = args.phone
    textgrids = sorted(glob.glob(args.folder + "*.TextGrid"))
    for grid in textgrids:
        filename = Path(grid).stem
        tg = textgrid.openTextgrid(grid, includeEmptyIntervals=True)
        phones_tier = tg.getTier('phones') # phones alignment (mfa)
        entries = phones_tier.entries
        for ientry in range(len(entries)):
            entry = entries[ientry]
            if entry.label == phone:
                features = extract_audio_features(f"{args.folder}{filename}.wav", entry.start, entry.end) # dataframe
                process_df(features)


if __name__ == '__main__':
    main()
