# @Author: Daniel Grooms
# @Description: Tab drawing class for the main application,
#               to be implemented in the View Screen

import os

from tab import Tab

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
    ATLAS_PREFIX = 'atlas://Assets/main/'

    lineheight = 32
    startheight = 6 * lineheight

    def drawtab(self, tabfile):
        self.tab = Tab(tabfile)
        grid = self.tab.getTabData()

        numRows = len(grid)

        with self.tabCanvas.canvas:
            for i in range(len(grid)):
                for j in range(len(grid[i])):
                    if isinstance(grid[i][j], str):
                        print(self.ATLAS_PREFIX+grid[i][j])
                        Rectangle(
                            source=self.ATLAS_PREFIX+grid[i][j],
                            pos=(j*self.CHAR_WIDTH, (numRows-i)*self.CHAR_HEIGHT),
                            size=(self.CHAR_WIDTH, self.CHAR_HEIGHT)
                        )
                    elif isinstance(grid[i][j], list):
                        for item in grid[i][j]:
                            Rectangle(
                                source=self.ATLAS_PREFIX+item,
                                pos=(j*self.CHAR_WIDTH, (numRows-i)*self.CHAR_HEIGHT),
                                size=(self.CHAR_WIDTH, self.CHAR_HEIGHT)
                            )

    def scroll_change(self, scrl, instance, value):
        scrl.scroll_x = value

    def slider_change(self, slide, instance, value):
        if value >= 0:
            slide.value = value
