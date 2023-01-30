import numpy as np
import re
import datetime

class Region:
      def __init__(self, name, fullname, population, eligiblepopulation, seats, status, color, issues=None, populations=None):
        self.name = name
        self.fullname = fullname
        self.population = population
        self.eligiblepopulation = eligiblepopulation
        self.seats = seats
        self.status = status
        self.color = color
        self.issues = issues
        self.populations = populations
      def print(self):
        print("|", self.name.center(93), "|")
        print("+" + "".join(["-" for c in range(95)]) + "+")
        print("|", "Population".rjust(20), "|", f'{self.population:,}'[0:70].ljust(70), "|")
        print("|", "Eligible Population".rjust(20), "|", str(self.eligiblepopulation)[0:70].ljust(70), "|")
        print("|", "Seats".rjust(20), "|", str(self.seats)[0:70].ljust(70), "|")
        print("+" + "".join(["-" for c in range(22)]) + "+" + "".join(["-" for c in range(72)]) + "+")
        print("|", "".rjust(20), "|", "Issues"[0:70].center(70).ljust(70), "|")
        print("|", "".rjust(20), "|", "Name"[0:20].center(20).ljust(20), "Mean"[0:70].center(15).ljust(15), "Variance"[0:70].center(16).ljust(16), "Importance"[0:70].center(16).ljust(16), "|")
        print("|" + "".rjust(22) + "+" + "".join(["-" for c in range(72)]) + "+")
        for i in self.issues:
            print("|", "".rjust(20), "|", i.issue.fullname[0:20].center(20).ljust(20), str(round(i.mean,4)).center(15).ljust(15), str(round(i.variance,4)).center(16).ljust(16), str(round(i.importance,4)).center(16).ljust(16), "|")
        print("+" + "".join(["-" for c in range(95)]) + "+")
        print("|", "".rjust(20), "|", "Populations"[0:70].center(70).ljust(70), "|")
        print("|", "".rjust(20), "|", "Name"[0:20].center(20).ljust(20), "Influence"[0:70].center(49).ljust(49), "|")
        print("|" + "".rjust(22) + "+" + "".join(["-" for c in range(72)]) + "+")
        for i in self.populations:
            print("|", "".rjust(20), "|", i.population.fullname[0:20].center(20).ljust(20), str(round(i.influence,4)).center(49).ljust(49), "|")
        print("+" + "".join(["-" for c in range(95)]) + "+")

def main(scenarioname, base):
    regions=[]
    f = open ( 'scenario/' + scenarioname + '/regions.txt' , 'r')
    l = []
    l = np.array([ line.split() for line in f], dtype=object)
    
    currentregion=None
    population, fullname, eligiblepopulation, seats, status, color=None,None,None,None,"state",None
    
    for i in l:
        newi=" ".join(i).split('#')[0] #Joins all the characters, and then takes all of them until the first hashtag
        if not newi:
            continue
        string=re.search("(.*):", newi)
        if string:
            if currentregion!=None:
                regions.append(Region(currentregion, fullname, population, eligiblepopulation, seats, status, color))
            currentregion="".join(string[1].rstrip().lstrip())
            population, fullname, eligiblepopulation, seats, status, color=None,None,None,None,"state",None
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
            string=re.search(".*status.*=(.*)", newi)
            if string:
                status="".join(string[1].rstrip().lstrip())
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
    
    regions.append(Region(currentregion, fullname, population, eligiblepopulation, seats, status, color))

    base.seats=sum(region.seats for region in regions if region.status!="territory")
    base.population=sum(region.population for region in regions if region.status!="territory")


    regions.sort(key=lambda x: (x.population, x.fullname), reverse=True)
    return np.array(regions)