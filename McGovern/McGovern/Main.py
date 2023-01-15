from re import A
import ScenarioHandler
import ResultHandler
import TriggerHandler
import os
import sys
import math
import pygame
import pygame.freetype
from pygame.locals import *

class GameData:
    def __init__(self, scenario, results=None, polling=None):
        self.scenario = scenario
        self.results = results
        self.polling = polling

def getvalidscenarios(scenarios):
    validscenarios=[]
    for i in scenarios:
        files=os.listdir('scenario/'+i)
        if set(['gfx', 'parties.txt', 'characters.txt', 'main.txt', 'regions.txt', 'populations.txt', 'ideologies.txt', 'outcomes.txt', 'events.txt', 'issues.txt', 'partyregion.txt']).issubset(files):
            validscenarios.append(i)
    return validscenarios

#####################################################################################
################################# Component classes #################################
#####################################################################################

class Rectangle():
    def __init__(self, x, y, width, height, color, text="", fontstyle=None, fontsize=None):
            self.x = x
            self.y = y
            self.width = width
            self.height = height
            self.color = color
            self.text = text

            if fontstyle!=None:
                self.fontstyle=fontstyle
            else:
                self.fontstyle=mainfontstyle
            if fontsize!=None:
                self.fontsize=int(screen_height/(700/fontsize))
            else:
                self.fontsize=mainfontsize

            self.font=pygame.freetype.SysFont(self.fontstyle, self.fontsize)

            while self.text!="": #Runs in case the font is too big for the rectangle
                self.font=pygame.freetype.SysFont(self.fontstyle, self.fontsize)      
                text_rect = self.font.get_rect(self.text)
                if text_rect.width<self.width and text_rect.height<self.height:
                    break
                else:
                    self.fontsize-=1

            objects.append(self)

            self.Surface = pygame.Surface((self.width, self.height))
            self.Surface.fill(self.color)
            self.Rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def process(self):
        screen.blit(self.Surface, self.Rect)

        text_rect = self.font.get_rect(self.text)
        text_rect.center = self.Surface.get_rect().center
        self.font.render_to(self.Surface, text_rect.topleft, self.text, (255,255,255))

        screen.blit(self.Surface, (self.x,self.y))

class Circle():
    def __init__(self, x, y, radius, color):
            self.x = x
            self.y = y
            self.radius = radius
            self.color = color

            objects.append(self)

    def process(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

class Image():
    def __init__(self, x, y, width, height, img):
            self.x = x
            self.y = y
            self.width = width
            self.height = height
            self.img = img

            self.image = pygame.image.load(self.img)
            self.image = pygame.transform.scale(self.image,(self.width, self.height)).convert()

            objects.append(self)

    def process(self):
        #print(self.image.get_at((2, 2)))
        screen.blit(self.image, (self.x,self.y))
        

class Button():
    def __init__(self, x, y, width, height, text='', onclickFunction=None, paramsFunction=[], color="#250045", onePress=False, fontstyle=None, fontsize=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.onclickFunction = onclickFunction
        self.paramsFunction = paramsFunction
        self.onePress = onePress
        self.color=color
        self.text=text

        self.buttonSurface = pygame.Surface((self.width, self.height))
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)

        #self.buttonSurf = mainfont.render(buttonText, True, (255, 255, 255))

        self.alreadyPressed = False

        if fontstyle!=None:
            self.fontstyle=fontstyle
        else:
            self.fontstyle=mainfontstyle
        if fontsize!=None:
            self.fontsize=int(screen_height/(700/fontsize))
        else:
            self.fontsize=mainfontsize

        self.font=pygame.freetype.SysFont(self.fontstyle, self.fontsize)
        while self.text!="": #Runs in case the font is too big for the rectangle
                self.font=pygame.freetype.SysFont(self.fontstyle, self.fontsize)      
                text_rect = self.font.get_rect(self.text)
                if text_rect.width<self.width and text_rect.height<self.height:
                    break
                else:
                    self.fontsize-=1

        objects.append(self)

    def process(self):

        mousePos = pygame.mouse.get_pos()
        global isclicked
        
        self.buttonSurface.fill(self.color)
        if self.buttonRect.collidepoint(mousePos):
            brighten = 50
            self.buttonSurface.fill((brighten, brighten, brighten), special_flags=pygame.BLEND_RGB_SUB)

            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                self.buttonSurface.fill((brighten, brighten, brighten), special_flags=pygame.BLEND_RGB_SUB)

                if self.onePress:
                    self.onclickFunction(*self.paramsFunction)

                elif not self.alreadyPressed:
                    if isclicked==False:
                        self.onclickFunction(*self.paramsFunction)
                        self.alreadyPressed = True
                        isclicked=True

            else:
                self.alreadyPressed = False
                isclicked=False

        text_rect = self.font.get_rect(self.text)
        text_rect.center = self.buttonSurface.get_rect().center
        self.font.render_to(self.buttonSurface, text_rect.topleft, self.text, (255,255,255))

        screen.blit(self.buttonSurface, self.buttonRect)

class ImageButton():
    def __init__(self, x, y, width, height, img, text='', onclickFunction=None, paramsFunction=[], fontstyle=None, fontsize=None):
            self.x = x
            self.y = y
            self.width = width
            self.height = height
            self.img = img
            self.text=text
            self.onclickFunction=onclickFunction
            self.paramsFunction=paramsFunction

            self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)

            if fontstyle!=None:
                self.fontstyle=fontstyle
            else:
                self.fontstyle=mainfontstyle
            if fontsize!=None:
                self.fontsize=int(screen_height/(700/fontsize))
            else:
                self.fontsize=mainfontsize

            self.font=pygame.freetype.SysFont(self.fontstyle, self.fontsize)
            while self.text!="": #Runs in case the font is too big for the rectangle
                self.font=pygame.freetype.SysFont(self.fontstyle, self.fontsize)      
                text_rect = self.font.get_rect(self.text)
                if text_rect.width<self.width and text_rect.height<self.height:
                    break
                else:
                    self.fontsize-=1

            objects.append(self)

    def process(self):
        mousePos = pygame.mouse.get_pos()
        global isclicked
        
        image = pygame.image.load(self.img)
        image = pygame.transform.scale(image,(self.width, self.height)).convert()

        self.newx, self.newy=round(self.x+((self.width-image.get_width())/2)), round(self.y+((self.height-image.get_height())/2))
        self.buttonRect = pygame.Rect(self.newx, self.newy, image.get_width(), image.get_height())

        if self.buttonRect.collidepoint(mousePos):
            color=image.get_at((mousePos[0]-self.newx, mousePos[1]-self.newy))
            if color!=(0,0,0,0) and color!=(0,0,0,255):
                brighten = 50
                image.fill((brighten, brighten, brighten), special_flags=pygame.BLEND_RGB_SUB)
                if pygame.mouse.get_pressed(num_buttons=3)[0]:
                    if isclicked==False:
                        self.onclickFunction(*self.paramsFunction)
                        isclicked=True

                else:
                    isclicked=False

        text_rect = self.font.get_rect(self.text)
        text_rect.center = image.get_rect().center
        self.font.render_to(image, text_rect.topleft, self.text, (255,255,255))

        screen.blit(image, (self.x,self.y))

