import numpy as np
import re
import datetime

class Trait:
      def __init__(self, name, fullname, effects):
        self.name = name
        self.fullname = fullname
        self.effects = effects

def main(scenarioname):
    traits=[]
    class Trait:
      def __init__(self, name, fullname, effects):
        self.name = name
        self.fullname = fullname
        self.effects = effects
    
    
    f = open ( 'scenario/' + scenarioname + '/traits.txt' , 'r')
    l = []
    l = np.array([ line.split() for line in f], dtype=object)

    currenttrait=None
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
                if currenttrait!=None:
                    traits.append(Trait(currenttrait, fullname, effects))
                currenttrait="".join(string[1].rstrip().lstrip())
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
    
    traits.append(Trait(currenttrait, fullname, effects))

    return np.array(traits)