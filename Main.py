from re import A
from turtle import screensize
import source.UserInterface.Views as UI
import source.ScenarioHandler.Main as ScenarioHandler
import source.ResultHandler.Main as ResultHandler
import source.TriggerHandler as TriggerHandler
import os
import sys
import pygame
import pygame.freetype
from pygame.locals import *

def getvalidscenarios(scenarios):
    validscenarios=[]
    for i in scenarios:
        files=os.listdir('scenario/'+i)
        if set(['gfx', 'parties.txt', 'characters.txt', 'main.txt', 'regions.txt', 'populations.txt', 'issues.txt']).issubset(files):
            validscenarios.append(i)
    return validscenarios

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


#####################################################################################
##################################### Main loop #####################################
#####################################################################################

if __name__ == "__main__":
    #Checks if scenario folder exists.
    if 'scenario' in os.listdir():
        scenarios=os.listdir('scenario')
    else:
        sys.exit("ERROR: no scenario folder found")

    #Creates an object of a class, which will be responsible for tracking current state of the UI.
    UIState=UserInterfaceState()
    UIState.scenarios=getvalidscenarios(scenarios)
    #Sets main things to do with pygame window.
    pygame.display.set_caption('McGovern')
    pygame.display.set_icon(pygame.image.load('resources/gfx/icon.png'))
    #Tracks the amount of objects to ensure that screen does not go black for a single frame.
    objectcounts=[]
    objectcount=5
    #Sets frames per second
    fps = 30
    fpsClock = pygame.time.Clock()
    #Initializes pygame
    pygame.init()
    UIState.mainfont = pygame.freetype.SysFont(UIState.mainfontstyle, UIState.mainfontsize) #must be done when initialized
    UI.mainmenu(UIState)
    
    # Game loop.
    while True:
        UIState.screen.fill((20,20,20))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        for object in UIState.objects:
            object.process()

        #This segment seeks to avoid displaying the screen while not all objects are loaded. This is
        #done by supressing display if actual objectcount does not match the previous count. If the
        #object count is consistent for 2 frames, then display is continued.
        newobjectcount=len(UIState.objects)
        if newobjectcount and not objectcounts and newobjectcount==objectcount:
            pygame.display.flip()
            objectcount=newobjectcount
        else:
            #print("POSSIBLE BLACK OUT:", len(UI.UIState.objects), objectcount, objectcounts )
            objectcount=newobjectcount
            if len(objectcounts)==2:
                if len(set(objectcounts))==1:
                    objectcounts.clear()
                else:
                    objectcounts.clear()
                    objectcounts.append(objectcount)
            else:
                objectcounts.append(objectcount)
                
        fpsClock.tick(fps)
        #print(fpsClock.get_fps())