class Map():
    def __init__(self, x, y, width, height, img, gamedata, colormode='main', party=None):
            self.x = x
            self.y = y
            self.width = width
            self.height = height
            self.img = img
            self.gamedata = gamedata
            self.colormode = colormode
            self.party = party

            objects.append(self)

    def process(self):
        mousePos = pygame.mouse.get_pos()
        global isclicked
        
        self.image = pygame.image.load(self.img)
        reducesizeby=max(self.image.get_width()/self.width, self.image.get_height()/self.height)
        self.image = pygame.transform.scale(self.image,(round(self.image.get_width()/reducesizeby), round(self.image.get_height()/reducesizeby))).convert()
        self.newx, self.newy=round(self.x+((self.width-self.image.get_width())/2)), round(self.y+((self.height-self.image.get_height())/2))
        self.buttonRect = pygame.Rect(self.newx, self.newy, self.image.get_width(), self.image.get_height())
        arr=pygame.PixelArray(self.image)

        if self.buttonRect.collidepoint(mousePos):
            color=self.image.get_at((mousePos[0]-self.newx, mousePos[1]-self.newy))
            if color!=(0,0,0,255):
                [arr.replace(color, (80,80,80)) for i in self.gamedata.scenario.regions]
                if pygame.mouse.get_pressed(num_buttons=3)[0]:
                    if isclicked==False:
                        regionview(self.gamedata.scenario.name, self.gamedata, next((x for x in self.gamedata.scenario.regions if x.color == color), None).name)
                        isclicked=True
                else:
                    isclicked=False
        
        if self.colormode=='main':
            [arr.replace(i.color, i.resultcolor) for i in self.gamedata.scenario.regions]
        elif self.colormode=='party':
            colors={}
            for i in [i for i in self.gamedata.polling.aggregated.partyregionresults if i.party.fullname==self.party.fullname]:
                multiplicator=i.percentage/max([j.percentage for j in self.gamedata.polling.aggregated.partyregionresults if j.party.fullname==self.party.fullname])
                colors[i.region.name]=tuple([max(40,j*multiplicator) for j in i.party.color])
            [arr.replace(i.color, colors[i.name]) for i in self.gamedata.scenario.regions]

        arr.close()

        #print(self.image.get_at((2, 2)))
        screen.blit(self.image, (self.newx, self.newy))

class MultipleLineText():
    def __init__(self, x, y, width, height, color, text="", fontstyle=None, fontsize=None):
            self.x = x
            self.y = y
            self.width = width
            self.height = height
            self.color = color
            self.text = text

            if fontstyle!=None:
                self.fontstyle=fontstyle
            else:
                self.fontstyle=mainfontstyle
            if fontsize!=None:
                self.fontsize=int(screen_height/(700/fontsize))
            else:
                self.fontsize=mainfontsize

            self.font=pygame.freetype.SysFont(self.fontstyle, self.fontsize)
            while text: #This loop is to decrease the font if the height is not enough
                self.text = text.copy()
                self.font=pygame.freetype.SysFont(self.fontstyle, self.fontsize)
                while True: #This loop is to divide the string in a way that it fits within the width
                    changed=False
                    newtext=[]
                    for count, i in enumerate(self.text):
                        text_rect = self.font.get_rect(i)
                        #print(i, "hello", text_rect.width, len(i))
                        if text_rect.width>self.width:
                            changed=True
                            if text_rect.width>self.width*2.5: #Generates a quicker split in case string is big
                                words=i.split()
                                newtext.append(" ".join(words[:-math.floor(len(words)/2)]))
                                newtext.append(" ".join(words[-math.floor(len(words)/2):]))
                                continue
                            words=i.split()
                            for j in range(len(words)):
                                if j==0:
                                    continue
                                testedtext=words[:-j] #sequentially reduces the string by removing last word
                                #print(testedtext, j)
                                text_rect = self.font.get_rect(" ".join(testedtext))
                                if text_rect.width>self.width:
                                    continue
                                else:
                                    newtext.append(" ".join(testedtext))
                                    if len(self.text)-1>count:
                                        if self.text[count+1]!="":
                                            self.text[count+1]=" ".join(words[-j:])+ " " + self.text[count+1]
                                        else:
                                            newtext.append(" ".join(words[-j:]))
                                    else:
                                        newtext.append(" ".join(words[-j:]))
                                    break
                        else:
                            newtext.append(i)
                    self.text=newtext
                    if not changed:
                        break
                totalheight=sum([self.font.get_rect(i).height for i in newtext])
                if totalheight<self.height:
                    self.text=newtext
                    break
                else:
                    self.fontsize-=1

            objects.append(self)

            self.Surface = pygame.Surface((self.width, self.height))
            self.Surface.fill(self.color)
            self.Rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def process(self):
        screen.blit(self.Surface, self.Rect)

        #text_rect = self.font.get_rect(self.text)
        #print(sum([self.font.get_rect(i).height for i in self.text]))
        previous_height_total=0
        heightofline=self.font.get_rect("Tg").height
        for i in self.text:
            text_rect = self.font.get_rect(i)
            text_rect.y+=previous_height_total+(heightofline-text_rect.height)/2
            previous_height_total+=heightofline

            self.font.render_to(self.Surface, text_rect.topleft, i, (255,255,255))

        """
        text_rect.center = self.Surface.get_rect().center
        self.font.render_to(self.Surface, text_rect.topleft, self.text, (255,255,255))
        """

        screen.blit(self.Surface, (self.x,self.y))

#####################################################################################
##################### Functions for adding groups of components #####################
#####################################################################################

def partysharechart(x, y, width, height, gamedata, region='National', mode='votes'):
    reachedsize=0
    sizes={}

    if region=='National':
        if mode=='votes':
            sizes={i:i.percentage/100*width for i in gamedata.polling.aggregated.totalpartyresults}
        else:
            sizes={i:i.seats/sum([j.seats for j in gamedata.polling.aggregated.totalpartyresults])*width for i in gamedata.polling.aggregated.totalpartyresults}
    else:
        partyregionresultslist=[j for j in gamedata.polling.aggregated.partyregionresults if j.region.name==region and j.votes>0]
        if mode=='votes':
            sizes={i:i.percentage/100*width for i in partyregionresultslist}
        else:
            sizes={i:i.seats/sum([j.seats for j in partyregionresultslist])*width for i in partyregionresultslist}

    while sum([int(i) for i in sizes.values()])<width:
        maximal=max([i%1 for i in sizes.values()])
        for i in sizes:
            if sizes[i]%1==maximal:
                sizes[i]=math.ceil(sizes[i])
                break

    sizes={i:int(sizes[i]) for i in sizes}


    if region=='National':
        for i in gamedata.polling.aggregated.totalpartyresults:
            Rectangle(x+reachedsize,y,sizes[i], height, i.party.color)
            reachedsize+=sizes[i]
    else:
        partyregionresultslist=[j for j in gamedata.polling.aggregated.partyregionresults if j.region.name==region and j.votes>0]
        for i in partyregionresultslist:
            size=i.percentage/100*width
            Rectangle(x+reachedsize,y,sizes[i], height, i.party.color)
            reachedsize+=sizes[i]

    #25%, 50% and 75% markers on vote charts
    Rectangle(x+width/4,y, width/(360/1), height/(50/5), (255,255,255))
    Rectangle(x+width/4,y+(height-height/(50/5)), width/(360/1), height/(50/5), (255,255,255))

    Rectangle(x+width/2,y, width/(360/1), height/(50/5), (255,255,255))
    Rectangle(x+width/2,y+(height-height/(50/5)), width/(360/1), height/(50/5), (255,255,255))

    Rectangle(x+width/2+width/4,y, width/(360/1), height/(50/5), (255,255,255))
    Rectangle(x+width/2+width/4,y+(height-height/(50/5)), width/(360/1), height/(50/5), (255,255,255))

