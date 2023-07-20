import opensmile
import pandas as pd
import numpy as np
import IPython
import os

wave = "../corpus-cut/waves-cut/Therese_Le_Vern_F_70_Valentine_Testanier_F_60_12e-v2/Thérèse_le_Vern_4622.704_4624.14.wav"
IPython.display.Audio(wave)

smile = opensmile.Smile(
    feature_set=opensmile.FeatureSet.GeMAPSv01b,
    feature_level=opensmile.FeatureLevel.LowLevelDescriptors,
)
result_df = smile.process_file(wave)

centerformantfreqs = ['F1frequency_sma3nz', 'F2frequency_sma3nz', 'F3frequency_sma3nz']
formant_df = result_df[centerformantfreqs]
formant_df.head()

result_df.to_csv("features.csv")
formant_df.to_csv("formants.csv")
