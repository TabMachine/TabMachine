# @Author: Daniel Grooms
# @Description: Class to store tab information from incoming tab file

class Tab:
	tabdata = []
	blankTabLine = "--------------------|"

	# Constructor for a Tab object, which takes a file containing a tab
	def __init__(self, tabfile=''):
		self.tabfile = tabfile
		if tabfile != '':
			self.parse(tabfile)

	# Description: Returns the entry at the x,y coordinate of the grid,
	#   or just returns the 2d grid if no x,y coordinate is passed
	def getTabData(self, x=-1, y=-1):
		if x >= 0 and y >= 0:
			return self.tabdata[x][y]
		else:
			return self.tabdata

	# Write a single change to the tab file
	def write(self, row, col, value):
		tab = open(self.tabfile, 'r')
		data = list(tab.read())
		tab.close()

		inputLength = len(str(value))
		print("input length is " + str(inputLength))
		position = (self.tabLength + 2) * row + col
		data[position] = value

		# If input is multiple characters long, must delete following hyphens
		if inputLength == 2:
			# Look for pattern of '--' and delete one '-'
			look = position + 2
			found = False
			while not found:
				if data[look] == '-' and data[look + 1] == '-':
					data = data[0:look] + data[look + 1:]
					found = True
				look += 1
		elif inputLength == 3:
			# Look for '---' and delete two '--'s
			look = position + 3
			found = False
			while not found:
				if data[look] == '-' and data[look + 1] == '-' and data[look + 2] == '-':
					data = data[:look] + data[look + 2:]
					found = True
				look += 1

		tab = open(self.tabfile, 'wb')
		for item in data:
			tab.write(bytes(item, 'UTF-8'))

	# Extend the tab by one bar
	def extendByOneBar(self):
		extendedTab = ''
		tabLines = []
		tab = open(self.tabfile)
		linecount = 0

		for line in tab:
			tabLines.append(line)
			linecount += 1
		tab.close()

		if linecount < 2:
			for i in range(5):
				extendedTab += '|' + self.blankTabLine + '\n'
			extendedTab += '|' + self.blankTabLine
		else:
			for i in range(len(tabLines)):
				if i < len(tabLines) - 1:
					# Not the last line
					newlineIndex = tabLines[i].find('\n')
					extendedTab += tabLines[i][:newlineIndex] + self.blankTabLine
					extendedTab += "\n"
				else:
					# Last line gets special treatment
					extendedTab += tabLines[i] + self.blankTabLine

		tab = open(self.tabfile, 'w')
		tab.write(extendedTab)
		tab.close()

	# Reduce the tab by one bar
	# If bar has content, confirmation is needed from the user
	def reduceByOneBar(self):
		tab = open(self.tabfile)
		reducedTab = ''
		tabLines = []
		hasMoreThanOneBar = True

		for line in tab:
			tabLines.append(line)
		tab.close()

		if len(tabLines[0]) < len(self.blankTabLine) * 2:
			hasMoreThanOneBar = False

		# Find index of 2nd to last bar, which will be the end of the tab
		if hasMoreThanOneBar:
			for i in range(len(tabLines)):
				firstBar = True
				j = len(tabLines[i]) - 1
				if j > 0:
					while(tabLines[i][j] != '|' or firstBar):
						if tabLines[i][j] == '|':
							firstBar = False
						j -= 1;

					# j is now at the 2nd to last bar
					if i < len(tabLines) - 1:
						reducedTab += tabLines[i][0:j+1] + "\n"
					else:
						reducedTab += tabLines[i][0:j+1]

			tab = open(self.tabfile, 'w')
			tab.write(reducedTab)
			tab.close()

	# Description: parse a txt file as a guitar tab, storing the corresponding
	#   image name for the Atlas in a 2d array, available for lookup.
	#   Stores as either a string, or in the case of overlapping images,
	#   stores as a list of two values.
	def parse(self, tabfile):
		tab = open(tabfile)

		# Initialize tabdata for a clean parse
		self.tabdata = []

		i = 0
		for line in tab:
			self.tabLength = len(line) - 1
			# Parse by character, translating input to graphical output
			self.tabdata.append([])
			for j in range(len(line)):
				thischar = line[j]
				if thischar == '\n' or thischar == ':':
					pass
				elif j == 0:
					self.tabdata[i].append('tbar')
				elif thischar == "|" and j > 0:
					# Plus bar
					self.tabdata[i].append('plusbar')
				elif thischar == "-":
					# Horizontal line
					self.tabdata[i].append('bar')
				elif thischar == "x" or thischar == "X":
					self.tabdata[i].append('mute')
				elif thischar == '\\' or thischar == '/':
					# Slide to next note, indicated with an arrow
					self.tabdata[i].append('slide')
				elif thischar == '~':
					# Vibrato, wavy string to show pull in both directions
					self.tabdata[i].append('vibrato')
				elif thischar == '*':
					# Squealie or harmonic
					self.tabdata[i].append('bar')
					# Write over previous note with squealie outline
					backtrack = 1
					if int(lastNumRead) >= 10:
						backtrack = 2
					self.tabdata[i][j-backtrack] = ['squealie', lastNumRead]
				elif thischar == 'h':
					#Hammer on
					self.tabdata[i].append('bar')
					backtrack = 1
					if int(lastNumRead) >= 10:
						backtrack = 2
					self.tabdata[i][j-backtrack] = ['hammeron', lastNumRead]
				elif thischar == 'p':
					#Pull off
					self.tabdata[i].append('bar')
					backtrack = 1
					if int(lastNumRead) >= 10:
						backtrack = 2
					self.tabdata[i][j-backtrack] = ['pulloff', lastNumRead]
				#elif thischar == 'b':
					#Bend note (may be up or down)
				else:
					# Look for digits
					found = False
					thisdigit = -1

					# See if this character is in range (0-9)
					for num in range(10):
						if str(num) == thischar and not found:
							found = True
							thisdigit = num
					# Get next and last character for 2-digit notes
					lastchar = ''
					nextchar = ''
					if found:
						if j-1 >= 0:
							lastchar = line[j-1]
						if j+1 < len(line):
							nextchar = line[j+1]

					if found and lastchar != '1' and lastchar != '2':
						# Could be a double digit note
						if thischar == '1' or thischar =='2':
							nextfound = False
							nextchar = line[j+1]
							for num in range(10):
								if str(num) == nextchar and not nextfound:
									nextfound = True
									combo = thischar + nextchar
									lastNumRead = combo
									self.tabdata[i].append(['norm', combo])

							# Wasn't double digit, draw it alone
							if not nextfound:
								lastNumRead = thischar
								self.tabdata[i].append(['norm', thischar])

						# It's just a lonely single digit, draw it
						else:
							lastNumRead = thischar
							self.tabdata[i].append(['norm', thischar])
					else:
						self.tabdata[i].append('bar')
			# Increment counter
			i += 1
		# Close tab
		tab.close()
		self.numRows = i + 1