def parliamentarychart(x, y, width, height, gamedata, mode='westminster', rulingparties=None, speaker=None, columns=8):
    y+=height/2


    rulingparties=[i for i in gamedata.scenario.parties if i.ruling==True]

    if len(rulingparties)==0:
        maximalseats=max([i.nationalseats for i in gamedata.scenario.parties])
        rulingparties=[i for i in gamedata.scenario.parties if i.nationalseats==maximalseats][0]

    speaker=next((x for x in gamedata.scenario.parties if x.name.lower()=="speaker" and x.nationalseats==1), rulingparties[0])

    if speaker not in rulingparties:
        lengthinseats=max(sum([i.nationalseats for i in gamedata.scenario.parties if i in rulingparties]), sum([i.nationalseats for i in gamedata.scenario.parties if i not in rulingparties])-1)
    else:
        lengthinseats=max(sum([i.nationalseats for i in gamedata.scenario.parties if i in rulingparties]), sum([i.nationalseats for i in gamedata.scenario.parties if i not in rulingparties]))

    radius=min(height/((columns+1.5)*2)/2, (width/(math.ceil((lengthinseats)/columns)+1))/2)

    Circle(x+radius, y, radius, speaker.color)

    frontrowposition=[x+radius*3, y+radius*3]
    position=[0, 0]

    for i in [j for j in gamedata.scenario.parties if j in rulingparties]:
        for j in range(next((x.nationalseats for x in gamedata.scenario.parties if i == x), None)):
            if i==speaker:
                if j+1==i.nationalseats:
                    continue
            Circle(frontrowposition[0]+position[0]*(radius*2), frontrowposition[1]+position[1]*(radius*2), radius, i.color)
            position[1]+=1
            #print(frontrowposition[1]+position[1]*10, frontrowposition[0]+position[0]*10)
            if position[1]>columns-1:
                position[0]+=1
                position[1]=0

    frontrowposition=[x+radius*3, y-radius*3]
    position=[0, 0]

    for i in [j for j in gamedata.scenario.parties if j not in rulingparties]:
        for j in range(next((x.nationalseats for x in gamedata.scenario.parties if i == x), None)):
            if i==speaker:
                if j+1==i.nationalseats:
                    continue
            Circle(frontrowposition[0]+position[0]*(radius*2), frontrowposition[1]-position[1]*(radius*2), radius, i.color)
            position[1]+=1
            #print(frontrowposition[1]+position[1]*10, frontrowposition[0]-position[0]*10)
            if position[1]>columns-1:
                position[0]+=1
                position[1]=0


#####################################################################################
####################################### Views #######################################
#####################################################################################

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

    for count, i in enumerate(scenarios):
        Button(screen_width/(1200/(x_outline/2))+(tile_size_x+5)*(count%objects_per_row), screen_height/(700/(y_outline/2))+(tile_size_y+5)*math.floor(count/objects_per_row), tile_size_x, tile_size_y, i , choosescenarioplayer, [i])

def choosescenarioplayer(scenarioname):
    def playerchosen(scenarioname, gamedata, party):
        party.player=True
        scenariomain(scenarioname, gamedata)

    objects.clear()
    gamedata=GameData(ScenarioHandler.main(scenarioname))
    TriggerHandler.generatevariables(gamedata)
    ScenarioHandler.initialisescenario(gamedata.scenario)

    button_size_x, button_size_y = screen_width/(1200/400), screen_height/(700/90)
    tile_size_x, tile_size_y = screen_width/(1200/200), screen_height/(700/200)
    Button(screen_width/2-(button_size_x/2), screen_width/(1200/550), button_size_x, button_size_y, 'Go back', choosescenario)

    objects_per_row=5
    rows=3
    x_outline, y_outline= screen_width/(1200/100),screen_height/(700/200)
    tile_size_x=(screen_width-(objects_per_row*5+x_outline))/objects_per_row
    tile_size_y=(screen_height-(objects_per_row*5+y_outline))/objects_per_row

    for count, i in enumerate([j for j in gamedata.scenario.parties if j.playable==True]):
        Button(screen_width/(1200/(x_outline/2))+(tile_size_x+5)*(count%objects_per_row), screen_height/(700/(y_outline/2))+(tile_size_y+5)*math.floor(count/objects_per_row), tile_size_x, tile_size_y, i.name , playerchosen, [scenarioname, gamedata, i], color=i.color)



def scenariomain(scenarioname, gamedata=None, recalculate=True):
    if recalculate==True:
        gamedata.results=ResultHandler.getresults(gamedata.scenario)
        gamedata.polling=ResultHandler.getpolling(gamedata, gamedata.polling, 5)


    #print(gamedata)
    #print(gamedata.scenario)
    #print(gamedata.results)

    objects.clear()
    Rectangle(900,0,screen_width,screen_height, '#006699')
    Rectangle(0,680,screen_width,screen_height, '#003366')
    Rectangle(0,0,screen_width,screen_height-(screen_height/(700/600)), '#003366')
    Rectangle(0,0,screen_width,screen_height-(screen_height/(700/600)), '#003366', str(gamedata.scenario.main.currentdate.date()))
    button_size_x, button_size_y = screen_width/(1200/200), screen_height/(700/80)
    playedparty=[i.name for i in gamedata.scenario.parties if i.player==True][0]
    if playedparty+'.png' in os.listdir('scenario/' + scenarioname + '/gfx/'):
        Image(980,screen_width/(1200/110),150,150, 'scenario/' + scenarioname + '/gfx/'+playedparty+'.png')
    else:
        Image(980,screen_width/(1200/110),150,150, 'scenario/' + scenarioname + '/gfx/main.png')
    Button(10, screen_width/(1200/10), button_size_x, button_size_y, 'Escape', escape, [scenarioname, gamedata])
    Button(950, screen_width/(1200/10), button_size_x, button_size_y, 'Next Turn', nextturn, [scenarioname, gamedata])
    Button(950, screen_width/(1200/280), button_size_x, button_size_y, 'Government', governmentview, [scenarioname, gamedata])
    Button(950, screen_width/(1200/380), button_size_x, button_size_y, 'Regions', regionview, [scenarioname, gamedata])
    Button(950, screen_width/(1200/480), button_size_x, button_size_y, 'Events', eventview, [scenarioname, gamedata])
    Button(950, screen_width/(1200/580), button_size_x, button_size_y, 'Campaign', escape, [scenarioname, gamedata])
    Button(905, screen_width/(1200/280), screen_width/(1200/20), screen_height/(700/380), '<', addon, [scenarioname, gamedata])
    Map(0,125,900,555, 'scenario/' + scenarioname + '/gfx/map.png', gamedata)

    partysharechart(0, 100, 900, 25, gamedata, 'National', 'seats')

    for i in openwindows:
        i(scenarioname, gamedata, False)
    
