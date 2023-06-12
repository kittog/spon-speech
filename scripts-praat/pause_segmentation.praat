textGrid = Read from file:  "/home/lena/Documents/LPP/spon-speech/TextGrid-corpus/Catherine_Lecuyer_F_39_SO-v2.TextGrid"
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
                	selectObject: textGrid
                	View & Edit alone
                	editor = textGrid
                	editor: editor
                		Select: xmin, xmax
                		Zoom to selection
				pause Annotate
				Close
		endfor
	endif
endfor