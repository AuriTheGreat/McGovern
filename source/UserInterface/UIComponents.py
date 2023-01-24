import pygame
import math

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
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.surface = pygame.Surface((self.UIState.screen_width, self.UIState.screen_height), pygame.SRCALPHA)
        self.transparency=60

        self.UIState.objects.append(self)

    def process(self):
        color=tuple(list(self.color) + [self.transparency])
        pygame.draw.circle(self.surface,color,(self.x, self.y), self.radius)
        self.UIState.screen.blit(self.surface, (0,0))
        self.x+=20
        self.transparency=min(255,self.transparency+30)

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

            self.colors=self.coloringmode()
            self.UIState.objects.append(self)

    def coloringmode(self):
        colors={}
        if self.colormode=='main':
            colors={i.name:i.resultcolor for i in self.gamedata.scenario.regions}
        elif self.colormode=='party':
            for i in [i for i in self.gamedata.polling.aggregated.partyregionresults if i.party.fullname==self.party.fullname]:
                multiplicator=i.percentage/max([j.percentage for j in self.gamedata.polling.aggregated.partyregionresults if j.party.fullname==self.party.fullname])
                colors[i.region.name]=tuple([max(40,j*multiplicator) for j in i.party.color])

        return colors


    def process(self):
        mousePos = pygame.mouse.get_pos()
        global isclicked
        
        self.image = self.baseimage
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
                    if self.UIState.isclicked==False:
                        self.regionview(self.UIState, self.gamedata.scenario.name, self.gamedata, next((x for x in self.gamedata.scenario.regions if x.color == color), None).name)
                        self.UIState.isclicked=True
                else:
                    self.UIState.isclicked=False
        
        [arr.replace(i.color, self.colors[i.name]) for i in self.gamedata.scenario.regions]

        arr.close()

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

    def process(self):
        self.UIState.screen.blit(self.Surface, self.Rect)

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

        self.UIState.screen.blit(self.Surface, (self.x,self.y))
