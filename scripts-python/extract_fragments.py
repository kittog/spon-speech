#!/bin/python3
# -*- coding: utf-8 -*-

import argparse
import glob
from pathlib import Path
import pandas as pd
from pydub import AudioSegment
import opensmile

def process_df():
    # process dataframe
    pass

def extract_features(filename):
    # extract features w opensmile
    smile = opensmile.Smile(
        feature_set=opensmile.FeatureSet.GeMAPSv01b,
        feature_level=opensmile.FeatureLevel.LowLevelDescriptors
    )
    features = smile.process_file(filename)  # dataframe
    return features

def extract_frag():
    # TODO: function which extracts 5s fragments
    pass

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument()
    args = parser.parse_args()
    return args

def main():
    pass

if __name__ == '__main__':
    main()