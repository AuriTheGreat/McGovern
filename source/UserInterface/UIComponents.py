import pygame
import math
import numpy as np

class Rectangle():
    def __init__(self, UIState, x, y, width, height, color, text="", fontstyle=None, fontsize=None):
            self.UIState = UIState
            self.x = x
            self.y = y
            self.width = width
            self.height = height
            self.color = color
            self.text = text

            if fontstyle!=None:
                self.fontstyle=fontstyle
            else:
                self.fontstyle=UIState.mainfontstyle
            if fontsize!=None:
                self.fontsize=int(UIState.screen_height/(700/fontsize))
            else:
                self.fontsize=UIState.mainfontsize

            self.font=pygame.freetype.SysFont(self.fontstyle, self.fontsize)

            while self.text!="": #Runs in case the font is too big for the rectangle
                self.font=pygame.freetype.SysFont(self.fontstyle, self.fontsize)      
                text_rect = self.font.get_rect(self.text)
                if text_rect.width<self.width and text_rect.height<self.height:
                    break
                else:
                    self.fontsize-=1

            self.UIState.objects.append(self)

            self.Surface = pygame.Surface((self.width, self.height))
            self.Surface.fill(self.color)

            text_rect = self.font.get_rect(self.text)
            text_rect.center = self.Surface.get_rect().center
            self.font.render_to(self.Surface, text_rect.topleft, self.text, (255,255,255))
            self.Rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def process(self):
        self.UIState.screen.blit(self.Surface, self.Rect)


class Circle():
    def __init__(self, UIState, x, y, radius, color):
            self.UIState = UIState
            self.x = x
            self.y = y
            self.radius = radius
            self.color = color

            self.UIState.objects.append(self)

    def process(self):
        pygame.draw.circle(self.UIState.screen, self.color, (self.x, self.y), self.radius)

class LoadingScreenImage():
    def __init__(self, UIState, x, y, radius, color):
        self.UIState = UIState
        self.basex = x
        self.basey = y
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        #self.surface = pygame.Surface((self.x+radius, self.y+radius), pygame.SRCALPHA)
        self.basetransparency=30
        self.transparency=self.basetransparency

        self.UIState.objects.append(self)

    def process(self):
        color=tuple(list(self.color) + [abs(self.transparency)])
        self.surface = pygame.Surface((self.x+self.radius, self.y+self.radius), pygame.SRCALPHA)
        pygame.draw.circle(self.surface,color,(self.x, self.y), self.radius)
        self.UIState.screen.blit(self.surface, (0,0))
        self.x+=30
        self.transparency=min(255,self.transparency+30)
        if self.transparency==255:
            self.x=self.basex
            self.y=self.basey
            self.transparency=self.basetransparency



class Image():
    def __init__(self, UIState, x, y, width, height, img):
        self.UIState=UIState
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.img = img

        self.image = pygame.image.load(self.img)
        self.image = pygame.transform.scale(self.image,(self.width, self.height)).convert()

        self.UIState.objects.append(self)

    def process(self):
        #print(self.image.get_at((2, 2)))
        self.UIState.screen.blit(self.image, (self.x,self.y))
        

class Button():
    def __init__(self, UIState, x, y, width, height, text='', onclickFunction=None, paramsFunction=[], color="#250045", onePress=False, fontstyle=None, fontsize=None):
        self.UIState = UIState
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
            self.fontstyle=UIState.mainfontstyle
        if fontsize!=None:
            self.fontsize=int(self.UIState.screen_height/(700/fontsize))
        else:
            self.fontsize=UIState.mainfontsize

        self.font=pygame.freetype.SysFont(self.fontstyle, self.fontsize)
        while self.text!="": #Runs in case the font is too big for the rectangle
                self.font=pygame.freetype.SysFont(self.fontstyle, self.fontsize)      
                text_rect = self.font.get_rect(self.text)
                if text_rect.width<self.width and text_rect.height<self.height:
                    break
                else:
                    self.fontsize-=1

        self.UIState.objects.append(self)

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
                    if self.UIState.isclicked==False:
                        self.onclickFunction(*self.paramsFunction)
                        self.alreadyPressed = True
                        self.UIState.isclicked=True

            else:
                self.alreadyPressed = False
                self.UIState.isclicked=False

        text_rect = self.font.get_rect(self.text)
        text_rect.center = self.buttonSurface.get_rect().center
        self.font.render_to(self.buttonSurface, text_rect.topleft, self.text, (255,255,255))

        self.UIState.screen.blit(self.buttonSurface, self.buttonRect)