def addon(scenarioname, gamedata, affectopenwindows=True):
    if affectopenwindows:
        if addon in openwindows:
            openwindows.remove(addon)
        else:
            openwindows.append(addon)
        scenariomain(scenarioname, gamedata, False)
    else:
        for count,i in enumerate(gamedata.scenario.regions):
            Rectangle(650,120+count*60,screen_width/(1200/250), screen_height/(700/50), '#003366', str(i.name))

def regionview(scenarioname, gamedata, region='National', page=0):
    objects.clear()
    partiesperpage=5
    regions=['National'] + [i.name for i in gamedata.scenario.regions]
    Rectangle(0,680,screen_width,screen_height, '#003366')
    Rectangle(0,0,screen_width,screen_height-(screen_height/(700/600)), '#003366')
    Rectangle(350,0,500,screen_height-(screen_height/(700/600)), '#003366', "Region Information")
    Rectangle(950,0,300,screen_height-(screen_height/(700/600)), '#003366', str(gamedata.scenario.main.currentdate.date()))
    button_size_x, button_size_y = screen_width/(1200/200), screen_height/(700/80)
    Button(10, screen_width/(1200/10), button_size_x, button_size_y, 'Back', scenariomain, [scenarioname, gamedata, False])
    leftlimit=regions.index(region)-1
    if leftlimit<0:
        leftlimit=len(regions)-1
    rightlimit=regions.index(region)+1
    if rightlimit>len(regions)-1:
        rightlimit=0
    Button(10,120,screen_width/(1200/50), screen_height/(700/50), '<', regionview, [scenarioname, gamedata, regions[leftlimit]])
    Rectangle(70,120,screen_width/(1200/1060), screen_height/(700/50), '#003366', region if region=="National" else [i.fullname for i in gamedata.scenario.regions if region==i.name][0])
    Button(1140,120,screen_width/(1200/50), screen_height/(700/50), '>', regionview, [scenarioname, gamedata, regions[rightlimit]])
    if region=='National':
        partycount=len([j for j in gamedata.polling.aggregated.totalpartyresults if j.votes>0 or j.seats>0])
        for count, i in enumerate([j for j in gamedata.polling.aggregated.totalpartyresults if j.votes>0 or j.seats>0]):
            if page*partiesperpage<=count<(page+1)*partiesperpage:
                Button(10,180+count%partiesperpage*60,screen_width/(1200/350), screen_height/(700/50), str(i.party.fullname), partyview, [scenarioname, gamedata, i.party.fullname], "#003366")
                Rectangle(370,180+count%partiesperpage*60,screen_width/(1200/100), screen_height/(700/50), '#003366', str(round(i.percentage,1)) + "%")
                Rectangle(480,180+count%partiesperpage*60,screen_width/(1200/100), screen_height/(700/50), '#003366', str(i.seats))
                Rectangle(590,180+count%partiesperpage*60,screen_width/(1200/380), screen_height/(700/50), '#003366', f'{i.votes:,}')
    else:
        partycount=len([j for j in gamedata.polling.aggregated.partyregionresults if j.region.name==region and (j.votes>0 or j.seats>0)])
        for count, i in enumerate([j for j in gamedata.polling.aggregated.partyregionresults if j.region.name==region and (j.votes>0 or j.seats>0)]):
            if page*partiesperpage<=count<(page+1)*partiesperpage:
                Button(10,180+count%partiesperpage*60,screen_width/(1200/350), screen_height/(700/50), str(i.party.fullname), partyview, [scenarioname, gamedata, i.party.fullname], "#003366")
                Rectangle(370,180+count%partiesperpage%partycount*60,screen_width/(1200/100), screen_height/(700/50), '#003366', str(round(i.percentage,1)) + "%")
                Rectangle(480,180+count%partiesperpage%partycount*60,screen_width/(1200/100), screen_height/(700/50), '#003366', str(i.seats))
                Rectangle(590,180+count%partiesperpage%partycount*60,screen_width/(1200/380), screen_height/(700/50), '#003366', f'{i.votes:,}')

    Rectangle(990,240,screen_width/(1200/200), screen_height/(700/250), '#003366')
    Button(1000, screen_width/(1200/250), screen_width/(1200/180), screen_height/(700/50), 'General', regionview, [scenarioname, gamedata, region])
    Button(1000, screen_width/(1200/310), screen_width/(1200/180), screen_height/(700/50), 'Issues', issueview, [scenarioname, gamedata, None, region])
    Button(1000, screen_width/(1200/370), screen_width/(1200/180), screen_height/(700/50), 'Influence', escape, [scenarioname, gamedata])
    Button(1000, screen_width/(1200/430), screen_width/(1200/180), screen_height/(700/50), 'Polling', pollingview, [scenarioname, gamedata, region])

    partysharechart(10, 480, 960, 50, gamedata, region, 'votes')
    partysharechart(10, 540, 960, 50, gamedata, region, 'seats')
    
    if page!=0:
        Button(400,600,screen_width/(1200/50), screen_height/(700/50), '<', regionview, [scenarioname, gamedata, region, page-1])
    if partycount>partiesperpage:
        Rectangle(460,600,screen_width/(1200/50), screen_height/(700/50), '#003366', str(page+1))
    if partycount>(page+1)*partiesperpage:
        Button(520,600,screen_width/(1200/50), screen_height/(700/50), '>', regionview, [scenarioname, gamedata, region, page+1])
            
