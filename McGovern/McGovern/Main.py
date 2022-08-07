from re import A
import ScenarioHandler
import ResultHandler
import TriggerHandler
import os
import math
import pygame
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
    def __init__(self, x, y, width, height, color, text=None):
            self.x = x
            self.y = y
            self.width = width
            self.height = height
            self.color = color
            self.text = text

            objects.append(self)

            self.Surface = pygame.Surface((self.width, self.height))
            self.Surface.fill(self.color)
            self.Rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def process(self):
        screen.blit(self.Surface, self.Rect)

        textsurface = font.render(self.text, True, (255,255,255))

        self.Surface.blit(textsurface, [
            self.width/2 - textsurface.get_rect().width/2,
            self.height/2 - textsurface.get_rect().height/2
        ])

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
    def __init__(self, x, y, width, height, buttonText='Button', onclickFunction=None, paramsFunction=[], color="#250045", onePress=False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.onclickFunction = onclickFunction
        self.paramsFunction = paramsFunction
        self.onePress = onePress
        self.color=color

        self.buttonSurface = pygame.Surface((self.width, self.height))
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.buttonSurf = font.render(buttonText, True, (255, 255, 255))

        self.alreadyPressed = False

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

        self.buttonSurface.blit(self.buttonSurf, [
            self.buttonRect.width/2 - self.buttonSurf.get_rect().width/2,
            self.buttonRect.height/2 - self.buttonSurf.get_rect().height/2
        ])

        screen.blit(self.buttonSurface, self.buttonRect)

class ImageButton():
    def __init__(self, x, y, width, height, img, buttonText='Button', onclickFunction=None, paramsFunction=[]):
            self.x = x
            self.y = y
            self.width = width
            self.height = height
            self.img = img
            self.buttonText=buttonText
            self.onclickFunction=onclickFunction
            self.paramsFunction=paramsFunction

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
                    self.onclickFunction(*self.paramsFunction)
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


    if rulingparties==None:
        rulingparties=[gamedata.polling.aggregated.totalpartyresults[0].party]

    speaker=next((x.party for x in gamedata.polling.aggregated.totalpartyresults if x.party.name.lower()=="speaker" and x.seats==1), rulingparties[0])

    if speaker not in rulingparties:
        lengthinseats=max(sum([i.seats for i in gamedata.polling.aggregated.totalpartyresults if i.party in rulingparties]), sum([i.seats for i in gamedata.polling.aggregated.totalpartyresults if i.party not in rulingparties])-1)
    else:
        lengthinseats=max(sum([i.seats for i in gamedata.polling.aggregated.totalpartyresults if i.party in rulingparties]), sum([i.seats for i in gamedata.polling.aggregated.totalpartyresults if i.party not in rulingparties]))

    radius=min(height/((columns+1.5)*2)/2, (width/(math.ceil((lengthinseats)/columns)+1))/2)

    Circle(x+radius, y, radius, speaker.color)

    frontrowposition=[x+radius*3, y+radius*3]
    position=[0, 0]

    for i in [j for j in gamedata.polling.aggregated.totalpartyresults if j.party in rulingparties]:
        for j in range(next((x.seats for x in gamedata.polling.aggregated.totalpartyresults if i.party == x.party), None)):
            if i.party==speaker:
                if j+1==i.seats:
                    continue
            Circle(frontrowposition[0]+position[0]*(radius*2), frontrowposition[1]+position[1]*(radius*2), radius, i.party.color)
            position[1]+=1
            #print(frontrowposition[1]+position[1]*10, frontrowposition[0]+position[0]*10)
            if position[1]>columns-1:
                position[0]+=1
                position[1]=0

    frontrowposition=[x+radius*3, y-radius*3]
    position=[0, 0]

    for i in [j for j in gamedata.polling.aggregated.totalpartyresults if j.party not in rulingparties]:
        for j in range(next((x.seats for x in gamedata.polling.aggregated.totalpartyresults if i.party == x.party), None)):
            if i.party==speaker:
                if j+1==i.seats:
                    continue
            Circle(frontrowposition[0]+position[0]*(radius*2), frontrowposition[1]-position[1]*(radius*2), radius, i.party.color)
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
        Button(screen_width/(1200/(x_outline/2))+(tile_size_x+5)*(count%objects_per_row), screen_height/(700/(y_outline/2))+(tile_size_y+5)*math.floor(count/objects_per_row), tile_size_x, tile_size_y, i , scenariomain, [i])


def scenariomain(scenarioname, gamedata=None, recalculate=True):
    if gamedata==None:
        gamedata=GameData(ScenarioHandler.main(scenarioname))

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
    Image(980,screen_width/(1200/110),150,150, 'scenario/' + scenarioname + '/gfx/labour.png')
    Button(10, screen_width/(1200/10), button_size_x, button_size_y, 'Escape', escape, [scenarioname, gamedata])
    Button(950, screen_width/(1200/10), button_size_x, button_size_y, 'Next Turn', nextturn, [scenarioname, gamedata])
    Button(950, screen_width/(1200/280), button_size_x, button_size_y, 'Government', governmentview, [scenarioname, gamedata])
    Button(950, screen_width/(1200/380), button_size_x, button_size_y, 'Regions', regionview, [scenarioname, gamedata])
    Button(950, screen_width/(1200/480), button_size_x, button_size_y, 'Events', escape, [scenarioname, gamedata])
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
    Rectangle(70,120,screen_width/(1200/1060), screen_height/(700/50), '#003366', region)
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

    Rectangle(990,180,screen_width/(1200/200), screen_height/(700/250), '#003366')
    Button(1000, screen_width/(1200/190), screen_width/(1200/180), screen_height/(700/50), 'General', regionview, [scenarioname, gamedata, region])
    Button(1000, screen_width/(1200/250), screen_width/(1200/180), screen_height/(700/50), 'Issues', issueview, [scenarioname, gamedata, None, region])
    Button(1000, screen_width/(1200/310), screen_width/(1200/180), screen_height/(700/50), 'Influence', escape, [scenarioname, gamedata])
    Button(1000, screen_width/(1200/370), screen_width/(1200/180), screen_height/(700/50), 'Polling', escape, [scenarioname, gamedata])

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
        biggestregion, lowestregion=next((x for x in gamedata.polling.aggregated.partyregionresults if x.party == currentparty and x.percentage==biggestregionpercentage), None).region.name, next((x for x in gamedata.polling.aggregated.partyregionresults if x.party == currentparty and x.percentage==lowestregionpercentage), None).region.name
    Rectangle(220,300,screen_width/(1200/350), screen_height/(700/50), '#003366', str(next((x for x in gamedata.polling.aggregated.totalpartyresults if x.party == currentparty), None).seats))
    if biggestregionpercentage!=None:
        Rectangle(10,360,screen_width/(1200/200), screen_height/(700/50), '#003366', "Strongest at")
        Button(220,360,screen_width/(1200/350), screen_height/(700/50), biggestregion[0:15] + " (" + str(round(biggestregionpercentage, 1)) + "%)", regionview,
               [scenarioname, gamedata, biggestregion], '#003366' )
        Rectangle(10,420,screen_width/(1200/200), screen_height/(700/50), '#003366', "Weakest at")
        Button(220,420,screen_width/(1200/350), screen_height/(700/50), lowestregion[0:15] + " (" + str(round(lowestregionpercentage, 1)) + "%)", regionview,
               [scenarioname, gamedata, lowestregion], '#003366' )

        Map(600,180,360,500, 'scenario/' + scenarioname + '/gfx/map.png', gamedata, 'party', currentparty)

        Rectangle(990,180,screen_width/(1200/200), screen_height/(700/250), '#003366')
        Button(1000, screen_width/(1200/190), screen_width/(1200/180), screen_height/(700/50), 'General', escape, [scenarioname, gamedata])
        Button(1000, screen_width/(1200/250), screen_width/(1200/180), screen_height/(700/50), 'Issues', escape, [scenarioname, gamedata])
        Button(1000, screen_width/(1200/310), screen_width/(1200/180), screen_height/(700/50), 'Influence', escape, [scenarioname, gamedata])
        Button(1000, screen_width/(1200/370), screen_width/(1200/180), screen_height/(700/50), 'Polling', escape, [scenarioname, gamedata])

def leaderview(scenarioname, gamedata, party):
    objects.clear()
    #leader=next((x for x in gamedata.scenario.characters if x.name == leadername), None)
    Rectangle(0,680,screen_width,screen_height, '#003366')
    Rectangle(0,0,screen_width,screen_height-(screen_height/(700/600)), '#003366')
    Rectangle(350,0,500,screen_height-(screen_height/(700/600)), '#003366', "Leader Information")
    Rectangle(950,0,300,screen_height-(screen_height/(700/600)), '#003366', str(gamedata.scenario.main.currentdate.date()))
    button_size_x, button_size_y = screen_width/(1200/200), screen_height/(700/80)
    Button(10, screen_width/(1200/10), button_size_x, button_size_y, 'Back', partyview, [scenarioname, gamedata, party.fullname])

    Button(0,120,screen_width/(1200/350), screen_height/(700/50), str(party.fullname), partyview, [scenarioname, gamedata, party.fullname], "#003366")

def governmentview(scenarioname, gamedata):
    objects.clear()
    Rectangle(0,680,screen_width,screen_height, '#003366')
    Rectangle(0,0,screen_width,screen_height-(screen_height/(700/600)), '#003366')
    Rectangle(350,0,500,screen_height-(screen_height/(700/600)), '#003366', "Government Information")
    Rectangle(950,0,300,screen_height-(screen_height/(700/600)), '#003366', str(gamedata.scenario.main.currentdate.date()))
    button_size_x, button_size_y = screen_width/(1200/200), screen_height/(700/80)
    Button(10, screen_width/(1200/10), button_size_x, button_size_y, 'Back', scenariomain, [scenarioname, gamedata, False])
    parliamentarychart(10, 100, 1180, 575, gamedata)

def issueview(scenarioname, gamedata, issue=None, region=None):
    objects.clear()
    Rectangle(0,680,screen_width,screen_height, '#003366')
    Rectangle(0,0,screen_width,screen_height-(screen_height/(700/600)), '#003366')
    Rectangle(350,0,500,screen_height-(screen_height/(700/600)), '#003366', "Issue Information")
    Rectangle(950,0,300,screen_height-(screen_height/(700/600)), '#003366', str(gamedata.scenario.main.currentdate.date()))
    button_size_x, button_size_y = screen_width/(1200/200), screen_height/(700/80)
    Button(10, screen_width/(1200/10), button_size_x, button_size_y, 'Back', scenariomain, [scenarioname, gamedata, False])
    regions=['National'] + [i.name for i in gamedata.scenario.regions]
    leftregion=regions.index(region)-1
    if leftregion<0:
        leftregion=len(regions)-1
    rightregion=regions.index(region)+1
    if rightregion>len(regions)-1:
        rightregion=0
    Button(10,120,screen_width/(1200/50), screen_height/(700/50), '<', issueview, [scenarioname, gamedata, issue, regions[leftregion]])
    Rectangle(70,120,screen_width/(1200/1060), screen_height/(700/50), '#003366', region)
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
    Button(10,620,screen_width/(1200/50), screen_height/(700/50), '<', issueview, [scenarioname, gamedata, issues[leftissue], region])
    Rectangle(70,620,screen_width/(1200/1060), screen_height/(700/50), '#003366', issue)
    Button(1140,620,screen_width/(1200/50), screen_height/(700/50), '>', issueview, [scenarioname, gamedata, issues[rightissue], region])

    if region=='National':
        pass
    else:
        regionissue=next((x for x in gamedata.scenario.regionissues if x.issue.fullname == issue and x.region.name==region), None)
        #Rectangle(400+regionissue.mean*100,340,screen_width/(1200/(100*regionissue.variance)), screen_height/(700/10), (200, 200, 200))
        for count, i in enumerate(reversed([j for j in gamedata.scenario.partyissues if j.issue.fullname==issue])):
            Rectangle(400+i.mean*100,350-count*10,screen_width/(1200/(100*i.variance)), screen_height/(700/10), i.party.color)
        Rectangle(400+regionissue.mean*100,350-len(gamedata.scenario.parties)*10,screen_width/(1200/(100*regionissue.variance)), screen_height/(700/10), (200, 200, 200))



    Rectangle(990,180,screen_width/(1200/200), screen_height/(700/250), '#003366')
    Button(1000, screen_width/(1200/190), screen_width/(1200/180), screen_height/(700/50), 'General', regionview, [scenarioname, gamedata, region])
    Button(1000, screen_width/(1200/250), screen_width/(1200/180), screen_height/(700/50), 'Issues', issueview, [scenarioname, gamedata, issue, region])
    Button(1000, screen_width/(1200/310), screen_width/(1200/180), screen_height/(700/50), 'Influence', escape, [scenarioname, gamedata])
    Button(1000, screen_width/(1200/370), screen_width/(1200/180), screen_height/(700/50), 'Polling', escape, [scenarioname, gamedata])


def nextturn(scenarioname, gamedata):
    objects.clear()
    if gamedata.scenario.base.enddate>gamedata.scenario.main.currentdate:
        gamedata.scenario.main.newturn()
        TriggerHandler.main(gamedata)
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


#####################################################################################
##################################### Main loop #####################################
#####################################################################################

if __name__ == "__main__":
    scenarios=os.listdir('scenario')
    scenarios=getvalidscenarios(scenarios)
    #scenarioname=getscenario(scenarios)

    pygame.init()
    pygame.display.set_caption('McGovern')
    pygame.display.set_icon(pygame.image.load('gfx/icon.png'))
    fps = 30
    fpsClock = pygame.time.Clock()
    screen_width, screen_height = 1200, 700
    screen = pygame.display.set_mode((screen_width, screen_height))

    font = pygame.font.SysFont('Arial', int(screen_height/(700/40)))

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