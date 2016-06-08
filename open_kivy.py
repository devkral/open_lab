#! /usr/bin/env python3

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Rectangle
from kivy.core.image import Image

from openthelab import dostuff, _token
iamugly=True

class ButtonRow(GridLayout):
    def __init__ (self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if iamugly:
            self.ids.openb.background_normal = 'Augenkrebs.jpg'
            self.ids.closeb.background_normal = 'Augenkrebs.jpg'
    def dostuff2(self, action):
        dostuff(action)
        self.parent.ids.statel.text = self.parent.status()

class MainWin(GridLayout):
    def __init__ (self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if _token != "":
            self.add_widget(ButtonRow())
        else:
            self.add_widget(Label("No token under: ./token"))
    def status(self):
        ret = dostuff("state")
        if ret:
            return ret
        else:
            return "Error"

class open_kivy(App):
    def build(self):
        self.title = "Augenkrebs"
        self.icon = "Augenkrebs.jpg"
        return MainWin()
if __name__ == '__main__':
    open_kivy().run()
