from re import A
from turtle import screensize
import source.UserInterface.Main as UI
import source.ScenarioHandler.Main as ScenarioHandler
import source.ResultHandler as ResultHandler
import source.TriggerHandler as TriggerHandler
import os
import sys
import math
import threading
import pygame
import time
import pygame.freetype
from pygame.locals import *

def getvalidscenarios(scenarios):
    validscenarios=[]
    for i in scenarios:
        files=os.listdir('scenario/'+i)
        if set(['gfx', 'parties.txt', 'characters.txt', 'main.txt', 'regions.txt', 'populations.txt', 'ideologies.txt', 'traits.txt', 'outcomes.txt', 'events.txt', 'issues.txt', 'partyregion.txt']).issubset(files):
            validscenarios.append(i)
    return validscenarios


#####################################################################################
##################################### Main loop #####################################
#####################################################################################

if __name__ == "__main__":
    if 'scenario' in os.listdir():
        scenarios=os.listdir('scenario')
    else:
        sys.exit("ERROR: no scenario folder found")
    UI.UIState.scenarios=getvalidscenarios(scenarios)
    pygame.display.set_caption('McGovern')
    pygame.display.set_icon(pygame.image.load('resources/gfx/icon.png'))
    fps = 30
    fpsClock = pygame.time.Clock()

    pygame.init()
    UI.UIState.mainfont = pygame.freetype.SysFont(UI.UIState.mainfontstyle, UI.UIState.mainfontsize)
    UI.callscreen()
    
    # Game loop.
    while True:
        UI.UIState.screen.fill((20,20,20))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                break
    
        if UI.UIState.nextscreen:
            UI.callscreen(UI.UIState.nextscreen, UI.UIState.nextscreenparameters)

        for object in UI.UIState.objects:
            object.process()

        if UI.UIState.objects:
            pygame.display.flip()
        fpsClock.tick(fps)
        #print(fpsClock.get_fps())