def partyview(scenarioname, gamedata, limit=None):
    objects.clear()
    parties=[i.fullname for i in gamedata.scenario.parties if next((x.votes for x in gamedata.results.totalpartyresults if x.party == i), 0)>0]
    currentparty=next((x for x in gamedata.scenario.parties if x.fullname == limit), None)
    if limit==None:
        limit=parties[0]
    Rectangle(0,680,screen_width,screen_height, '#003366')
    Rectangle(0,0,screen_width,screen_height-(screen_height/(700/600)), '#003366')
    Rectangle(350,0,500,screen_height-(screen_height/(700/600)), '#003366', "Party Information")
    Rectangle(950,0,300,screen_height-(screen_height/(700/600)), '#003366', str(gamedata.scenario.main.currentdate.date()))
    button_size_x, button_size_y = screen_width/(1200/200), screen_height/(700/80)
    Button(10, screen_width/(1200/10), button_size_x, button_size_y, 'Back', scenariomain, [scenarioname, gamedata, False])
    if limit in parties:
        leftlimit=parties.index(limit)-1
        if leftlimit<0:
            leftlimit=len(parties)-1
        rightlimit=parties.index(limit)+1
        if rightlimit>len(parties)-1:
            rightlimit=0
    else:
        leftlimit=rightlimit=0
    Button(10,120,screen_width/(1200/50), screen_height/(700/50), '<', partyview, [scenarioname, gamedata, parties[leftlimit]])
    Rectangle(70,120,screen_width/(1200/1060), screen_height/(700/50), '#003366', limit)
    Button(1140,120,screen_width/(1200/50), screen_height/(700/50), '>', partyview, [scenarioname, gamedata, parties[rightlimit]])
    
    Rectangle(10,180,screen_width/(1200/200), screen_height/(700/50), '#003366', "Leader")
    if currentparty.leader==None:
        Rectangle(220,180,screen_width/(1200/350), screen_height/(700/50), '#003366', "None")
    else:
        Button(220,180,screen_width/(1200/350), screen_height/(700/50), currentparty.leader.name, leaderview, [scenarioname, gamedata, currentparty], '#003366' )
    Rectangle(10,240,screen_width/(1200/200), screen_height/(700/50), '#003366', "Votes")
    Rectangle(220,240,screen_width/(1200/250), screen_height/(700/50), '#003366', f'{next((x for x in gamedata.polling.aggregated.totalpartyresults if x.party == currentparty), None).votes:,}')
    Rectangle(480,240,screen_width/(1200/90), screen_height/(700/50), '#003366', str(round(next((x for x in gamedata.polling.aggregated.totalpartyresults if x.party == currentparty), None).percentage,1))+"%")
    Rectangle(10,300,screen_width/(1200/200), screen_height/(700/50), '#003366', "Seats")
    biggestregionpercentage, lowestregionpercentage = None,None
    if next((x.votes for x in gamedata.polling.aggregated.totalpartyresults if x.party.fullname == limit), 0):
        biggestregionpercentage, lowestregionpercentage=max([j.percentage for j in gamedata.polling.aggregated.partyregionresults if j.party.fullname==limit]), min([j.percentage for j in gamedata.polling.aggregated.partyregionresults if j.party.fullname==limit and j.percentage>0])
        biggestregion, lowestregion=next((x for x in gamedata.polling.aggregated.partyregionresults if x.party == currentparty and x.percentage==biggestregionpercentage), None).region.fullname, next((x for x in gamedata.polling.aggregated.partyregionresults if x.party == currentparty and x.percentage==lowestregionpercentage), None).region.fullname
    projectedseats=next((x for x in gamedata.polling.aggregated.totalpartyresults if x.party == currentparty), None).seats
    Rectangle(220,300,screen_width/(1200/350), screen_height/(700/50), '#003366', str(currentparty.nationalseats) + " (projecting " + str(projectedseats) + ")")
    if biggestregionpercentage!=None:
        Rectangle(10,360,screen_width/(1200/200), screen_height/(700/50), '#003366', "Strongest at")
        Button(220,360,screen_width/(1200/350), screen_height/(700/50), biggestregion + " (" + str(round(biggestregionpercentage, 1)) + "%)", regionview,
               [scenarioname, gamedata, biggestregion], '#003366' )
        Rectangle(10,420,screen_width/(1200/200), screen_height/(700/50), '#003366', "Weakest at")
        Button(220,420,screen_width/(1200/350), screen_height/(700/50), lowestregion + " (" + str(round(lowestregionpercentage, 1)) + "%)", regionview,
               [scenarioname, gamedata, lowestregion], '#003366' )

        Map(600,180,360,500, 'scenario/' + scenarioname + '/gfx/map.png', gamedata, 'party', currentparty)

        Rectangle(990,240,screen_width/(1200/200), screen_height/(700/250), '#003366')
        Button(1000, screen_width/(1200/250), screen_width/(1200/180), screen_height/(700/50), 'General', escape, [scenarioname, gamedata])
        Button(1000, screen_width/(1200/310), screen_width/(1200/180), screen_height/(700/50), 'Issues', escape, [scenarioname, gamedata])
        Button(1000, screen_width/(1200/370), screen_width/(1200/180), screen_height/(700/50), 'Influence', escape, [scenarioname, gamedata])
        Button(1000, screen_width/(1200/430), screen_width/(1200/180), screen_height/(700/50), 'Polling', pollingview, [scenarioname, gamedata])

def leaderview(scenarioname, gamedata, party):
    objects.clear()
    #leader=next((x for x in gamedata.scenario.characters if x.name == leadername), None)
    Rectangle(0,680,screen_width,screen_height, '#003366')
    Rectangle(0,0,screen_width,screen_height-(screen_height/(700/600)), '#003366')
    Rectangle(350,0,500,screen_height-(screen_height/(700/600)), '#003366', "Leader Information")
    Rectangle(950,0,300,screen_height-(screen_height/(700/600)), '#003366', str(gamedata.scenario.main.currentdate.date()))
    button_size_x, button_size_y = screen_width/(1200/200), screen_height/(700/80)
    Button(10, screen_width/(1200/10), button_size_x, button_size_y, 'Back', partyview, [scenarioname, gamedata, party.fullname])

    #Button(0,120,screen_width/(1200/350), screen_height/(700/50), str(party.fullname), partyview, [scenarioname, gamedata, party.fullname], "#003366")
    Rectangle(10,120,screen_width/(1200/1180), screen_height/(700/50), '#003366', party.leader.name)
    Rectangle(10,180,screen_width/(1200/250), screen_height/(700/50), '#003366', "Ideologies")
    for count, i in enumerate(party.leader.ideologies):
        Rectangle(10,240+count*60,screen_width/(1200/250), screen_height/(700/50), '#003366', i.fullname)
    Rectangle(270,180,screen_width/(1200/250), screen_height/(700/50), '#003366', "Traits")
    for count, i in enumerate(party.leader.traits):
        Rectangle(270,240+count*60,screen_width/(1200/250), screen_height/(700/50), '#003366', i.fullname)
    Rectangle(10,480,screen_width/(1200/250), screen_height/(700/50), '#003366', "Home Region")
    Rectangle(270,480,screen_width/(1200/250), screen_height/(700/50), '#003366', party.leader.homeregion.fullname)
    Rectangle(10,540,screen_width/(1200/250), screen_height/(700/50), '#003366', "Potential Leaders")
    for count, i in enumerate([j for j in party.characters if j!=party.leader]):
        Rectangle(10+count*190,600,screen_width/(1200/180), screen_height/(700/50), '#003366', i.name)

    if party.leader.identifier+'.png' in os.listdir('scenario/' + scenarioname + '/gfx/'):
        Image(890,180,screen_width/(1200/300),screen_height/(700/350), 'scenario/' + scenarioname + '/gfx/'+party.leader.identifier+'.png')
    else:
        Image(890,180,screen_width/(1200/300),screen_height/(700/350), 'scenario/' + scenarioname + '/gfx/nocharacter.png')


