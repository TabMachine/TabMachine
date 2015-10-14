# @Author: Daniel Grooms
# @Description: Class to store tab information from incoming tab file

class Tab:
    tabdata = []

    # Constructor for a Tab object, which takes a file containing a tab
    def __init__(self, tabfile):
        self.tabfile = tabfile
        self.parse(tabfile)

    # Description: Returns the entry at the x,y coordinate of the grid,
    #   or just returns the 2d grid if no x,y coordinate is passed
    def getTabData(self, x=-1, y=-1):
        if x >= 0 and y >= 0:
            return self.tabdata[x][y]
        else:
            return self.tabdata

    # Write any changes to the tab file
    def write(self, row, col, value):
        tab = open(self.tabfile, 'r')
        data = list(tab.read())
        tab.close()

        position = (self.tabLength + 2) * row + col
        data[position] = value

        tab = open(self.tabfile, 'wb')
        for item in data:
            tab.write(bytes(item, 'UTF-8'))

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
