import glob
import re
from praatio import textgrid

# file list
path = "../TextGrid/"
gridFiles = glob.glob(path + "*.TextGrid")

# soundFiles = glob.glob(path)

for grid in gridFiles[:2]:
    tg = textgrid.openTextgrid(grid, False)
    # create new textgrid
    newtg = textgrid.Textgrid()
    tiers = tg.tierNames
    for itier in range(len(tiers)):
        tier = tg.getTier(tiers[itier])
        # labelList = [entry.label for entry in tier.entries]
        newEntries = []
        # range(len(tier.entries))
        for ientry in range(len(tier.entries)):
            entry = tier.entries[ientry]
            label = entry.label

            # didascalies
            cleanLabel = re.sub("(\[|\{)[^pause]\w*(\}|\])", "", label)
            # speech
            # cleanLabel = re.sub()
            # mmm
            cleanLabel = re.sub("(m+h+)", "euh", cleanLabel)
            # clitiques
            cleanLabel = re.sub("c['] ", "ce", cleanLabel)
            cleanLabel = re.sub("j['] ", "je", cleanLabel)
            cleanLabel = re.sub("t['] ", "tu", cleanLabel)

            # create new entry
            newEntry = (entry.start, entry.end, cleanLabel)
            newEntries.append(newEntry)

        # copy tier, replace entries
        newTier = tier.new(entries=newEntries)
        newtg.addTier(newTier)
    # save new textgrid
    newtg.save("TextGrid-clean/" + grid[len(path):],
                format="short_textgrid", includeBlankSpaces=True)

enq = []
for grid in gridFiles:
    tg = textgrid.openTextgrid(grid, False)
    tiers = tg.tierNames
    for i in range(len(tiers)):
        if "ENQ" in tiers[i]:
            #print(grid + ": " + tiers[i])
            enq.append(tiers[i])
#print(len(enq) == len(gridFiles))