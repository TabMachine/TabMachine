#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

from functools import partial
import os
import random

import kivy
kivy.require('1.8.0')

from kivy.config import Config
Config.set('graphics', 'width', '1400')
Config.set('graphics', 'height', '420')

from kivy.app import App
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.clock import mainthread
from kivy.lang import Builder
from kivy.logger import Logger
from kivy.metrics import sp
from kivy.properties import NumericProperty
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty
from kivy.uix.accordion import AccordionItem
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.codeinput import CodeInput
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.scatter import Scatter
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
from functools import partial

import os
EventLoop.ensure_window()
__version__ = '0.2.4'

screens = ["Title", "CreateScreen", "ViewScreen"]
for screen in screens:
    kv_file = "{}.kv".format(screen.lower())
    Builder.load_file(os.path.join("screens", kv_file))

class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)

class SaveDialog(FloatLayout):
    save = ObjectProperty(None)
    #text_input = ObjectProperty(None)
    cancel = ObjectProperty(None)

class TitleScreen(Screen):
    pass

class CreateScreen(Screen):
    def on_enter(self):
        print('Enter create screen')

class ViewScreen(Screen):
    loadfile = ObjectProperty(None)
    savefile = ObjectProperty(None)

    def on_enter(self):
        # starts the file manager when this screen is entered
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content, size_hint=(0.4, 0.6))
        self._popup.open()

    def dismiss_popup(self):
        self._popup.dismiss()

    def load(self, path, filename):
        #loads the file
        tab = open(os.path.join(path, filename[0]))
        self._popup.dismiss()

        # Draw the tab on the screen
        wid = Widget(size_hint=(10, 1), pos=(0.5, 0))
        self.drawtab(tab, wid)

        slide = Slider(min=0, max=1, value=25, orientation='horizontal', step=0.01, size_hint=(1, 0.1))
        slide.bind(value=partial(self.scroll_change, slide))

        scrl = ScrollView()
        scrl.bind(scroll_x=partial(self.slider_change, slide))
        scrl.add_widget(wid)

        self.add_widget(slide)
        self.add_widget(scrl)

    def show_save(self):
        content = SaveDialog(save=self.save, cancel=self.dismiss_popup)
        print(self.save)
        self._popup = Popup(title="Save file", content=content, size_hint=(0.9, 0.9))
        self._popup.open()

    def drawtab(self, tab, wid):
        charwidth = 32
        charheight = 32
        lineheight = 32
        startheight = 500
        i = 0

        # Get path to current file to find atlas file
        curdir = os.path.dirname(os.path.realpath(__file__))
        #test print
        print(curdir + r"/Assets/main.atlas")
        atlas = Atlas(curdir + r"/Assets/main.atlas")

        for line in tab:
            # Parse by character, translating input to graphical output
            with wid.canvas:
                for j in range(len(line)):
                    thischar = line[j]
                    print(thischar)
                    if thischar == '\n' or thischar == ':':
                        pass
                    elif j == 0:
                        # T bar
                        Rectangle(source='atlas://Assets/main/tbar',
                                  pos=(0, startheight-(i*lineheight)),
                                  size=(32, 32))
                    elif thischar == "|" and j > 0:
                        # Plus bar
                        print("Making vertical line")
                        Rectangle(source='atlas://Assets/main/plusbar',
                                  pos=(j*charwidth, startheight-(i*lineheight)),
                                  size=(32, 32))
                    elif thischar == "-":
                        # Horizontal line
                        print("Making horizontal line")
                        Rectangle(source='atlas://Assets/main/bar',
                                  pos=(j*charwidth, startheight-(i*lineheight)),
                                  size=(32, 32))
                    elif int(thischar) >= 0 and int(thischar) <= 24:
                        print("Making " + thischar)
                        Rectangle(source=('atlas://Assets/main/norm' + thischar),
                                  pos=(j*charwidth, startheight-(i*lineheight)),
                                  size=(32, 32))
                    else:
                        print("Can't draw it yet")

            # Increment counter
            i += 1

    def scroll_change(self, scrl, instance, value):
        scrl.scroll_x = value

    def slider_change(self, slide, instance, value):
        if value >= 0:
            slide.value = value

#main widget of the app
class TabMachine(BoxLayout):
    def __init__(self, **kwargs):
        super(TabMachine, self).__init__(**kwargs)
        self.orientation = 'vertical'
        # Adds the screen manager to the main app
        self.content = ScreenManager()
        self.content.add_widget(TitleScreen(name='Title'))
        self.content.add_widget(CreateScreen(name='CreateScreen'))
        self.content.add_widget(ViewScreen(name='ViewScreen'))
        # Displays in the order of adds
        # Add the nav bar to the top
        self.slide_menu = NavMenu(root=self)
        self.add_widget(self.slide_menu)
        # Add the screen to the middle.
        self.add_widget(self.content)

    def get_current_slide(self):
        print('test1')
        #return self.content.current

    def set_current_slide(self, jump_to):
        self.content.current = jump_to

Builder.load_file("navmenu.kv")
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
        self.root.set_current_slide('CreateScreen')

    def go_view(self):
        self.root.set_current_slide('ViewScreen')

class TabMachineApp(App):
    font_size_regular = sp(25)

    def build(self):
        return TabMachine()

if __name__ == '__main__':
    TabMachineApp().run()
