import numpy as np
import re
import datetime

class Base:
      def __init__(self):
        self.name=None
        self.nation=None
        self.year=None
        self.fiction=None
        self.description=None
        self.startdate=None
        self.enddate=None
        self.electiondate=None
        self.turns=None
        
        #Style
        self.territorycolor=(100, 100, 100, 255)

        #System
        self.electoralsystem="Proportional"
        
        #Calculated later
        self.seats=None
        self.population=None


      def print(self):
        print("+" + "".join(["-" for c in range(95)]) + "+")
        print("|", "BASE".center(93), "|")
        print("+" + "".join(["-" for c in range(95)]) + "+")
        print("|", "Name".rjust(20), "|", self.name[0:70].ljust(70), "|")
        print("|", "Nation".rjust(20), "|", self.nation[0:70].ljust(70), "|")
        print("|", "Year".rjust(20), "|", str(self.year)[0:70].ljust(70), "|")
        print("|", "Fiction".rjust(20), "|", self.fiction[0:70].ljust(70), "|")
        print("|", "Description".rjust(20), "|", self.description[0:70].ljust(70), "|")
        print("|", "Start date".rjust(20), "|", str(self.startdate.date())[0:70].ljust(70), "|")
        print("|", "End date".rjust(20), "|", str(self.enddate.date())[0:70].ljust(70), "|")
        print("|", "Election date".rjust(20), "|", str(self.electiondate.date())[0:70].ljust(70), "|")
        print("|", "Turns".rjust(20), "|", str(self.turns)[0:70].ljust(70), "|")
        print("|", "Population".rjust(20), "|", f'{self.population:,}'[0:70].ljust(70), "|")
        print("|", "Seats".rjust(20), "|", str(self.seats)[0:70].ljust(70), "|")
        print("+" + "".join(["-" for c in range(95)]) + "+")

def main(scenarioname):
    f = open ( 'scenario/' + scenarioname + '/main.txt' , 'r')
    l = []
    l = np.array([ line.split() for line in f], dtype=object)
    
    base=Base()
    
    for i in l:
        newi=" ".join(i).split('#')[0] #Joins all the characters, and then takes all of them until the first hashtag
        if not newi:
            continue
        string=re.search(".*name.*=(.*)", newi)
        if string:
            base.name="".join(string[1].rstrip().lstrip())
            continue
        string=re.search(".*nation.*=(.*)", newi)
        if string:
            base.nation="".join(string[1].rstrip().lstrip())
            continue
        string=re.search(".*year.*=(.*)", newi)
        if string:
            base.year=int("".join(string[1].rstrip().lstrip()))
            continue
        string=re.search(".*fiction.*=(.*)", newi)
        if string:
            base.fiction="".join(string[1].rstrip().lstrip())
            continue
        string=re.search(".*description.*=(.*)", newi)
        if string:
            base.description="".join(string[1].rstrip().lstrip())
            continue
        string=re.search(".*startdate.*=(.*)", newi)
        if string:
            startdate="".join(string[1].rstrip().lstrip())
            base.startdate=datetime.datetime.strptime(startdate, "%Y-%m-%d")
            continue
        string=re.search(".*enddate.*=(.*)", newi)
        if string:
            enddate="".join(string[1].rstrip().lstrip())
            base.enddate=datetime.datetime.strptime(enddate, "%Y-%m-%d")
            continue
        string=re.search(".*electiondate.*=(.*)", newi)
        if string:
            electiondate="".join(string[1].rstrip().lstrip())
            base.electiondate=datetime.datetime.strptime(electiondate, "%Y-%m-%d")
            continue
        string=re.search(".*turns.*=(.*)", newi)
        if string:
            base.turns=int("".join(string[1].rstrip().lstrip()))
            continue
        string=re.search(".*territorycolor.*=(.*)", newi)
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
            base.territorycolor=tuple(color)
            continue

        string=re.search(".*electoralsystem.*=(.*)", newi)
        if string:
            base.electoralsystem="".join(string[1].rstrip().lstrip())
            continue

    return base