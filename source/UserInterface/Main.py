import pygame
import pygame.freetype
from pygame.locals import *
import source.UserInterface.Views as s

class UserInterfaceState():
    def __init__(self):
        self.screen_width = 1200
        self.screen_height = 700
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.mainfontstyle='Arial'
        self.mainfontsize=int(self.screen_height/(700/40))
        self.mainfont = None
        self.scenarios = []
        self.objects = []
        self.windowhistory=[]
        self.openwindows = []
        self.isclicked=False
        self.calculating=False
        self.nextscreen, self.nextscreenparameters=None, []

UIState=UserInterfaceState()

def callscreen(screen=s.mainmenu, newparameters=[]):
    global UIState
    UIState.nextscreen, UIState.nextscreenparameters=None, []
    parameters=[UIState]
    parameters.extend(newparameters)
    UIState=screen(*parameters)
    if UIState.nextscreen!=None:
        callscreen(UIState.nextscreen, UIState.nextscreenparameters)
