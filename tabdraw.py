# @Author: Daniel Grooms
# @Description: Tab drawing class for the main application,
#               to be implemented in the View Screen

import os
from functools import partial

from tab import Tab

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.atlas import Atlas
from kivy.graphics import Rectangle

# The widget that holds the drawing of the tab
class TabCanvas(Widget):
    editable = False

    def setEditable(self):
        self.editable = True


# The area holding the tab canvas and the slider
class TabArea(BoxLayout):
    tabCanvas = ObjectProperty(None)
    slide = ObjectProperty(None)
    scrlv = ObjectProperty(None)

    # Constant declaration
    CHAR_WIDTH = 32
    CHAR_HEIGHT = CHAR_WIDTH
    ATLAS_PREFIX = 'atlas://Assets/main/'

    # Determines if tab can be edited
    editable = False

    def scroll_change(self, scrl, instance, value):
        scrl.scroll_x = value

    def slider_change(self, slide, instance, value):
        if value >= 0:
            slide.value = value

    def setEditable(self):
        self.editable = True
        self.tabCanvas.setEditable()

    def tabTouched(self, touch):
        print("Tab touched! X, Y: " + str(int(touch.x)) + ", " + str(int(touch.y)))
        # Get the indices of the corresponding character of the tab
        xpos = int(touch.x)
        ypos = int(touch.y)
        xIndex = (xpos // 32)
        yIndex = self.tabNumRows - (ypos // 32)
        print("Coords: " + str(yIndex) + " " + str(xIndex))

        # To access (row, column) use (yIndex, xIndex)

        # open input textbox

        # call tab to rewrite file at (yIndex, xIndex) with input if valid

    def drawtab(self, tabfile):
        self.tab = Tab(tabfile)
        grid = self.tab.getTabData()

        self.tabNumRows = len(grid) - 1

        with self.tabCanvas.canvas:
            for i in range(len(grid)):
                for j in range(len(grid[i])):
                    if isinstance(grid[i][j], str):
                        print(self.ATLAS_PREFIX+grid[i][j])
                        Rectangle(
                            source=self.ATLAS_PREFIX+grid[i][j],
                            pos=(j*self.CHAR_WIDTH, (self.tabNumRows-i)*self.CHAR_HEIGHT),
                            size=(self.CHAR_WIDTH, self.CHAR_HEIGHT)
                        )
                    elif isinstance(grid[i][j], list):
                        for item in grid[i][j]:
                            Rectangle(
                                source=self.ATLAS_PREFIX+item,
                                pos=(j*self.CHAR_WIDTH, (self.tabNumRows-i)*self.CHAR_HEIGHT),
                                size=(self.CHAR_WIDTH, self.CHAR_HEIGHT)
                            )
