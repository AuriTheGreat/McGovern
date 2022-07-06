import ScenarioHandler
import ResultHandler
import os
import time
import pygame
from pygame.locals import *



def getvalidscenarios(scenarios):
    validscenarios=[]
    for i in scenarios:
        files=os.listdir('scenario/'+i)
        if set(['parties.txt', 'characters.txt', 'main.txt', 'regions.txt', 'populations.txt', 'ideologies.txt', 'outcomes.txt', 'events.txt', 'issues.txt']).issubset(files):
            validscenarios.append(i)
    return validscenarios

def getscenario(scenarios):
    while True:
        print("Scenarios:", ', '.join([i for i in scenarios]))
        answer = input("Which scenario would you like to play? ").lower()
        if answer in scenarios:
            return answer
        else:
            print("Wrong input: scenario name needed.")

class Rectangle():
    def __init__(self, x, y, width, height, color):
            self.x = x
            self.y = y
            self.width = width
            self.height = height
            self.color = color

            objects.append(self)

            self.Surface = pygame.Surface((self.width, self.height))
            self.Surface.fill(self.color)
            self.Rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def process(self):
        screen.blit(self.Surface, self.Rect)

class Image():
    def __init__(self, x, y, width, height, img):
            self.x = x
            self.y = y
            self.width = width
            self.height = height
            self.img = img

            objects.append(self)

    def process(self):
        image = pygame.image.load(self.img)
        image = pygame.transform.scale(image,(self.width, self.height))
        screen.blit(image, (self.x,self.y))
        

class Button():
    def __init__(self, x, y, width, height, buttonText='Button', onclickFunction=None, onePress=False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.onclickFunction = onclickFunction
        self.onePress = onePress

        self.fillColors = {
            'normal': '#250045',
            'hover': '#666666',
            'pressed': '#333333',
        }

        self.buttonSurface = pygame.Surface((self.width, self.height))
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.buttonSurf = font.render(buttonText, True, (255, 255, 255))

        self.alreadyPressed = False

        objects.append(self)

    def process(self):

        mousePos = pygame.mouse.get_pos()
        global isclicked
        
        self.buttonSurface.fill(self.fillColors['normal'])
        if self.buttonRect.collidepoint(mousePos):
            self.buttonSurface.fill(self.fillColors['hover'])

            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                self.buttonSurface.fill(self.fillColors['pressed'])

                if self.onePress:
                    self.onclickFunction()

                elif not self.alreadyPressed:
                    if isclicked==False:
                        self.onclickFunction()
                        self.alreadyPressed = True
                        isclicked=True

            else:
                self.alreadyPressed = False
                isclicked=False

        self.buttonSurface.blit(self.buttonSurf, [
            self.buttonRect.width/2 - self.buttonSurf.get_rect().width/2,
            self.buttonRect.height/2 - self.buttonSurf.get_rect().height/2
        ])

        screen.blit(self.buttonSurface, self.buttonRect)


def mainmenu():
    objects.clear()
    Rectangle(0,screen_width/(1200/250),screen_width,screen_height, '#D4FFFD')
    button_size_x, button_size_y = screen_width/3, screen_height/(700/90)
    Button(screen_width/2-(button_size_x/2), screen_width/(1200/300), button_size_x, button_size_y, 'Play', choosescenario)
    Button(screen_width/2-(button_size_x/2), screen_width/(1200/400), button_size_x, button_size_y, 'Options', options)
    Button(screen_width/2-(button_size_x/2), screen_width/(1200/500), button_size_x, button_size_y, 'Quit', quit)
    Image(0, screen_width/(1200/10), screen_width, screen_width/4.8, 'gfx/title.png')


def choosescenario():
    objects.clear()
    Button(screen_width/2-200, 130, 400, 100, 'Go back', mainmenu)
    for i in scenarios:
        Button(screen_width/2-200, 230, 400, 100, i)

def options():
    objects.clear()
    Button(screen_width/2-200, 130, 400, 100, 'Go back', mainmenu)

def quit():
    pygame.quit()


if __name__ == "__main__":
    scenarios=os.listdir('scenario')
    scenarios=getvalidscenarios(scenarios)
    scenarioname=getscenario(scenarios)
    scenario=ScenarioHandler.main(scenarioname)

    results=ResultHandler.main(scenario)

    pygame.init()
    pygame.display.set_caption('McGovern')
    pygame.display.set_icon(pygame.image.load('gfx/icon.png'))
    fps = 30
    fpsClock = pygame.time.Clock()
    screen_width, screen_height = 1200, 700
    screen = pygame.display.set_mode((screen_width, screen_height))

    font = pygame.font.SysFont('Arial', int(screen_height/(700/40)))

    objects = []
    isclicked=False

    mainmenu()
    
    # Game loop.
    while True:
        screen.fill((20,20,20))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
    
        for object in objects:
            object.process()
    
        pygame.display.flip()
        fpsClock.tick(fps)