def governmentview(scenarioname, gamedata):
    objects.clear()
    Rectangle(0,680,screen_width,screen_height, '#003366')
    Rectangle(0,0,screen_width,screen_height-(screen_height/(700/600)), '#003366')
    Rectangle(350,0,500,screen_height-(screen_height/(700/600)), '#003366', "Government Information")
    Rectangle(950,0,300,screen_height-(screen_height/(700/600)), '#003366', str(gamedata.scenario.main.currentdate.date()))
    button_size_x, button_size_y = screen_width/(1200/200), screen_height/(700/80)
    Button(10, screen_width/(1200/10), button_size_x, button_size_y, 'Back', scenariomain, [scenarioname, gamedata, False])
    parliamentarychart(10, 100, 1180, 575, gamedata)

def issueview(scenarioname, gamedata, issue=None, region=None, page=0):
    objects.clear()
    partiesperpage=5
    Rectangle(0,680,screen_width,screen_height, '#003366')
    Rectangle(0,0,screen_width,screen_height-(screen_height/(700/600)), '#003366')
    Rectangle(350,0,500,screen_height-(screen_height/(700/600)), '#003366', "Issue Information")
    Rectangle(950,0,300,screen_height-(screen_height/(700/600)), '#003366', str(gamedata.scenario.main.currentdate.date()))
    button_size_x, button_size_y = screen_width/(1200/200), screen_height/(700/80)
    Button(10, screen_width/(1200/10), button_size_x, button_size_y, 'Back', scenariomain, [scenarioname, gamedata, False])
    regions=['National'] + [i.name for i in gamedata.scenario.regions]
    if not region:
        region=regions[0]
    leftregion=regions.index(region)-1
    if leftregion<0:
        leftregion=len(regions)-1
    rightregion=regions.index(region)+1
    if rightregion>len(regions)-1:
        rightregion=0
    Button(10,120,screen_width/(1200/50), screen_height/(700/50), '<', issueview, [scenarioname, gamedata, issue, regions[leftregion]])
    Rectangle(70,120,screen_width/(1200/1060), screen_height/(700/50), '#003366', region if region=="National" else [i.fullname for i in gamedata.scenario.regions if region==i.name][0])
    Button(1140,120,screen_width/(1200/50), screen_height/(700/50), '>', issueview, [scenarioname, gamedata, issue, regions[rightregion]])
    issues=[i.fullname for i in gamedata.scenario.issues]
    if not issue:
        issue=issues[0]
    leftissue=issues.index(issue)-1
    if leftissue<0:
        leftissue=len(issues)-1
    rightissue=issues.index(issue)+1
    if rightissue>len(issues)-1:
        rightissue=0
    Button(10,180,screen_width/(1200/50), screen_height/(700/50), '<', issueview, [scenarioname, gamedata, issues[leftissue], region])
    Rectangle(70,180,screen_width/(1200/1060), screen_height/(700/50), '#003366', issue)
    Button(1140,180,screen_width/(1200/50), screen_height/(700/50), '>', issueview, [scenarioname, gamedata, issues[rightissue], region])

    if region=='National':
        partycount=len(gamedata.scenario.parties)
        for count, i in enumerate([j for j in gamedata.scenario.partyissues if issue==j.issue.fullname]):
            if page*partiesperpage<=count<(page+1)*partiesperpage:
                if i.variance>2:
                    division="Divided"
                else:
                    division="United"
                #print(i.party.name, i.issue.name, i.mean, i.variance, division, min(math.floor((i.mean+5)/+(10/len(i.issue.levels))),len(i.issue.levels)-1))
                #print(i.party.name, i.issue.name, i.mean, i.variance, division, i.issue.levels[min(math.floor((i.mean+5)/+(10/len(i.issue.levels))),len(i.issue.levels)-1)])
                Button(10,240+count%partiesperpage*60,screen_width/(1200/350), screen_height/(700/50), str(i.party.fullname), partyview, [scenarioname, gamedata, i.party.fullname], "#003366")
                Rectangle(370,240+count%partiesperpage%partycount*60,screen_width/(1200/300), screen_height/(700/50), '#003366', division)
                Rectangle(680,240+count%partiesperpage%partycount*60,screen_width/(1200/300), screen_height/(700/50), '#003366', i.issue.levels[min(math.floor((i.mean+5)/+(10/len(i.issue.levels))),len(i.issue.levels)-1)])
    else:
        partycount=len(gamedata.scenario.parties)
        currentregionissue=next((x for x in gamedata.scenario.regionissues if issue==x.issue.fullname and region==x.region.name), None)
        if currentregionissue.variance>2:
            division="Divided"
        else:
            division="United"
        Button(10,240,screen_width/(1200/350), screen_height/(700/50), str(currentregionissue.region.fullname), regionview, [scenarioname, gamedata, region], "#003366")
        Rectangle(370,240,screen_width/(1200/300), screen_height/(700/50), '#003366', division)
        Rectangle(680,240,screen_width/(1200/300), screen_height/(700/50), '#003366', currentregionissue.issue.levels[min(math.floor((currentregionissue.mean+5)/+(10/len(currentregionissue.issue.levels))),len(currentregionissue.issue.levels)-1)])
        for count, i in enumerate([j for j in gamedata.scenario.partyissues if issue==j.issue.fullname]):
            if page*partiesperpage<=count<(page+1)*partiesperpage:
                if i.variance>2:
                    division="Divided"
                else:
                    division="United"
                #print(i.party.name, i.issue.name, i.mean, i.variance, division, min(math.floor((i.mean+5)/+(10/len(i.issue.levels))),len(i.issue.levels)-1))
                #print(i.party.name, i.issue.name, i.mean, i.variance, division, i.issue.levels[min(math.floor((i.mean+5)/+(10/len(i.issue.levels))),len(i.issue.levels)-1)])
                Button(10,300+count%partiesperpage*60,screen_width/(1200/350), screen_height/(700/50), str(i.party.fullname), partyview, [scenarioname, gamedata, i.party.fullname], "#003366")
                Rectangle(370,300+count%partiesperpage%partycount*60,screen_width/(1200/300), screen_height/(700/50), '#003366', division)
                Rectangle(680,300+count%partiesperpage%partycount*60,screen_width/(1200/300), screen_height/(700/50), '#003366', i.issue.levels[min(math.floor((i.mean+5)/+(10/len(i.issue.levels))),len(i.issue.levels)-1)])

    Rectangle(990,240,screen_width/(1200/200), screen_height/(700/250), '#003366')
    Button(1000, screen_width/(1200/250), screen_width/(1200/180), screen_height/(700/50), 'General', regionview, [scenarioname, gamedata, region])
    Button(1000, screen_width/(1200/310), screen_width/(1200/180), screen_height/(700/50), 'Issues', issueview, [scenarioname, gamedata, None, region])
    Button(1000, screen_width/(1200/370), screen_width/(1200/180), screen_height/(700/50), 'Influence', escape, [scenarioname, gamedata])
    Button(1000, screen_width/(1200/430), screen_width/(1200/180), screen_height/(700/50), 'Polling', pollingview, [scenarioname, gamedata, region])

    if page!=0:
        Button(400,600,screen_width/(1200/50), screen_height/(700/50), '<', issueview, [scenarioname, gamedata, issue, region, page-1])
    if partycount>partiesperpage:
        Rectangle(460,600,screen_width/(1200/50), screen_height/(700/50), '#003366', str(page+1))
    if partycount>(page+1)*partiesperpage:
        Button(520,600,screen_width/(1200/50), screen_height/(700/50), '>', issueview, [scenarioname, gamedata, issue, region, page+1])

