# @Author: Daniel Grooms
# @Description: Tab drawing class for the main application,
#               to be implemented in the View Screen

import os
from functools import partial

from tab import Tab

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.properties import ObjectProperty
from kivy.atlas import Atlas
from kivy.graphics import Rectangle


# The widget that holds the drawing of the tab
class TabCanvas(Widget):
    pass


# The area holding the tab canvas and the slider
class TabArea(BoxLayout):
    tabCanvas = ObjectProperty(None)
    slide = ObjectProperty(None)
    scrlv = ObjectProperty(None)

    # Constant declaration
    CHAR_WIDTH = 32
    CHAR_HEIGHT = CHAR_WIDTH
    ATLAS_PREFIX = 'atlas://Assets/main/'
    ACCEPT_CHARS = ['|', '-', 'x', 'X', '\\', '/', '~', '*']
    for num in range(25):
        ACCEPT_CHARS.append(str(num))

    # Determines if tab can be edited
    editable = False
    inputText = ''

    def scroll_change(self, scrl, instance, value):
        scrl.scroll_x = value

    def slider_change(self, slide, instance, value):
        if value >= 0:
            slide.value = value

    # Set the tab as editable or not editable
    # Allows user to alter the tab depending on the value
    def setEditable(self, setter=True):
        self.editable = setter

    # A callback function to get the user input from the textInput module
    def setInputText(self, instance, value):
        self.inputText = str(value)

    # Detects a user click on the tab, and allows editing if the option is set
    def tabTouched(self, touch):
        if self.editable:
            # Get the indices of the corresponding character of the tab
            xpos = int(touch.x)
            ypos = int(touch.y)
            xIndex = (xpos // 32)
            yIndex = self.tabNumRows - (ypos // 32)
            print("Coords: " + str(yIndex) + " " + str(xIndex))

            # To access (row, column) use (yIndex, xIndex)

            # Popup a kivy TextInput
            textbox = TextInput(text='', multiline=False)
            inputPopup = Popup(
                title='Edit',
                content = textbox,
                size_hint = (None, None),
                size = (100, 100)
            )
            textbox.bind(on_text_validate=inputPopup.dismiss)
            textbox.bind(text=self.setInputText)
            inputPopup.bind(
                on_dismiss=partial(self.writeToTab, row=yIndex, col=xIndex)
            )
            inputPopup.open()
            # call tab to rewrite file at (yIndex, xIndex) with input if valid

    # Write input to the tab using tab's write function
    def writeToTab(self, instance, row, col):
        if self.editable:
            # Validate input
            if self.inputText in self.ACCEPT_CHARS:
                # Write to tab
                self.tab.write(row, col, self.inputText)
                self.drawtab()

    # Draws the tab to the screen from the given file using a Tab object
    def drawtab(self, filename=''):
        if filename != '':
            self.tabFile = filename
        self.tab = Tab(self.tabFile)
        grid = self.tab.getTabData()

        self.tabNumRows = len(grid) - 1

        with self.tabCanvas.canvas:
            for i in range(len(grid)):
                for j in range(len(grid[i])):
                    if isinstance(grid[i][j], str):
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
