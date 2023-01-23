import numpy as np
import re
import datetime

class Ideology:
      def __init__(self, name, fullname, effects):
        self.name = name
        self.fullname = fullname
        self.effects = effects

def main(scenarioname):
    ideologies=[]
    f = open ( 'scenario/' + scenarioname + '/ideologies.txt' , 'r')
    l = []
    l = np.array([ line.split() for line in f], dtype=object)

    currentideology=None
    fullname, effects="",[]
    effectreader=False
    
    for i in l:
        newi=" ".join(i).split('#')[0] #Joins all the characters, and then takes all of them until the first hashtag
        if not newi:
            continue
        string=re.search("(.*):", newi)
        if string:
            effectreader=False
            if string.group(1)=='effects':
                effectreader=True
            else:
                if currentideology!=None:
                    ideologies.append(Ideology(currentideology, fullname, effects))
                currentideology="".join(string[1].rstrip().lstrip())
                fullname, effects="",[]
        else:
            if effectreader==True:
                string=re.search("(.*)", newi)
                if string:
                    effects.append("".join(string[1].rstrip().lstrip()))
            else:
                string=re.search(".*fullname.*=(.*)", newi)
                if string:
                    word="".join(string[1].rstrip().lstrip())
                    fullname=word
                    continue
    
    ideologies.append(Ideology(currentideology, fullname, effects))

    return np.array(ideologies)