def pollingview(scenarioname, gamedata, region="National", page=0):
    objects.clear()
    pollsperpage=7
    regions=['National'] + [i.name for i in gamedata.scenario.regions]
    Rectangle(0,680,screen_width,screen_height, '#003366')
    Rectangle(0,0,screen_width,screen_height-(screen_height/(700/600)), '#003366')
    Rectangle(350,0,500,screen_height-(screen_height/(700/600)), '#003366', "Polling")
    Rectangle(950,0,300,screen_height-(screen_height/(700/600)), '#003366', str(gamedata.scenario.main.currentdate.date()))
    button_size_x, button_size_y = screen_width/(1200/200), screen_height/(700/80)
    Button(10, screen_width/(1200/10), button_size_x, button_size_y, 'Back', scenariomain, [scenarioname, gamedata, False])
    leftlimit=regions.index(region)-1
    if leftlimit<0:
        leftlimit=len(regions)-1
    rightlimit=regions.index(region)+1
    if rightlimit>len(regions)-1:
        rightlimit=0
    Button(10,120,screen_width/(1200/50), screen_height/(700/50), '<', pollingview, [scenarioname, gamedata, regions[leftlimit], 0])
    Rectangle(70,120,screen_width/(1200/1060), screen_height/(700/50), '#003366', region if region=="National" else [i.fullname for i in gamedata.scenario.regions if region==i.name][0])
    Button(1140,120,screen_width/(1200/50), screen_height/(700/50), '>', pollingview, [scenarioname, gamedata, regions[rightlimit], 0])

    pollcount=len(gamedata.polling.polls)

    if region=='National':
        for count, i in enumerate(reversed([j for j in gamedata.polling.polls])):
            if page*pollsperpage<=count<(page+1)*pollsperpage:
                Button(10,180+count%pollsperpage*60,screen_width/(1200/350), screen_height/(700/50), str(i.date.strftime('%Y-%m-%d')), pollview, [scenarioname, gamedata, i, region], '#003366')
                for partycount, j in enumerate(i.totalpartyresults):
                    if partycount<5:
                        Button(370+partycount*110,180+count%pollsperpage*60,screen_width/(1200/100), screen_height/(700/50), str(j.seats), partyview, [scenarioname, gamedata, j.party.fullname], "#003366")
    else:
        for count, i in enumerate(reversed([j for j in gamedata.polling.polls])):
            if page*pollsperpage<=count<(page+1)*pollsperpage:
                Button(10,180+count%pollsperpage*60,screen_width/(1200/350), screen_height/(700/50), str(i.date.strftime('%Y-%m-%d')), pollview, [scenarioname, gamedata, i, region], '#003366')
                for partycount, j in enumerate([k for k in i.partyregionresults if k.region.name==region]):
                    if partycount<5:
                        Button(370+partycount*110,180+count%pollsperpage*60,screen_width/(1200/100), screen_height/(700/50), str(j.seats), partyview, [scenarioname, gamedata, j.party.fullname], "#003366")


    Rectangle(990,240,screen_width/(1200/200), screen_height/(700/250), '#003366')
    Button(1000, screen_width/(1200/250), screen_width/(1200/180), screen_height/(700/50), 'General', regionview, [scenarioname, gamedata, region])
    Button(1000, screen_width/(1200/310), screen_width/(1200/180), screen_height/(700/50), 'Issues', issueview, [scenarioname, gamedata])
    Button(1000, screen_width/(1200/370), screen_width/(1200/180), screen_height/(700/50), 'Influence', escape, [scenarioname, gamedata])
    Button(1000, screen_width/(1200/430), screen_width/(1200/180), screen_height/(700/50), 'Polling', pollingview, [scenarioname, gamedata, region, 0])

    if page!=0:
        Button(400,600,screen_width/(1200/50), screen_height/(700/50), '<', pollingview, [scenarioname, gamedata, region, page-1])
    if pollcount>pollsperpage:
        Rectangle(460,600,screen_width/(1200/50), screen_height/(700/50), '#003366', str(page+1))
    if pollcount>(page+1)*pollsperpage:
        Button(520,600,screen_width/(1200/50), screen_height/(700/50), '>', pollingview, [scenarioname, gamedata, region, page+1])

