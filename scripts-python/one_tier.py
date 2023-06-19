# get one tier only
# on aurait pu faire cela sur elan directement, mais
# moins chronophage avec ça

# récupérer une seule tier

from praatio import textgrid
import glob
from pathlib import Path

def one_tier_only(path_to_file):
    filename = Path(path_to_file).stem
    newtg = textgrid.Textgrid()
    tg = textgrid.openTextgrid(path_to_file, False)
    tiers = tg.tierNames
    for itier in range(len(tiers)):
        tier = tg.getTier(tiers[itier])
        # pick better test
        if "(ENQ)" not in tiers[itier]:
            newTier = tier.new(entries=tier.entries)
            newtg.addTier(newTier)
    newtg.save(f"../TextGrid-corpus/{filename}.TextGrid",
            format="long_textgrid", includeBlankSpaces=False)


path_to_textgrids = "../TextGrid/"
textgrids = glob.glob(path_to_textgrids + "*.TextGrid")

for tg in textgrids:
    one_tier_only(tg)

