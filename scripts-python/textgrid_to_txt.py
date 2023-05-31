import glob
import os
from pathlib import Path
from pydub import AudioSegment
from praatio import textgrid
from praatio import audio


def divide(textgrids, waves):
    for i in range(len(textgrids)):
        # open textgrid and wav
        tg = textgrid.openTextgrid(textgrids[i], False)
        wave = AudioSegment.from_file(waves[i])
        # create new directories
        filename = Path(textgrids[i]).stem
        os.mkdir(f"../TextGrid-cut/{filename}")
        os.mkdir(f"../waves-cut/{filename}")
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
                newtg.save(f"../TextGrid-cut/{filename}/{tiers[itier]}_{entry.start}_{entry.end}.TextGrid",
                           format="long_textgrid", includeBlankSpaces=False)
                # wave
                newWave = wave[entry.start*1000:entry.end*1000]
                newWave.export(
                    f"../waves-cut/{filename}/{tiers[itier]}_{entry.start}_{entry.end}.wav", format="wav")


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


def txt_or_divide(path_to_folder, func):
    gridFiles = glob.glob(path_to_folder + "*.TextGrid")
    for grid in gridFiles:
        func(grid)


# main
print(os.getcwd())

path_to_textgrids = "TextGrid-corpus/"
path_to_waves = "../cfpp/wav/"

textgrids = glob.glob(path_to_textgrids + "*.TextGrid")
waves = glob.glob(path_to_waves + "*.wav")

textgrids_test = ""
divide(textgrids, waves)