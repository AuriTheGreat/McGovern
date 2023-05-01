import numpy as np
import re

class Decision:
    def __init__(self):
        self.identifier = None
        self.name = ""
        self.description = ""
        self.expiresafter = 0
        self.ignorable = False
        self.options = [] #contains Option objects
    def print(self):
        print(self.identifier)
        print(self.name)
        for i in self.options:
            i.print()

class Option:
    def __init__(self):
        self.name = ""
        self.privatedescription = ""
        self.newsdescription = ""
        self.condition = ""
        self.effects = [] #contains Effect objects
    def print(self):
        print(self.name)
        for i in self.effects:
            i.print()

class Effect:
    def __init__(self):
        self.condition = ""
        self.privatedescription = ""
        self.newsdescription = ""
        self.effects = [] #contains effect queries that are used by TriggerHandler
    def print(self):
        print(self.privatedescription)

def main(scenarioname):
    decisions=[]
    f = open ( 'scenario/' + scenarioname + '/decisions.txt' , 'r')
    l = []
    l = np.array([ line.split() for line in f], dtype=object)
    
    currentdecision=currentoption=currenteffect=None
    name, description, effects, hidden=None,[],[], False
    ifreader=privatedescriptionreader=newsdescriptionreader=effectreader=effectsreader= \
                optionsreader=maineffectsreader=ignoreeffectsreader=False

    for i in l:
        newi=" ".join(i).split('#')[0] #Joins all the characters, and then takes all of them until the first hashtag
        if not newi and privatedescriptionreader==newsdescriptionreader==False:
            continue
        string=re.search("(.*):", newi)
        if string:
            if string.group(1)=='if':
                ifreader=True
            elif string.group(1)=='privatedescription':
                ifreader=privatedescriptionreader=newsdescriptionreader=ignoreeffectsreader=effectsreader=False
                privatedescriptionreader=True
            elif string.group(1)=='newsdescription':
                ifreader=privatedescriptionreader=newsdescriptionreader=ignoreeffectsreader=effectsreader=False
                newsdescriptionreader=True
            elif string.group(1)=='option':
                currentoption=Option()
                currenteffect=None
                currentdecision.options.append(currentoption)
                print("Option")
            elif string.group(1)=='effect':
                ifreader=privatedescriptionreader=newsdescriptionreader=effectreader=effectsreader= \
                optionsreader=maineffectsreader=ignoreeffectsreader=False
                effectreader=True
                currenteffect=Effect()
                currentoption.effects.append(currenteffect)
                print("Effect")
            elif string.group(1)=='options':
                ifreader=privatedescriptionreader=newsdescriptionreader=effectreader=effectsreader= \
                optionsreader=maineffectsreader=ignoreeffectsreader=False
                optionsreader=True
                continue
            elif string.group(1)=='maineffects':
                ifreader=privatedescriptionreader=newsdescriptionreader=effectreader=effectsreader= \
                maineffectsreader=ignoreeffectsreader=False
                maineffectsreader=True
            elif string.group(1)=='effects':
                effectsreader=True
            elif string.group(1)=='ignoreeffects':
                ignoreeffectsreader=True
            else:
                if optionsreader==effectreader==True:
                    continue
                else:
                    currentoption=currenteffect=None
                    currentdecision=Decision()
                    decisions.append(currentdecision)
                    currentdecision.identifier="".join(string[1].rstrip().lstrip())
                    print("Decision:", currentdecision.identifier)
        else:
            if effectreader==True:
                string=re.search("(.*)", newi)
                if string:
                    effects.append("".join(string[1].rstrip().lstrip()))
            else:
                string=re.search(".*optionname.*=(.*)", newi)
                if string:
                    currentoption.name="".join(string[1].rstrip().lstrip())
                    continue
                string=re.search(".*name.*=(.*)", newi)
                if string:
                    currentdecision.name="".join(string[1].rstrip().lstrip())
                    continue
                string=re.search(".*expiresafter.*=(.*)", newi)
                if string:
                    currentdecision.expiresafter=int("".join(string[1].rstrip().lstrip()))
                    continue
                string=re.search(".*ignorable.*=(.*)", newi)
                if string:
                    string="".join(string[1].rstrip().lstrip())
                    if string=="true":
                        currentdecision.ignorable=True
                    else:
                        currentdecision.ignorable=False
                    continue


    for i in decisions:
        i.print()
    return decisions