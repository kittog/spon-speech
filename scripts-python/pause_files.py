# which textgrids have [pause] in them?

import glob
from pathlib import Path
import re

path_to_textgrids = "../TextGrid/"

textgrids = glob.glob(path_to_textgrids + "*.TextGrid")

pause_tg = []

for file in textgrids:
    with open(file, "r") as f:
        tg = f.read()
        if "[pause]" in tg or "+" in tg:
            pause_tg.append(file)

with open("fichiers_pause.txt", "w") as f:
    for i in range(len(pause_tg)):
        f.write(Path(pause_tg[i]).stem)
        f.write("\n")