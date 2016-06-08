#! /usr/bin/env python3

from kivy.app import App
from kivy.uix.gridlayout import GridLayout

from openthelab import dostuff

class MainWin(GridLayout):
    
    def dostuff2(self, action):
        dostuff(action)
    
    def status(self):
        ret = dostuff("state")
        if ret:
            return ret
        else:
            return "Error"

class open_kivy(App):
    def build(self):
        return MainWin()
if __name__ == '__main__':
    open_kivy().run()
