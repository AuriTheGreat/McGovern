import ScenarioHandler
import ResultHandler
import os
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
            'normal': '#ffffff',
            'hover': '#666666',
            'pressed': '#333333',
        }

        self.buttonSurface = pygame.Surface((self.width, self.height))
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.buttonSurf = font.render(buttonText, True, (20, 20, 20))

        self.alreadyPressed = False

        objects.append(self)

    def process(self):

        mousePos = pygame.mouse.get_pos()
        
        self.buttonSurface.fill(self.fillColors['normal'])
        if self.buttonRect.collidepoint(mousePos):
            self.buttonSurface.fill(self.fillColors['hover'])

            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                self.buttonSurface.fill(self.fillColors['pressed'])

                if self.onePress:
                    self.onclickFunction()

                elif not self.alreadyPressed:
                    self.onclickFunction()
                    self.alreadyPressed = True

            else:
                self.alreadyPressed = False

        self.buttonSurface.blit(self.buttonSurf, [
            self.buttonRect.width/2 - self.buttonSurf.get_rect().width/2,
            self.buttonRect.height/2 - self.buttonSurf.get_rect().height/2
        ])
        screen.blit(self.buttonSurface, self.buttonRect)


def mainmenu():
    objects.clear()
    Button(width/2-200, 30, 400, 100, 'Button One (onePress)', choosescenario)
    Image(width/2-200, 10, 200, 50, 'gfx/title.png')


def choosescenario():
    objects.clear()
    Button(width/2-200, 130, 400, 100, 'Button One (onePress)', mainmenu)
    for i in scenarios:
        Button(width/2-200, 230, 400, 100, i)




if __name__ == "__main__":
    scenarios=os.listdir('scenario')
    scenarios=getvalidscenarios(scenarios)
    scenarioname=getscenario(scenarios)
    scenario=ScenarioHandler.main(scenarioname)

    results=ResultHandler.main(scenario)

    pygame.init()
    fps = 60
    fpsClock = pygame.time.Clock()
    width, height = 640, 480
    screen = pygame.display.set_mode((width, height))
    
    font = pygame.font.SysFont('Arial', 40)

    objects = []

    mainmenu()
    
    # Game loop.
    while True:
        screen.fill((20,20,20))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
    
        for object in objects:
            object.process()
    
        pygame.display.flip()
        fpsClock.tick(fps)