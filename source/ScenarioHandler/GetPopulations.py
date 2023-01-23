import numpy as np
import re
import datetime

class Population:
      def __init__(self, name, fullname, pollingbias, financialpower, regions, parties):
        self.name = name
        self.fullname = fullname
        self.pollingbias = pollingbias
        self.financialpower = financialpower
        self.regions=regions
        self.parties=parties

def main(scenarioname):
    populations=[]
    f = open ( 'scenario/' + scenarioname + '/populations.txt' , 'r')
    l = []
    l = np.array([ line.split() for line in f], dtype=object)
    
    currentpopulation=None
    fullname, pollingbias, financialpower=None,None,None
    
    for i in l:
        newi=" ".join(i).split('#')[0] #Joins all the characters, and then takes all of them until the first hashtag
        if not newi:
            continue
        string=re.search("(.*):", newi)
        if string:
            if currentpopulation!=None:
                populations.append(Population(currentpopulation, fullname, pollingbias, financialpower, [], []))
            currentpopulation="".join(string[1].rstrip().lstrip())
            fullname, pollingbias, financialpower=None,None,None
        else:
            string=re.search(".*fullname.*=(.*)", newi)
            if string:
                fullname="".join(string[1].rstrip().lstrip())
                continue
            string=re.search(".*pollingbias.*=(.*)", newi)
            if string:
                pollingbias=float("".join(string[1].rstrip().lstrip()))
                continue
            string=re.search(".*financialpower.*=(.*)", newi)
            if string:
                financialpower=float("".join(string[1].rstrip().lstrip()))
                continue
    
    populations.append(Population(currentpopulation, fullname, pollingbias, financialpower, [], []))

    return np.array(populations)