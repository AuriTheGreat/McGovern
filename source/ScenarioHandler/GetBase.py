import numpy as np
import re
import datetime

class Base:
      def __init__(self, name, nation, year, fiction, description, startdate, enddate, electiondate, turns, seats=None, population=None):
        self.name=name
        self.nation=nation
        self.year=year
        self.fiction=fiction
        self.description=description
        self.startdate=startdate
        self.enddate=enddate
        self.electiondate=electiondate
        self.turns=turns
        self.seats=seats
        self.population=population
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
    
    name=nation=year=fiction=description=startdate=enddate=electiondate=turns=seats=None
    
    for i in l:
        newi=" ".join(i).split('#')[0] #Joins all the characters, and then takes all of them until the first hashtag
        if not newi:
            continue
        string=re.search(".*name.*=(.*)", newi)
        if string:
            name="".join(string[1].rstrip().lstrip())
            continue
        string=re.search(".*nation.*=(.*)", newi)
        if string:
            nation="".join(string[1].rstrip().lstrip())
            continue
        string=re.search(".*year.*=(.*)", newi)
        if string:
            year=int("".join(string[1].rstrip().lstrip()))
            continue
        string=re.search(".*fiction.*=(.*)", newi)
        if string:
            fiction="".join(string[1].rstrip().lstrip())
            continue
        string=re.search(".*description.*=(.*)", newi)
        if string:
            description="".join(string[1].rstrip().lstrip())
            continue
        string=re.search(".*startdate.*=(.*)", newi)
        if string:
            startdate="".join(string[1].rstrip().lstrip())
            startdate=datetime.datetime.strptime(startdate, "%Y-%m-%d")
            continue
        string=re.search(".*enddate.*=(.*)", newi)
        if string:
            enddate="".join(string[1].rstrip().lstrip())
            enddate=datetime.datetime.strptime(enddate, "%Y-%m-%d")
            continue
        string=re.search(".*electiondate.*=(.*)", newi)
        if string:
            electiondate="".join(string[1].rstrip().lstrip())
            electiondate=datetime.datetime.strptime(electiondate, "%Y-%m-%d")
            continue
        string=re.search(".*turns.*=(.*)", newi)
        if string:
            turns=int("".join(string[1].rstrip().lstrip()))
            continue

    return Base(name, nation, year, fiction, description, startdate, enddate, electiondate, turns)