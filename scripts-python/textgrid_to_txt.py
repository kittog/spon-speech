import glob
import os
from pathlib import Path
from pydub import AudioSegment
from praatio import textgrid
from praatio import audio

def divide(entry, wave, filename, new_filename, tier):
    # create new textgrid and wave file from xmin to xmax
    # new textgrid file
    newtg = textgrid.Textgrid()
    newTier = tier.new(entries=[entry])
    newtg.addTier(newTier)
    newtg.save(f"../corpus-cut/TextGrid-cut/{filename}/{new_filename}.TextGrid",
               format="long_textgrid", includeBlankSpaces=False)
    # wave
    newWave = wave[entry.start*1000:entry.end*1000]
    newWave.export(
        f"../corpus-cut/waves-cut/{filename}/{new_filename}.wav", format="wav")

def label_to_txt(path_to_textgrid, folder):
    # extract label from textgrid and save to text file
    tg = textgrid.openTextgrid(path_to_textgrid, False)
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

def divide_and_write(textgrids, waves):
    for i in range(len(textgrids)):
        # open textgrid and wav
        tg = textgrid.openTextgrid(textgrids[i], False)
        wave = AudioSegment.from_file(waves[i])
        # create new directories
        filename = Path(textgrids[i]).stem
        os.mkdir(f"../corpus-cut/TextGrid-cut/{filename}")
        os.mkdir(f"../corpus-cut/waves-cut/{filename}")
        os.mkdir(f"../corpus-cut/txt-cut/{filename}")
        # get tier names
        tiers = tg.tierNames
        for itier in range(len(tiers)):
            tier = tg.getTier(tiers[itier])
            for ientry in range(len(tier.entries)):
                entry = tier.entries[ientry]
                newtier_name = "_".join(tiers[itier].split())
                new_filename = f"{newtier_name}_{round(entry.start,3)}_{round(entry.end,3)}"

                # cut
                divide(entry, wave, filename, new_filename, tier)
                # label_to_txt
                # label_to_txt(f"../corpus-cut/TextGrid-cut/{filename}/{new_filename}.TextGrid", filename)




# main
print(os.getcwd())

path_to_textgrids = "../cfpp/TextGrid-clean/"
path_to_waves = "../cfpp/wav/"

textgrids = glob.glob(path_to_textgrids + "*.TextGrid")
waves = glob.glob(path_to_waves + "*.wav")

textgrid_test = [path_to_textgrids +
                 "Pierre_Beysson_H_59_Marie_Beysson_F_X_12e-v2.TextGrid"]
wave_test = [path_to_waves +
             "Pierre_Beysson_H_59_Marie_Beysson_F_X_12e.wav"]
divide_and_write(textgrid_test, wave_test)