class ImageButton():
    def __init__(self, UIState, x, y, width, height, img, text='', onclickFunction=None, paramsFunction=[], fontstyle=None, fontsize=None):
        self.UIState = UIState
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
            self.fontstyle=UIState.mainfontstyle
        if fontsize!=None:
            self.fontsize=int(UIState.screen_height/(700/fontsize))
        else:
            self.fontsize=UIState.mainfontsize

        self.font=pygame.freetype.SysFont(self.fontstyle, self.fontsize)
        while self.text!="": #Runs in case the font is too big for the rectangle
            self.font=pygame.freetype.SysFont(self.fontstyle, self.fontsize)      
            text_rect = self.font.get_rect(self.text)
            if text_rect.width<self.width and text_rect.height<self.height:
                break
            else:
                self.fontsize-=1

        self.UIState.objects.append(self)

    def process(self):
        mousePos = pygame.mouse.get_pos()
        
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
                    if self.UIState.isclicked==False:
                        self.onclickFunction(*self.paramsFunction)
                        self.UIState.isclicked=True

                else:
                    self.UIState.isclicked=False

        text_rect = self.font.get_rect(self.text)
        text_rect.center = image.get_rect().center
        self.font.render_to(image, text_rect.topleft, self.text, (255,255,255))

        self.UIState.screen.blit(image, (self.x,self.y))

