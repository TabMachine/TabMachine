# @Author: Daniel Grooms
# @Description: Tab drawing class for the main application,
#				to be implemented in the View Screen

import os
from functools import partial

from tab import Tab

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.properties import ObjectProperty
from kivy.atlas import Atlas
from kivy.graphics import Rectangle
from kivy.lang import Builder
from kivy.uix.actionbar import ActionBar

# Global variable to hold the toggle button pressed on the edit toolbar
toggle_button = 'Null'
temp = ''
m = 0

# The widget that holds the drawing of the tab
class TabCanvas(Widget):
	pass


# The area holding the tab canvas and the slider
class TabArea(BoxLayout):
	tabCanvas = ObjectProperty(None)
	slide = ObjectProperty(None)
	scrlv = ObjectProperty(None)
	mainBoxLayout = ObjectProperty(None)

	# Constant declaration
	CHAR_WIDTH = 32
	CHAR_HEIGHT = CHAR_WIDTH
	ATLAS_PREFIX = 'atlas://Assets/main/'
	ACCEPT_CHARS = ['|', '-', 'x', 'X', '\\', '/', '~', '*', 'h', 'p', 'b', 'r', ]
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
	# Allows user to edit the tab if True
	def setEditable(self, setter=True):
		# Adds the 'extend tab' button to the right of the tab
		if not self.editable and setter:
			self.mainBoxLayout.add_widget(Button(text='Extend Tab',size_hint=(0.1, 0.5),on_release=self.extendTab))
			self.mainBoxLayout.add_widget(Button(text='Reduce Tab',size_hint=(0.1, 0.5),on_release=self.reduceTab))

		self.editable = setter

	# Extend each line of the tab by one blank bar
	def extendTab(self, kivyAction):
		self.tab.extendByOneBar()
		self.drawtab()

    # Reduce each line of the tab by one bar
	def reduceTab(self, kivyAction):
		self.tab.reduceByOneBar()
		self.drawtab()

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
			print('This is what your toggle button is: ', toggle_button)
			curr_val = self.tab.getTabData(yIndex, xIndex)
			double_digit = False
			modifier = True
			if len(curr_val[1]) != 1:
				double_digit = True
			print('this is the eval of double_digit: ', double_digit)
			if double_digit == True:
				double_val = self.tab.getTabData(yIndex,xIndex + 2)
				print('her is solksdflasf: ',self.tab.getTabData(yIndex,xIndex + 1), ' ', self.tab.getTabData(yIndex,xIndex), ' ', self.tab.getTabData(yIndex,xIndex + 2))
				if self.tab.getTabData(yIndex,xIndex) in ('bar' , 'tbar' , 'plusbar' , 'mute' , 'slide' , 'vibrato') or self.tab.getTabData(yIndex,xIndex)[0] == 'norm':
					modifier = False
				# if ((double_val in ('bar' , 'tbar' , 'plusbar' , 'mute' , 'slide' , 'vibrato')) or double_val[1].isdigit()):
					# modifier = False
			else:
				print('her is solksdflasf: ',self.tab.getTabData(yIndex,xIndex + 1), ' ', self.tab.getTabData(yIndex,xIndex)[0], ' ', self.tab.getTabData(yIndex,xIndex + 2))
				next_val = self.tab.getTabData(yIndex,xIndex + 1)
				if self.tab.getTabData(yIndex,xIndex) in ('bar' , 'tbar' , 'plusbar' , 'mute' , 'slide' , 'vibrato') or self.tab.getTabData(yIndex,xIndex)[0] == 'norm':
					modifier = False
				# if ((next_val in ('bar' , 'tbar' , 'plusbar' , 'mute' , 'slide' , 'vibrato')) or next_val[1].isdigit()):
					# modifier = False
			print('Result of modifier: ', modifier)
			if toggle_button == 'slide':
				self.inputText = '/'
				print('This is the inputText: ', self.inputText)
				self.writeToTab(0,yIndex,xIndex)
				if double_digit == True:
					self.inputText = '-'
					self.writeToTab(0,yIndex,xIndex + 1)
					if modifier == True:
						self.writeToTab(0,yIndex,xIndex + 2)
				else:
					self.inputText = '-'
					if modifier == True:
						self.writeToTab(0,yIndex,xIndex)
			elif toggle_button == 'vibrato':
				self.inputText = '~'
				print('This is the inputText: ', self.inputText)
				self.writeToTab(0,yIndex,xIndex)
				if double_digit == True:
					self.inputText = '-'
					self.writeToTab(0,yIndex,xIndex + 1)
					if modifier == True:
						self.writeToTab(0,yIndex,xIndex + 2)
				else:
					self.inputText = '-'
					if modifier == True:
						self.writeToTab(0,yIndex,xIndex)
			elif toggle_button == 'squealie':
				self.inputText = '*'
				print('This is the inputText: ', self.inputText)
				if double_digit == False:
					self.writeToTab(0,yIndex,xIndex + 1)
				else:
					self.writeToTab(0,yIndex,xIndex + 2)
			elif toggle_button == 'hammeron':
				self.inputText = 'h'
				print('This is the inputText: ', self.inputText)
				if double_digit == False:
					self.writeToTab(0,yIndex,xIndex + 1)
				else:
					self.writeToTab(0,yIndex,xIndex + 2)
			elif toggle_button == 'pulloff':
				self.inputText = 'p'
				print('This is the inputText: ', self.inputText)
				if double_digit == False:
					self.writeToTab(0,yIndex,xIndex + 1)
				else:
					self.writeToTab(0,yIndex,xIndex + 2)
			else:
				next_val = self.tab.getTabData(yIndex, xIndex + 1)
				if double_digit == False:
					if not (next_val[1].isdigit() or next_val[0] == '-'):
						self.inputText = '-'
						self.writeToTab(0,yIndex,xIndex + 1)
				else:
					self.inputText = '-'
					self.writeToTab(0,yIndex,xIndex + 1)
					if ((self.tab.getTabData(yIndex,xIndex + 2) not in ('bar' , 'tbar' , 'plusbar' , 'mute' , 'slide' , 'vibrato')) or not self.tab.getTabData(yIndex,xIndex + 2)[1].isdigit()):
						self.writeToTab(0,yIndex,xIndex + 2)
				textbox = TextInput(text='', multiline=False)
				inputPopup = Popup(
					title='Fret Number',
					content = textbox,
					size_hint = (None, None),
					size = (150, 100),
					#pos = (xpos, ypos)
					)
				textbox.bind(on_text_validate=inputPopup.dismiss)
				textbox.bind(text=self.setInputText)
				inputPopup.bind(
					on_dismiss=partial(self.writeToTab,row = yIndex, col = xIndex)
				)
				inputPopup.open()
			# call tab to rewrite file at (yIndex, xIndex) with input if valid

	# Write input to the tab using tab's write function
	def writeToTab(self, instance, row, col):
		if self.editable:
			# Validate input
			if self.inputText in self.ACCEPT_CHARS:
				# Write to tab
				print('We are writing ', self.inputText, ' to the tab!')
				self.tab.write(row, col, self.inputText)
				self.drawtab()

	# Draws the tab to the screen from the given file using a Tab object
	def drawtab(self, filename=''):
		if filename != '':
			self.tabFile = filename
		self.tab = Tab(self.tabFile)
		grid = self.tab.getTabData()
		self.tabNumRows = len(grid) - 1

		# Clear canvas in case a bar was removed
		self.tabCanvas.canvas.clear()
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

class Edittoolbar(ActionBar):
	Builder.load_file("screens/edittoolbar.kv")
	def checkButtons(self,value):
		#print(value)
		global toggle_button, temp, m
		if m > 0:
			temp = toggle_button
		toggle_button = value
		if temp == toggle_button:
			toggle_button = ''
		print(toggle_button)
		m += 1
		return value
