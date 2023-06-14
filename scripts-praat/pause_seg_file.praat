clearinfo

sound = Open long sound file: "/home/lena/Documents/LPP/cfpp/wav/Ozgur_Kilic_H_32_alii_3e.wav"
textGrid = Read from file: "/home/lena/Documents/LPP/TextGrid/Ozgur_Kilic_H_32_alii_3e-1-v2.TextGrid" 
nTiers = Get number of tiers

		# loop through tiers
for tierIndex from 1 to nTiers
	nIntervals = Get number of intervals: tierIndex

			# loop through intervals
	pauseCount = Count intervals where: tierIndex, "matches (regex)", "[pause]"
	if pauseCount <> 0
		for inter from 1 to nIntervals			
			intText$ = Get label of interval: tierIndex, inter
			appendInfoLine: intText$
			appendInfoLine: index (intText$, "[pause]")
			if index (intText$, "[pause]") > 0
				xmin = Get start time of interval: tierIndex, inter
				xmax = Get end time of interval: tierIndex, inter
				selectObject: textGrid, sound
				View & Edit
				editor = textGrid
				editor: editor
			    		Select: xmin, xmax
					Zoom to selection
					appendEditor: "pause Annotate"
				endeditor
			endif
		endfor
	endif
endfor