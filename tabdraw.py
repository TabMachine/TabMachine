# @Author: Daniel Grooms
# @Description: Tab drawing class for the main application,
#               to be implemented in the View Screen

import os

from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.atlas import Atlas
from kivy.graphics import Rectangle

class TabArea(BoxLayout):
    tabCanvas = ObjectProperty(None)
    slide = ObjectProperty(None)

    # Constant declaration
    CHAR_WIDTH = 32
    CHAR_HEIGHT = CHAR_WIDTH

    lineheight = 32
    startheight = 6 * lineheight

    def drawtab(self, tab):
        # Required tab pre-processing:
        # 1. Between brackets (|) enforce a bar width (set number of characters)

        wid = self.tabCanvas
        lastNumRead = ''

        # Get path to current file to find atlas file
        curdir = os.path.dirname(os.path.realpath(__file__))
        atlas = Atlas(curdir + r"/Assets/main.atlas")

        i = 0
        for line in tab:
            # Parse by character, translating input to graphical output
            with wid.canvas:
                for j in range(len(line)):
                    thischar = line[j]
                    if thischar == '\n' or thischar == ':':
                        pass
                    elif j == 0:
                        # T bar
                        Rectangle(source='atlas://Assets/main/tbar',
                                  pos=(0, self.startheight-(i*self.lineheight)),
                                  size=(32, 32))
                    elif thischar == "|" and j > 0:
                        # Plus bar
                        #print("Making vertical line")
                        Rectangle(source='atlas://Assets/main/plusbar',
                                  pos=(j*self.CHAR_WIDTH, self.startheight-(i*self.lineheight)),
                                  size=(32, 32))
                    elif thischar == "-":
                        # Horizontal line
                        #print("Making horizontal line")
                        Rectangle(source='atlas://Assets/main/bar',
                                  pos=(j*self.CHAR_WIDTH, self.startheight-(i*self.lineheight)),
                                  size=(32, 32))
                    elif thischar == "x" or thischar == "X":
                        # Mute or X in tab
                        Rectangle(source='atlas://Assets/main/mute',
                                  pos=(j*self.CHAR_WIDTH, self.startheight-(i*self.lineheight)),
                                  size=(32, 32))
                    elif thischar == '\\' or thischar == '/':
                        # Slide to next note, indicated with an arrow
                        Rectangle(source='atlas://Assets/main/slide',
                                  pos=(j*self.CHAR_WIDTH, self.startheight-(i*self.lineheight)),
                                  size=(32, 32))
                    elif thischar == '~':
                        # Vibrato, wavy string to show pull in both directions
                        Rectangle(source='atlas://Assets/main/vibrato',
                                  pos=(j*self.CHAR_WIDTH, self.startheight-(i*self.lineheight)),
                                  size=(32, 32))
                    elif thischar == '*':
                        # Squealie or harmonic
                        Rectangle(source='atlas://Assets/main/bar',
                                  pos=(j*self.CHAR_WIDTH, self.startheight-(i*self.lineheight)),
                                  size=(32, 32))
                        # Write over previous note with squealie outline
                        backtrack = 1
                        if int(lastNumRead) >= 10:
                            backtrack = 2
                        Rectangle(source='atlas://Assets/main/squealie',
                                  pos=((j-backtrack)*self.CHAR_WIDTH, self.startheight-(i*self.lineheight)),
                                  size=(32, 32))
                        Rectangle(source=('atlas://Assets/main/' + lastNumRead),
                                  pos=((j-backtrack)*self.CHAR_WIDTH, self.startheight-(i*self.lineheight)),
                                  size=(32, 32))
                    # Look for digits
                    else:
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
                                        print("Making " + combo)
                                        self.drawNormNote(combo, j, i)

                                # Wasn't double digit, draw it alone
                                if not nextfound:
                                    lastNumRead = thischar
                                    print("Making " + thischar)
                                    self.drawNormNote(thischar, j, i)

                            # It's just a lonely single digit, draw it
                            else:
                                lastNumRead = thischar
                                self.drawNormNote(thischar, j, i)
                        else:
                            print("Unknown symbol or second digit")
                            Rectangle(source='atlas://Assets/main/bar',
                                      pos=(j*self.CHAR_WIDTH, self.startheight-(i*self.lineheight)),
                                      size=(32, 32))

            # Increment counter
            i += 1

    def drawNormNote(self, num, xpos, ypos):
        wid = self.tabCanvas

        with wid.canvas:
            Rectangle(source=('atlas://Assets/main/norm'),
                      pos=(xpos*self.CHAR_WIDTH, self.startheight-(ypos*self.lineheight)),
                      size=(32, 32))
            Rectangle(source=('atlas://Assets/main/' + num),
                      pos=(xpos*self.CHAR_WIDTH, self.startheight-(ypos*self.lineheight)),
                      size=(32, 32))

    def scroll_change(self, scrl, instance, value):
        scrl.scroll_x = value

    def slider_change(self, slide, instance, value):
        if value >= 0:
            slide.value = value
