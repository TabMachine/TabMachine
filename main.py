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
from kivy.clock import Clock
from kivy.properties import NumericProperty
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.checkbox import CheckBox
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
from kivy.core.audio import SoundLoader, Sound
from kivy.uix.actionbar import ActionBar
import webbrowser
from kivy.garden.navigationdrawer import NavigationDrawer
# What is i and where is it used?
i = 0

global move_value
move_value = 0
vp = VideoPlayer(source="Assets/videos/testVideo.mp4", options={'allow_stretch': True})
EventLoop.ensure_window()
sound = SoundLoader.load('Assets/sounds/beep.mp3')
__version__ = '0.2.4'
count = 0
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
    curSavefile = ""
    save = ObjectProperty(None)
    text_input = ObjectProperty(None)
    cancel = ObjectProperty(None)


class TitleScreen(Screen):
	pass


class NewOrOldFile(BoxLayout):
    newTab = ObjectProperty(None)
    oldTab = ObjectProperty(None)


class CreateScreen(Screen):
    slide = ObjectProperty(None)
    volSlider = ObjectProperty(None)
    bpsSlider = ObjectProperty(None)
    active_setting = ObjectProperty(None)
    loadfile = ObjectProperty(None)
    savefile = ObjectProperty(None)
    tabarea = ObjectProperty(None)
    curDirectory = os.path.dirname(os.path.realpath(__file__))
    checkbox = CheckBox()
    text_input = ObjectProperty(None)
    tabCanvas = ObjectProperty(None)

    # Basic blank tab for new tab files
    # Must not have extra lines! If it has 6 strings, use 6 lines!
    blankBarOneString = "|--------------------|"
    blankTab = blankBarOneString
    blankTab += ("\n" + blankBarOneString) * 5

    # When entering create screen, prompts user to pick an existing file to edit
    #  or to create a new file
    def on_enter(self):
		# starts the file manager when this screen is entered
        #self.tabarea.edit_toolbar = EditToolbar(root=self)
        #self.add_widget(self.tabarea.edit_toolbar)
        content = NewOrOldFile(newTab=self.newTab, oldTab=self.oldTab)
        self._popup = Popup(title="File Type", content=content, size_hint=(0.4, 0.4))
        self._popup.open()

    # Allow user to pick location for the new file and give it a name
    def newTab(self):
        print("Open a new tab")
        content = SaveDialog(save=self.makeBlankTab, cancel=self.dismiss_popup)
        self._popup.dismiss()
        self._popup = Popup(title="Make a New Tab", content=content, size_hint=(0.4, 0.8))
        self._popup.open()

    # Writes to the blank tab the user creates, and loads it into edit mode
    def makeBlankTab(self, path, filename):
        if filename[-4::] != ".txt":
            filename += ".txt"
        with open(os.path.join(path, filename), 'w') as stream:
            print(filename)
            stream.write(self.blankTab)
            self._popup.dismiss()
        # Hacky filename in brackets to get load to work
        self.load(path, [filename])

    # Opens an existing tab into edit mode
    def oldTab(self):
        print("Open an existing tab")
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup.dismiss()
        self._popup = Popup(title="Load File", content=content, size_hint=(0.4, 0.8))
        self._popup.open()

    # The popup is dismissed and the title screen is shown
    def dismiss_popup(self):
        self._popup.dismiss()
        self.manager.current = 'Title'

    # Load the file given a path and the filename
    def load(self, path, filename):
        #loads the file
        tab = os.path.join(path, filename[0])
        self._popup.dismiss()

        # Draws tab in the CreateScreen's tabArea, which is editable by default
        #   for the Create Screen
        self.tabarea.drawtab(tab)
        self.tabarea.setEditable()

    # Allow user to save a file
    def show_save(self):
        content = SaveDialog(save=self.save, cancel=self.dismiss_popupSave)
        self._popup = Popup(title="Save file", content=content, size_hint=(0.9, 0.9))
        self._popup.open()

    # Tester file-saving function
    def save(self, path, filename):
        with open(os.path.join(path, filename), 'w') as stream:
            print(filename)
            stream.write(filename)
            self.dismiss_popupSave()

    def on_checkbox_active(self, *args):
        print(args[2])
        if args[2]:
            print("active")
        self.checkbox._toggle_active()

    def play_pause(self, *args):
        if args[0].state == 'down':
            print(self.bpsSlider.value)
            #beeps self.bpsSlider per second
            Clock.schedule_interval(self.play_metro, 60/(self.bpsSlider.value))
        else:
            Clock.unschedule(self.play_metro)
            sound.stop()

    # Play the metronome
    def play_metro(self,dt):
        #Trying to get the scroll view to be animated by button press
        #right now just moving the slider

        # One dead puppy per global
        global move_value
        move_value += .01
        self.tabarea.slide.value = move_value
        sound.volume =int(self.volSlider.value)
        sound.play()


class ViewScreen(Screen):
    slide = ObjectProperty(None)
    volSlider = ObjectProperty(None)
    bpsSlider = ObjectProperty(None)
    active_setting = ObjectProperty(None)
    loadfile = ObjectProperty(None)
    savefile = ObjectProperty(None)
    tabarea = ObjectProperty(None)
    curDirectory = os.path.dirname(os.path.realpath(__file__))
    checkbox = CheckBox()
    text_input = ObjectProperty(None)

    def on_enter(self):
        # starts the file manager when this screen is entered
        self.tabarea.setEditable(False)
        content = LoadDialog(load=self.load, cancel=self.dismiss_popupLoad)
        self._popup = Popup(title="Load file", content=content, size_hint=(0.4, 0.8))
        self._popup.open()

    def dismiss_popupLoad(self):
        self._popup.dismiss()
        self.manager.current = 'Title'

    def dismiss_popupSave(self):
        self._popup.dismiss()

    def load(self, path, filename):
        #loads the file
        tab = os.path.join(path, filename[0])
        self._popup.dismiss()
        # Draws tab in the ViewScreen's tabArea
        self.tabarea.drawtab(tab)

    def show_save(self):
        content = SaveDialog(save=self.save, cancel=self.dismiss_popupSave)
        print(self.save)
        self._popup = Popup(title="Save file", content=content, size_hint=(0.9, 0.9))
        self._popup.open()

    def save(self, path, filename):
        with open(os.path.join(path, filename), 'w') as stream:
            stream.write(filename)
            self.dismiss_popupSave()

    def on_checkbox_active(self, *args):
        self.checkbox._toggle_active()

    def play_pause(self, *args):
        if args[0].state == 'down':
            #beeps self.bpsSlider per second
            Clock.schedule_interval(self.play_metro, 60/(self.bpsSlider.value))
        else:
            Clock.unschedule(self.play_metro)
            sound.stop()

    def play_metro(self,dt):
        #Trying to get the scroll view to be animated by button press
        #right now just moving the slider
        # One dead puppy per global
        global move_value
        move_value += .01
        #move_value = .5
        self.tabarea.slide.value = move_value
        sound.volume =int(self.volSlider.value)
        sound.play()


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

        self.nav_menu = NavMenu(root=self)
        self.add_widget(self.nav_menu)
        # Add the screen to the middle.
        #self.add_widget(self.content)
        self.add_widget(self.root)

    def set_current_screen(self, jump_to):
        self.root.current = jump_to


Builder.load_file("screens/navmenu.kv")


class NavMenu(BoxLayout):

    def __init__(self, root, **kwargs):
        super(NavMenu, self).__init__(**kwargs)
        self.root = root

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
