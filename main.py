#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

from functools import partial
import os
import random

import kivy
kivy.require('1.8.0')

from kivy.config import Config
Config.set('graphics', 'width', '1280')
Config.set('graphics', 'height', '480')

from kivy.app import App
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.clock import mainthread
from kivy.graphics import Color
from kivy.graphics import Line
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
from kivy.uix.scrollview import ScrollView
from kivy.properties import StringProperty

import os

__version__ = '0.2.4'


#slides = ["Title", "WhatIsKivy", "MobileToolchain"]
slides = ["Title", "CreateScreen", "ViewScreen"]
for slide in slides:
    kv_file = "{}.kv".format(slide.lower())
    Builder.load_file(os.path.join("screens", kv_file))

class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)

class SaveDialog(FloatLayout):
    save = ObjectProperty(None)
    #text_input = ObjectProperty(None)
    cancel = ObjectProperty(None)

class TitleScreen(Screen):
    test_string = StringProperty("adsfasdfasdf")
    loadfile = ObjectProperty(None)
    savefile = ObjectProperty(None)
    #text_input = ObjectProperty(None)

    def dismiss_popup(self):
        self._popup.dismiss()

    def show_load(self):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        print(content)
        print(self.load)
        self._popup = Popup(title="Load file", content=content, size_hint=(0.6, 0.8))
        self._popup.open()

    def show_save(self):
        content = SaveDialog(save=self.save, cancel=self.dismiss_popup)
        print(self.save)
        self._popup = Popup(title="Save file", content=content, size_hint=(0.9, 0.9))
        self._popup.open()

    def go_to_create(self):
        self.content.set_current_slide('ViewScreen')

    def load(self, path, filename):
        print("inside load def")
        with open(os.path.join(path, filename[0])) as stream:
            self.test_string = stream.read()
        self.dismiss_popup()
        #root.set_current_slide('WhatIsKivy')
        #self._popup = Popup(title="Load file", content=Label(text = 'File Loaded Successfully'), size_hint=(0.9, 0.9))
        #self._popup.open()
    pass

class CreateScreen(Screen):
    def on_enter(self):
        print('Enter create screen')
        
class Test(Screen):
    test_string = StringProperty("adsfasdfasdf")
    loadfile = ObjectProperty(None)
    savefile = ObjectProperty(None)
    def on_enter(self):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        print(content)
        print(self.load)
        self._popup = Popup(title="Load file", content=content, size_hint=(0.6, 0.8))
        self._popup.open()


    #text_input = ObjectProperty(None)

    def dismiss_popup(self):
        self._popup.dismiss()

    def show_load(self):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        print(content)
        print(self.load)
        self._popup = Popup(title="Load file", content=content, size_hint=(0.6, 0.8))
        self._popup.open()

    def show_save(self):
        content = SaveDialog(save=self.save, cancel=self.dismiss_popup)
        print(self.save)
        self._popup = Popup(title="Save file", content=content, size_hint=(0.9, 0.9))
        self._popup.open()

    def go_to_create(self):
        self.content.set_current_slide('ViewScreen')

    def load(self, path, filename):
        print("inside load def")
        with open(os.path.join(path, filename[0])) as stream:
            self.test_string = stream.read()
        self.dismiss_popup()
        #root.set_current_slide('WhatIsKivy')
        #self._popup = Popup(title="Load file", content=Label(text = 'File Loaded Successfully'), size_hint=(0.9, 0.9))
        #self._popup.open()
    pass

class ViewScreen(Screen):    
    test_string = StringProperty("adsfasdfasdf")
    loadfile = ObjectProperty(None)
    savefile = ObjectProperty(None)
    def on_enter(self):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        print(content)
        print(self.load)
        self._popup = Popup(title="Load file", content=content, size_hint=(0.6, 0.8))
        self._popup.open()


    #text_input = ObjectProperty(None)

    def dismiss_popup(self):
        self._popup.dismiss()

    def show_load(self):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        print(content)
        print(self.load)
        self._popup = Popup(title="Load file", content=content, size_hint=(0.6, 0.8))
        self._popup.open()

    def show_save(self):
        content = SaveDialog(save=self.save, cancel=self.dismiss_popup)
        print(self.save)
        self._popup = Popup(title="Save file", content=content, size_hint=(0.9, 0.9))
        self._popup.open()

    def go_to_create(self):
        self.content.set_current_slide('ViewScreen')

    def load(self, path, filename):
        print("inside load def")
        with open(os.path.join(path, filename[0])) as stream:
            self.test_string = stream.read()
        self.dismiss_popup()
        #root.set_current_slide('WhatIsKivy')
        #self._popup = Popup(title="Load file", content=Label(text = 'File Loaded Successfully'), size_hint=(0.9, 0.9))
        #self._popup.open()
    pass          

#main widget of the app
class KivyPres(BoxLayout):
    def __init__(self, **kwargs):
        super(KivyPres, self).__init__(**kwargs)
        self.orientation = 'vertical'

        self.content = ScreenManager()
        self.content.add_widget(TitleScreen(name='Title'))
        self.content.add_widget(CreateScreen(name='CreateScreen'))
        self.content.add_widget(ViewScreen(name="ViewScreen"))

        #add the nav bar to the top
        self.slide_menu = NavMenu(root=self)
        self.add_widget(self.slide_menu)
        #add the screen to the middle.
        self.add_widget(self.content)
  
    def get_current_slide(self):
        print 'test1'
        #return self.content.current
    
    def set_current_slide(self, jump_to):
        print 'test2'
        self.content.current = jump_to

Builder.load_file("navmenu.kv")
class NavMenu(BoxLayout):
    slide_spinner = ObjectProperty(None)
    
    def __init__(self, root, **kwargs):
        super(NavMenu, self).__init__(**kwargs)
        self.root = root
        self.slide_spinner.values = slides
        
    def go_slide(self, spinner):
        if spinner.text in slides:
            self.root.set_current_slide(spinner.text)
    #goes to kivypress.        
    def go_create(self):
        self.root.set_current_slide('CreateScreen')
        
    def go_view(self):
        self.root.set_current_slide('ViewScreen')


# Declare both screens
class MenuScreen(Screen):
    print "test main screen"
    pass

class SettingsScreen(Screen):
    pass

class KivyPresApp(App):
    font_size_regular = sp(25)

    def build(self):
        return KivyPres()
    
    def on_pause(self):
        print "PAUSE"
        return True
        
    def on_resume(self):
        print "RESUME"
        pass
    
    def open_browser(self, url):
        browser.open_url(url)


if __name__ == '__main__':
    KivyPresApp().run()
