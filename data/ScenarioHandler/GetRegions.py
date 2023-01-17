import numpy as np
import re
import datetime

class Region:
      def __init__(self, name, fullname, population, eligiblepopulation, seats, color, issues=None, populations=None, resultcolor=None):
        self.name = name
        self.fullname = fullname
        self.population = population
        self.eligiblepopulation = eligiblepopulation
        self.seats = seats
        self.color = color
        self.issues = issues
        self.populations = populations
        self.resultcolor = resultcolor

def main(scenarioname, base):
    regions=[]
    f = open ( 'scenario/' + scenarioname + '/regions.txt' , 'r')
    l = []
    l = np.array([ line.split() for line in f], dtype=object)
    
    currentregion=None
    population, fullname, eligiblepopulation, seats, color=None,None,None,None,None
    
    for i in l:
        newi=" ".join(i).split('#')[0] #Joins all the characters, and then takes all of them until the first hashtag
        if not newi:
            continue
        string=re.search("(.*):", newi)
        if string:
            if currentregion!=None:
                regions.append(Region(currentregion, fullname, population, eligiblepopulation, seats, color))
            currentregion="".join(string[1].rstrip().lstrip())
            population, fullname, eligiblepopulation, seats, color=None,None,None,None,None
        else:
            string=re.search(".*fullname.*=(.*)", newi)
            if string:
                fullname="".join(string[1].rstrip().lstrip())
                continue
            string=re.search(".*eligiblepopulation.*=(.*)", newi)
            if string:
                eligiblepopulation=float("".join(string[1].rstrip().lstrip()))
                continue
            string=re.search(".*population.*=(.*)", newi)
            if string:
                population=int("".join(string[1].rstrip().lstrip()))
                continue
            string=re.search(".*seats.*=(.*)", newi)
            if string:
                seats=int("".join(string[1].rstrip().lstrip()))
                continue
            string=re.search(".*color.*=(.*)", newi)
            if string:
                tempcolor=list("".join(string[1].rstrip().lstrip()))
                color=[[]]
                for i in tempcolor:
                    if i!=',':
                        color[len(color)-1].append(i)
                    else:
                        color.append([])
                for count,i in enumerate(color):
                    color[count]=int("".join(i))
                #color.append(255)
                color=tuple(color)
                continue
    
    regions.append(Region(currentregion, fullname, population, eligiblepopulation, seats, color))

    base.seats=sum(region.seats for region in regions)
    base.population=sum(region.population for region in regions)


    regions.sort(key=lambda x: x.population, reverse=True)
    return np.array(regions)