def pollview(scenarioname, gamedata, poll, region='National', page=0):
    objects.clear()
    partiesperpage=5
    regions=['National'] + [i.name for i in gamedata.scenario.regions]
    Rectangle(0,680,screen_width,screen_height, '#003366')
    Rectangle(0,0,screen_width,screen_height-(screen_height/(700/600)), '#003366')
    Rectangle(350,0,500,screen_height-(screen_height/(700/600)), '#003366', "Poll Information")
    Rectangle(950,0,300,screen_height-(screen_height/(700/600)), '#003366', str(gamedata.scenario.main.currentdate.date()))
    button_size_x, button_size_y = screen_width/(1200/200), screen_height/(700/80)
    Button(10, screen_width/(1200/10), button_size_x, button_size_y, 'Back', pollingview, [scenarioname, gamedata, region])
    leftlimit=regions.index(region)-1
    if leftlimit<0:
        leftlimit=len(regions)-1
    rightlimit=regions.index(region)+1
    if rightlimit>len(regions)-1:
        rightlimit=0
    Button(10,120,screen_width/(1200/50), screen_height/(700/50), '<', pollview, [scenarioname, gamedata, poll, regions[leftlimit]])
    Rectangle(70,120,screen_width/(1200/1060), screen_height/(700/50), '#003366', region if region=="National" else [i.fullname for i in gamedata.scenario.regions if region==i.name][0])
    Button(1140,120,screen_width/(1200/50), screen_height/(700/50), '>', pollview, [scenarioname, gamedata, poll, regions[rightlimit]])
    if region=='National':
        partycount=len([j for j in poll.totalpartyresults if j.votes>0 or j.seats>0])
        for count, i in enumerate([j for j in poll.totalpartyresults if j.votes>0 or j.seats>0]):
            if page*partiesperpage<=count<(page+1)*partiesperpage:
                Button(10,180+count%partiesperpage*60,screen_width/(1200/350), screen_height/(700/50), str(i.party.fullname), partyview, [scenarioname, gamedata, i.party.fullname], "#003366")
                Rectangle(370,180+count%partiesperpage*60,screen_width/(1200/100), screen_height/(700/50), '#003366', str(round(i.percentage,1)) + "%")
                Rectangle(480,180+count%partiesperpage*60,screen_width/(1200/100), screen_height/(700/50), '#003366', str(i.seats))
                Rectangle(590,180+count%partiesperpage*60,screen_width/(1200/100), screen_height/(700/50), '#003366', str(i.seats-next((x for x in gamedata.polling.aggregated.totalpartyresults if x.party == i.party), None).seats))
                Rectangle(700,180+count%partiesperpage*60,screen_width/(1200/100), screen_height/(700/50), '#003366', str(round(i.percentage-next((x for x in gamedata.polling.aggregated.totalpartyresults if x.party == i.party), None).percentage,1)) + "%")
    else:
        partycount=len([j for j in poll.partyregionresults if j.region.name==region and (j.votes>0 or j.seats>0)])
        for count, i in enumerate([j for j in poll.partyregionresults if j.region.name==region and (j.votes>0 or j.seats>0)]):
            if page*partiesperpage<=count<(page+1)*partiesperpage:
                Button(10,180+count%partiesperpage*60,screen_width/(1200/350), screen_height/(700/50), str(i.party.fullname), partyview, [scenarioname, gamedata, i.party.fullname], "#003366")
                Rectangle(370,180+count%partiesperpage%partycount*60,screen_width/(1200/100), screen_height/(700/50), '#003366', str(round(i.percentage,1)) + "%")
                Rectangle(480,180+count%partiesperpage%partycount*60,screen_width/(1200/100), screen_height/(700/50), '#003366', str(i.seats))
                Rectangle(590,180+count%partiesperpage*60,screen_width/(1200/100), screen_height/(700/50), '#003366', str(i.seats-next((x for x in gamedata.polling.aggregated.partyregionresults if x.party == i.party and x.region==i.region), None).seats))
                Rectangle(700,180+count%partiesperpage*60,screen_width/(1200/100), screen_height/(700/50), '#003366', str(round(i.percentage-next((x for x in gamedata.polling.aggregated.partyregionresults if x.party == i.party and x.region==i.region), None).percentage,1)) + "%")

    Rectangle(990,240,screen_width/(1200/200), screen_height/(700/250), '#003366')
    Button(1000, screen_width/(1200/250), screen_width/(1200/180), screen_height/(700/50), 'General', regionview, [scenarioname, gamedata, region])
    Button(1000, screen_width/(1200/310), screen_width/(1200/180), screen_height/(700/50), 'Issues', issueview, [scenarioname, gamedata, None, region])
    Button(1000, screen_width/(1200/370), screen_width/(1200/180), screen_height/(700/50), 'Influence', escape, [scenarioname, gamedata])
    Button(1000, screen_width/(1200/430), screen_width/(1200/180), screen_height/(700/50), 'Polling', pollingview, [scenarioname, gamedata, region])

    partysharechart(10, 480, 960, 50, gamedata, region, 'votes')
    partysharechart(10, 540, 960, 50, gamedata, region, 'seats')
    
    if page!=0:
        Button(400,600,screen_width/(1200/50), screen_height/(700/50), '<', pollview, [scenarioname, gamedata, poll, region, page-1])
    if partycount>partiesperpage:
        Rectangle(460,600,screen_width/(1200/50), screen_height/(700/50), '#003366', str(page+1))
    if partycount>(page+1)*partiesperpage:
        Button(520,600,screen_width/(1200/50), screen_height/(700/50), '>', pollview, [scenarioname, gamedata, poll, region, page+1])

def eventview(scenarioname, gamedata, currentevent=None):
    objects.clear()
    Rectangle(0,680,screen_width,screen_height, '#003366')
    Rectangle(0,0,screen_width,screen_height-(screen_height/(700/600)), '#003366')
    Rectangle(350,0,500,screen_height-(screen_height/(700/600)), '#003366', "Events' View")
    Rectangle(950,0,300,screen_height-(screen_height/(700/600)), '#003366', str(gamedata.scenario.main.currentdate.date()))
    button_size_x, button_size_y = screen_width/(1200/200), screen_height/(700/80)
    Button(10, screen_width/(1200/10), button_size_x, button_size_y, 'Back', scenariomain, [scenarioname, gamedata, False])

    Rectangle(10, 110, screen_width/(1200/190), screen_width/(1200/565), '#003366')
    if not gamedata.scenario.news:
        Rectangle(15, 115, screen_width/(1200/180), screen_width/(1200/80), '#250045', "No events so far")
    else:
        for count, i in enumerate(reversed(gamedata.scenario.news)):
            Button(15, 115+count*90, screen_width/(1200/180), screen_width/(1200/80), i.event.name, eventview, [scenarioname, gamedata, i.event])

    if currentevent==None:
        pass
    else:
        MultipleLineText(210,110, 580, 565, '#003366', currentevent.description, fontsize=30)
    #parliamentarychart(10, 100, 1180, 575, gamedata)

def nextturn(scenarioname, gamedata):
    objects.clear()
    if gamedata.scenario.base.enddate>gamedata.scenario.main.currentdate:
        gamedata.scenario.main.newturn()
        TriggerHandler.main(gamedata.scenario)
        if gamedata.scenario.main.currentdate<gamedata.scenario.base.electiondate<gamedata.scenario.main.currentdate+gamedata.scenario.main.turnlength:
            print(gamedata.scenario.main.currentdate.date(), "ELECTION DAY")
        else:
            print(gamedata.scenario.main.currentdate.date())

    scenariomain(scenarioname, gamedata)


def escape(scenarioname, gamedata):
    objects.clear()
    button_size_x, button_size_y = screen_width/(1200/400), screen_height/(700/90)
    ImageButton(screen_width/2-(button_size_x/2), screen_width/(1200/300), button_size_x, button_size_y, 'gfx/button.png', 'Return to the game', scenariomain, [scenarioname, gamedata, False])
    ImageButton(screen_width/2-(button_size_x/2), screen_width/(1200/400), button_size_x, button_size_y, 'gfx/button.png', 'Main menu', mainmenu)
    ImageButton(screen_width/2-(button_size_x/2), screen_width/(1200/500), button_size_x, button_size_y, 'gfx/button.png', 'Quit', quit)

def options():
    objects.clear()
    Button(screen_width/2-200, 130, 400, 100, 'Go back', mainmenu)

def quit():
    pygame.quit()
    sys.exit()


#####################################################################################
##################################### Main loop #####################################
#####################################################################################

if __name__ == "__main__":
    if 'scenario' in os.listdir():
        scenarios=os.listdir('scenario')
    else:
        sys.exit("ERROR: no scenario folder found")
    scenarios=getvalidscenarios(scenarios)
    #scenarioname=getscenario(scenarios)

    pygame.init()
    pygame.display.set_caption('McGovern')
    pygame.display.set_icon(pygame.image.load('gfx/icon.png'))
    fps = 30
    fpsClock = pygame.time.Clock()
    screen_width, screen_height = 1200, 700
    screen = pygame.display.set_mode((screen_width, screen_height))

    mainfontstyle='Arial'
    mainfontsize=int(screen_height/(700/40))
    mainfont = pygame.freetype.SysFont(mainfontstyle, mainfontsize)

    objects = []
    openwindows = []
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