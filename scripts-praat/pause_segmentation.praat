clearinfo

tg$ = "/home/lena/Documents/LPP/TextGrid"
sounds$ = "/home/lena/Documents/cfpp/mp3"
Create Strings as file list: "textFiles$", "tg$" + "*.TextGrid"
Create Strings as file list: "soundFiles$", "sounds$" + "*.wav"

nfiles = Get number of strings: textFiles$
for ifile from 1 to nfiles
	sound = Read from file: sound$ + "/" + soundFiles$# [ifile]
	textGrid = Read from file: folder$ + "/" + fileNames$ [ifile]
	nTiers = Get number of tiers

		# loop through tiers
	for tierIndex from 1 to nTiers
		nIntervals = Get number of intervals: tierIndex

			# loop through intervals
		pauseCount = Count intervals where: tierIndex, "matches (regex)", "\[pause\]"
			if pauseCount <> 0
				for inter from 1 to nIntervals
						intText$ = Get label of interval: tierIndex, inter
						xmin = Get start time of interval: tierIndex, inter
						xmax = Get end time of interval: tierIndex, inter
						selectObject: textGrid, sound
						View & Edit
						editor = textGrid + sound
						editor: editor
							Select: xmin, xmax
							Zoom to selection
							pause Annotate
							Close
			endfor
		endif
	endfor
endfor