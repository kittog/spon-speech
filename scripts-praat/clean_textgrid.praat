clearinfo

folder$ = "/home/lena/Documents/LPP/TextGrid"
fileNames$# = fileNames$# (folder$ +"/*.TextGrid")

# loop through .TextGrid files
for ifile to size (fileNames$#)

	textGrid = Read from file: folder$ + "/" + fileNames$# [ifile]
	nTiers = Get number of tiers
	printline 'nTiers'
	appendInfoLine: fileNames$# [ifile]

	# loop through tiers
	for tierIndex from 1 to nTiers
		printline 'tierIndex'
		nIntervals = Get number of intervals: tierIndex

		# loop through intervals
		for inter from 1 to nIntervals
			intText$ = Get label of interval: tierIndex, inter
			# appendInfoLine: intText$
			# didascalies
			regDid$ = "(\[|\{)[^pause]\w*(\}|\])"
			# mmm
			regMm$ = "m*h?"
			# clitiques
			regCl1$ = "c[] [^est]"
			regCl2$ = "j[] "
			regCl3$ = "t "
			# replace all matches
			intText$ = replace(intText$, regDid$, "", 0)
			intText$ = replace(intText$, regMm$, "mm", 0)
			intText$ = replace(intText$, regCl1$, "ce", 0)
			intText$ = replace(intText$, regCl2$, "je", 0)
			intText$ = replace(intText$, regCl3$, "tu", 0)
		Save as text file: fileNames$# [ifile]
		endfor
	endfor
endfor