class Map():
    def __init__(self, UIState, x, y, width, height, img, gamedata, regionviewfunction, colormode='main', party=None):
            self.UIState = UIState
            self.x = x
            self.y = y
            self.width = width
            self.height = height
            self.img = img
            self.gamedata = gamedata
            self.regionview = regionviewfunction
            self.colormode = colormode
            self.party = party
            
            
            self.baseimage=pygame.image.load(self.img)
            self.savedimages={}

            self.colors=self.coloringmode()
            self.UIState.objects.append(self)

    def coloringmode(self):
        colors={}
        if self.colormode=='main':
            #Can sort either by either seats or votes
            #partyregionresults=sorted(self.gamedata.polling.aggregated.partyregionresults, key=lambda x: (x.region.seats, x.region.population, x.region.name, x.seats, x.votes), reverse=True)
            partyregionresults=sorted(self.gamedata.polling.aggregated.partyregionresults, key=lambda x: (x.region.seats, x.region.population, x.region.name, x.votes, x.seats), reverse=True)

            region, firstmargin, secondmargin = partyregionresults[0].region, partyregionresults[0].percentage, 0
            winnercolor, normalcolor=np.array(partyregionresults[0].party.color), np.array([200,200,200])
            maxdifference=10

            for i in partyregionresults[1:]:
                if i.region!=region:
                    region, firstmargin, secondmargin = i.region, i.percentage, 0
                    winnercolor=np.array(i.party.color)
                elif secondmargin!=0:
                    continue
                else:
                    secondmargin=i.percentage
                    difference=min(maxdifference, firstmargin-secondmargin)
                    color=(normalcolor*(maxdifference-difference)+winnercolor*difference)/maxdifference
                    colors[region.name]=tuple(color)

            for i in self.gamedata.scenario.regions:
                if i.name not in colors:
                    colors[i.name]=self.gamedata.scenario.base.territorycolor

            #Old coloring, probably highly inefficient
            #for i in self.gamedata.scenario.regions:
            #    seatweights=[(j.seats/i.seats)**2.5 for j in partyregionresults if i==j.region]
            #    seatweights=[j/sum(seatweights) for j in seatweights]
            #    resultcolor=[0,0,0]
            #    for count, j in enumerate([k for k in partyregionresults if i==k.region]):
            #        resultcolor=[seatweights[count]*j.party.color[colorcount]+k for colorcount,k in enumerate(resultcolor)]
            #    colors[i.name]=tuple(resultcolor)

            #To get only the winner color, it's enough to only take the first value that is of different region
            #for i in partyregionresults:
            #    if i.region.name not in colors:
            #        colors[i.region.name]=i.party.color
        elif self.colormode=='party':
            for i in [i for i in self.gamedata.polling.aggregated.partyregionresults if i.party.fullname==self.party.fullname]:
                multiplicator=i.percentage/max([j.percentage for j in self.gamedata.polling.aggregated.partyregionresults if j.party.fullname==self.party.fullname])
                colors[i.region.name]=tuple([max(40,j*multiplicator) for j in i.party.color])
            for i in self.gamedata.scenario.regions:
                if i.name not in colors:
                    colors[i.name]=(0,0,0,255)

        return colors


    def prepareimage(self):
        mousePos = pygame.mouse.get_pos()
        arr=pygame.PixelArray(self.image)

        if self.buttonRect.collidepoint(mousePos):
            color=self.image.get_at((mousePos[0]-self.newx, mousePos[1]-self.newy))
            if color in [i.color for i in self.gamedata.scenario.regions if i.status=="state"]:
                [arr.replace(color, (80,80,80)) for i in self.gamedata.scenario.regions]
        
        [arr.replace(i.color, self.colors[i.name]) for i in self.gamedata.scenario.regions]

        arr.close()

        return self.image

    def process(self):
        mousePos = pygame.mouse.get_pos()

        self.image = self.baseimage
        reducesizeby=max(self.image.get_width()/self.width, self.image.get_height()/self.height)
        self.image = pygame.transform.scale(self.image,(round(self.image.get_width()/reducesizeby), round(self.image.get_height()/reducesizeby))).convert()
        self.newx, self.newy=round(self.x+((self.width-self.image.get_width())/2)), round(self.y+((self.height-self.image.get_height())/2))
        self.buttonRect = pygame.Rect(self.newx, self.newy, self.image.get_width(), self.image.get_height())
        
        #Checks if map, where the pixel with same color has already been saved in a dictionary.
        #If yes, takes image from dictionary. If not, image is created in self.prepareimage().
        if self.buttonRect.collidepoint(mousePos):
            chosencolor=self.image.get_at((mousePos[0]-self.newx, mousePos[1]-self.newy))
            color="-".join(str(i) for i in chosencolor)
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                if self.UIState.isclicked==False:
                    region=next((x for x in self.gamedata.scenario.regions if x.color == chosencolor and x.status=="state"), None)
                    if region:
                        self.regionview(self.UIState, self.gamedata.scenario.name, self.gamedata, region.name)
                        self.UIState.isclicked=True
            else:
                self.UIState.isclicked=False
            if color in self.savedimages:
                self.image=self.savedimages[color]
            else:
                self.image=self.prepareimage()
                self.savedimages[color]=self.image
        else:
            if "base" in self.savedimages:
                self.image=self.savedimages["base"]
            else:
                self.image=self.prepareimage()
                self.savedimages["base"]=self.image

        #print(self.image.get_at((2, 2)))
        self.UIState.screen.blit(self.image, (self.newx, self.newy))

class MultipleLineText():
    def __init__(self, UIState, x, y, width, height, color, text="", fontstyle=None, fontsize=None):
            self.UIState=UIState
            self.x = x
            self.y = y
            self.width = width
            self.height = height
            self.color = color
            self.text = text

            if fontstyle!=None:
                self.fontstyle=fontstyle
            else:
                self.fontstyle=UIState.mainfontstyle
            if fontsize!=None:
                self.fontsize=int(UIState.screen_height/(700/fontsize))
            else:
                self.fontsize=UIState.mainfontsize

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

            self.UIState.objects.append(self)

            self.Surface = pygame.Surface((self.width, self.height))
            self.Surface.fill(self.color)
            self.Rect = pygame.Rect(self.x, self.y, self.width, self.height)

            previous_height_total=0
            heightofline=self.font.get_rect("Tg").height
            for i in self.text:
                text_rect = self.font.get_rect(i)
                text_rect.y+=previous_height_total+(heightofline-text_rect.height)/2
                previous_height_total+=heightofline

                self.font.render_to(self.Surface, text_rect.topleft, i, (255,255,255))

    def process(self):
        self.UIState.screen.blit(self.Surface, self.Rect)
