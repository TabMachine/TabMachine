#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

# Python imports
from functools import partial
import os
import random

# Local project imports
from tabdraw import TabArea

# Kivy imports
import kivy
kivy.require('1.8.0')

from kivy.config import Config
Config.set('graphics', 'width', '1400')
Config.set('graphics', 'height', '400')

from kivy.app import App
from kivy.lang import Builder
from kivy.metrics import sp
from kivy.properties import NumericProperty
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.videoplayer import VideoPlayer
from kivy.uix.screenmanager import Screen
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.screenmanager import SlideTransition
from kivy.properties import StringProperty
from kivy.base import EventLoop
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.stacklayout import StackLayout
from kivy.graphics import Color, Rectangle, Line
from kivy.atlas import Atlas
from kivy.uix.scrollview import ScrollView
from kivy.uix.slider import Slider
#from libs import browser
import webbrowser

# What is i and where is it used?
i = 0

vp = VideoPlayer(source="Assets/videos/testVideo.mp4", options={'allow_stretch': True})
EventLoop.ensure_window()
__version__ = '0.2.4'
#Adds different fonts to the program can use the name in the label to use different
#fonts Ex. Label:
#          font_name: name_of_font
from kivy.core.text import LabelBase
KIVY_FONTS = [
    {
        "name": "bitMap",
        "fn_regular": "Assets/fonts/bitMap.ttf",
    }
]

for font in KIVY_FONTS:
    LabelBase.register(**font)

screens = ["Title", "CreateScreen", "ViewScreen"]
for screen in screens:
    kv_file = "{}.kv".format(screen.lower())
    Builder.load_file(os.path.join("screens", kv_file))

class LoadDialog(FloatLayout):
    curdir = os.path.dirname(os.path.realpath(__file__))
    # Need to use curdir to open THIS folder location
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)


class SaveDialog(FloatLayout):
    save = ObjectProperty(None)
    #text_input = ObjectProperty(None)
    cancel = ObjectProperty(None)


class TitleScreen(Screen):
	def on_enter(self):
		self.ids.video_ai.add_widget(vp)

	def on_leave(self):
		self.ids.video_ai.remove_widget(vp)


class CreateScreen(Screen):
    def on_enter(self):
        print('Enter create screen')


class ViewScreen(Screen):
    loadfile = ObjectProperty(None)
    savefile = ObjectProperty(None)
    tabarea = ObjectProperty(None)
    curDirectory = os.path.dirname(os.path.realpath(__file__))

    def on_enter(self):
        # starts the file manager when this screen is entered
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content, size_hint=(0.4, 0.8))
        self._popup.open()

    def dismiss_popup(self):
        self._popup.dismiss()
        self.manager.current = 'Title'

    def load(self, path, filename):
        #loads the file
        tab = os.path.join(path, filename[0])
        self._popup.dismiss()

        # Draws tab in the ViewScreen's tabArea
        self.tabarea.drawtab(tab)

    def show_save(self):
        content = SaveDialog(save=self.save, cancel=self.dismiss_popup)
        print(self.save)
        self._popup = Popup(title="Save file", content=content, size_hint=(0.9, 0.9))
        self._popup.open()


# Main widget of the app
class TabMachine(BoxLayout):
    def __init__(self, **kwargs):
        super(TabMachine, self).__init__(**kwargs)
        self.orientation = 'vertical'
        # Adds the screen manager to the main app
        self.root = ScreenManager()
        # Displays in the order of adds
        # Add the nav bar to the top
        self.root.add_widget(TitleScreen(name='Title'))
        self.root.add_widget(CreateScreen(name='CreateScreen'))
        self.root.add_widget(ViewScreen(name='ViewScreen'))

        self.slide_menu = NavMenu(root=self)
        self.add_widget(self.slide_menu)
        # Add the screen to the middle.
        #self.add_widget(self.content)
        self.add_widget(self.root)

    def set_current_screen(self, jump_to):
        self.root.current = jump_to


Builder.load_file("screens/navmenu.kv")

class NavMenu(BoxLayout):
    slide_spinner = ObjectProperty(None)

    def __init__(self, root, **kwargs):
        super(NavMenu, self).__init__(**kwargs)
        self.root = root
        #self.slide_spinner.values = screens

    #def go_slide(self, spinner):
    #    if spinner.text in screens:
    #        self.root.set_current_slide(spinner.text)

    def go_create(self):
        self.root.set_current_screen('CreateScreen')

    def go_view(self):
        self.root.set_current_screen('ViewScreen')


class TabMachineApp(App):
    font_size_regular = sp(25)
    font_size_large = font_size_regular * 2
    font_size_xlarge = font_size_regular * 3

    curDirectory = os.path.dirname(os.path.realpath(__file__))
    def build(self):
        return TabMachine()

    def open_browser(self):
        webbrowser.open('http://kivy.org/')

    def on_pause(self):
        return True

    def on_resume(self):
        pass


if __name__ == '__main__':
    TabMachineApp().run()
