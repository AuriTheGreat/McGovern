import ScenarioHandler
import ResultHandler
import os
import math
import pygame
from pygame.locals import *



def getvalidscenarios(scenarios):
    validscenarios=[]
    for i in scenarios:
        files=os.listdir('scenario/'+i)
        if set(['parties.txt', 'characters.txt', 'main.txt', 'regions.txt', 'populations.txt', 'ideologies.txt', 'outcomes.txt', 'events.txt', 'issues.txt', 'partyregion.txt']).issubset(files):
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

class ImageButton():
    def __init__(self, x, y, width, height, img, buttonText='Button', onclickFunction=None):
            self.x = x
            self.y = y
            self.width = width
            self.height = height
            self.img = img
            self.buttonText=buttonText
            self.onclickFunction=onclickFunction

            self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)

            objects.append(self)

    def process(self):
        mousePos = pygame.mouse.get_pos()
        global isclicked
        
        image = pygame.image.load(self.img).convert_alpha()
        image = pygame.transform.scale(image,(self.width, self.height))

        if self.buttonRect.collidepoint(mousePos):
            brighten = 50
            image.fill((brighten, brighten, brighten), special_flags=pygame.BLEND_RGB_SUB)
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                if isclicked==False:
                    self.onclickFunction()
                    isclicked=True

            else:
                isclicked=False

        textsurface = font.render(self.buttonText, True, (255,255,255))

        image.blit(textsurface, [
            self.width/2 - textsurface.get_rect().width/2,
            self.height/2 - textsurface.get_rect().height/2
        ])

        screen.blit(image, (self.x,self.y))
        #screen.blit(textsurface, (self.x+self.width/2,self.y+self.height/2))




def mainmenu():
    objects.clear()
    #Rectangle(0,screen_width/(1200/250),screen_width,screen_height-(screen_height/(700/250)), '#D4FFFD')
    Image(0,screen_width/(1200/250),screen_width,screen_height-(screen_height/(700/250)), 'gfx/menu.png')
    button_size_x, button_size_y = screen_width/(1200/400), screen_height/(700/90)
    ImageButton(screen_width/2-(button_size_x/2), screen_width/(1200/300), button_size_x, button_size_y, 'gfx/button.png', 'Play', choosescenario)
    ImageButton(screen_width/2-(button_size_x/2), screen_width/(1200/400), button_size_x, button_size_y, 'gfx/button.png', 'Options', options)
    ImageButton(screen_width/2-(button_size_x/2), screen_width/(1200/500), button_size_x, button_size_y, 'gfx/button.png', 'Quit', quit)
    Image(0, screen_width/(1200/10), screen_width, screen_width/4.8, 'gfx/title.png')


testscenarios=["nice", "indeed", "hello", "good", "fun", "destroy", "life", "great", "alright", "minecraft", "uk1970", "yes",
               "scenario", "betterscenario", "worstscenario", "bestscenario", "indeed", "i like it", "yes"]

def choosescenario():
    objects.clear()
    button_size_x, button_size_y = screen_width/(1200/400), screen_height/(700/90)
    tile_size_x, tile_size_y = screen_width/(1200/200), screen_height/(700/200)
    Button(screen_width/2-(button_size_x/2), screen_width/(1200/550), button_size_x, button_size_y, 'Go back', mainmenu)

    objects_per_row=5
    rows=3
    x_outline, y_outline= screen_width/(1200/100),screen_height/(700/200)
    tile_size_x=(screen_width-(objects_per_row*5+x_outline))/objects_per_row
    tile_size_y=(screen_height-(objects_per_row*5+y_outline))/objects_per_row

    for count, i in enumerate(testscenarios):
        Button(screen_width/(1200/(x_outline/2))+(tile_size_x+5)*(count%objects_per_row), screen_height/(700/(y_outline/2))+(tile_size_y+5)*math.floor(count/objects_per_row), tile_size_x, tile_size_y, i , None)


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
                break
    
        for object in objects:
            object.process()
    
        pygame.display.flip()
        fpsClock.tick(fps)