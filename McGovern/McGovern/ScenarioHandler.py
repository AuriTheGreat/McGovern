from operator import truediv
from pickle import TRUE
import numpy as np
import re
import datetime

class Scenario:
      def __init__(self, name, main=None, base=None, issues=None, parties=None, ideologies=None, characters=None, outcomes=None, regions=None, populations=None, partyissues=None, partypopulations=None, regionissues=None, regionpopulations=None, partyregions=None, events=None, decisions=None, triggers=None, variables=None):
        self.name = name
        self.main = main
        self.base = base
        self.issues = issues
        self.parties = parties
        self.ideologies = ideologies
        self.characters = characters
        self.outcomes = outcomes
        self.regions = regions
        self.populations = populations
        self.partyissues = partyissues
        self.partypopulations = partypopulations
        self.regionissues = regionissues
        self.regionpopulations = regionpopulations
        self.partyregions = partyregions
        self.events = events
        self.decisions = decisions
        self.triggers = triggers
        self.variables = variables
      def printbase(self):
        print("+" + "".join(["-" for c in range(95)]) + "+")
        print("|", "BASE".center(93), "|")
        print("+" + "".join(["-" for c in range(95)]) + "+")
        print("|", "Name".rjust(20), "|", self.base.name[0:70].ljust(70), "|")
        print("|", "Nation".rjust(20), "|", self.base.nation[0:70].ljust(70), "|")
        print("|", "Year".rjust(20), "|", str(self.base.year)[0:70].ljust(70), "|")
        print("|", "Fiction".rjust(20), "|", self.base.fiction[0:70].ljust(70), "|")
        print("|", "Description".rjust(20), "|", self.base.description[0:70].ljust(70), "|")
        print("|", "Start date".rjust(20), "|", str(self.base.startdate.date())[0:70].ljust(70), "|")
        print("|", "End date".rjust(20), "|", str(self.base.enddate.date())[0:70].ljust(70), "|")
        print("|", "Election date".rjust(20), "|", str(self.base.electiondate.date())[0:70].ljust(70), "|")
        print("|", "Turns".rjust(20), "|", str(self.base.turns)[0:70].ljust(70), "|")
        print("|", "Population".rjust(20), "|", f'{self.base.population:,}'[0:70].ljust(70), "|")
        print("|", "Seats".rjust(20), "|", str(self.base.seats)[0:70].ljust(70), "|")
        print("+" + "".join(["-" for c in range(95)]) + "+")
      def printparties(self):
        print("+" + "".join(["-" for c in range(95)]) + "+")
        print("|", "PARTIES".center(93), "|")
        print("+" + "".join(["-" for c in range(95)]) + "+")
        for i in self.parties:
            print("|", i.name.center(93), "|")
            print("+" + "".join(["-" for c in range(95)]) + "+")
            print("|", "Full name".rjust(20), "|", i.fullname[0:70].ljust(70), "|")
            if i.leader!=None:
                print("|", "Leader".rjust(20), "|", str(i.leader.name)[0:70].ljust(70), "|")
            else:
                print("|", "Leader".rjust(20), "|", "None"[0:70].ljust(70), "|")
            print("|", "Power".rjust(20), "|", str(round(i.power,4))[0:70].ljust(70), "|")
            print("|", "Ideologies".rjust(20), "|", ", ".join(i.ideologies)[0:70].ljust(70), "|")
            print("+" + "".join(["-" for c in range(22)]) + "+" + "".join(["-" for c in range(72)]) + "+")
            print("|", "".rjust(20), "|", "Issues"[0:70].center(70).ljust(70), "|")
            print("|", "".rjust(20), "|", "Name"[0:20].center(20).ljust(20), "Mean"[0:70].center(24).ljust(24), "Variance"[0:70].center(24).ljust(24), "|")
            print("|" + "".rjust(22) + "+" + "".join(["-" for c in range(72)]) + "+")
            for j in i.issues:
                print("|", "".rjust(20), "|", j.issue.fullname[0:20].center(20).ljust(20), str(round(j.mean,4)).center(24).ljust(24), str(round(j.variance,4)).center(24).ljust(24), "|")
            print("+" + "".join(["-" for c in range(95)]) + "+")
            print("|", "".rjust(20), "|", "Populations"[0:70].center(70).ljust(70), "|")
            print("|", "".rjust(20), "|", "Name"[0:20].center(20).ljust(20), "Appeal"[0:70].center(49).ljust(49), "|")
            print("|" + "".rjust(22) + "+" + "".join(["-" for c in range(72)]) + "+")
            for j in i.populations:
                print("|", "".rjust(20), "|", j.population.fullname[0:20].center(20).ljust(20), str(round(j.appeal,4)).center(49).ljust(49), "|")
            print("+" + "".join(["-" for c in range(95)]) + "+")

      def printregions(self):
        print("+" + "".join(["-" for c in range(95)]) + "+")
        print("|", "REGIONS".center(93), "|")
        print("+" + "".join(["-" for c in range(95)]) + "+")
        for i in self.regions:
            print("|", i.name.center(93), "|")
            print("+" + "".join(["-" for c in range(95)]) + "+")
            print("|", "Population".rjust(20), "|", f'{i.population:,}'[0:70].ljust(70), "|")
            print("|", "Eligible Population".rjust(20), "|", str(i.eligiblepopulation)[0:70].ljust(70), "|")
            print("|", "Seats".rjust(20), "|", str(i.seats)[0:70].ljust(70), "|")
            print("+" + "".join(["-" for c in range(22)]) + "+" + "".join(["-" for c in range(72)]) + "+")
            print("|", "".rjust(20), "|", "Issues"[0:70].center(70).ljust(70), "|")
            print("|", "".rjust(20), "|", "Name"[0:20].center(20).ljust(20), "Mean"[0:70].center(15).ljust(15), "Variance"[0:70].center(16).ljust(16), "Importance"[0:70].center(16).ljust(16), "|")
            print("|" + "".rjust(22) + "+" + "".join(["-" for c in range(72)]) + "+")
            for j in i.issues:
                print("|", "".rjust(20), "|", j.issue.fullname[0:20].center(20).ljust(20), str(round(j.mean,4)).center(15).ljust(15), str(round(j.variance,4)).center(16).ljust(16), str(round(j.importance,4)).center(16).ljust(16), "|")
            print("+" + "".join(["-" for c in range(95)]) + "+")
            print("|", "".rjust(20), "|", "Populations"[0:70].center(70).ljust(70), "|")
            print("|", "".rjust(20), "|", "Name"[0:20].center(20).ljust(20), "Influence"[0:70].center(49).ljust(49), "|")
            print("|" + "".rjust(22) + "+" + "".join(["-" for c in range(72)]) + "+")
            for j in i.populations:
                print("|", "".rjust(20), "|", j.population.fullname[0:20].center(20).ljust(20), str(round(j.influence,4)).center(49).ljust(49), "|")
            print("+" + "".join(["-" for c in range(95)]) + "+")
      def printcharacters(self):
        print("+" + "".join(["-" for c in range(95)]) + "+")
        print("|", "CHARACTERS".center(93), "|")
        print("+" + "".join(["-" for c in range(95)]) + "+")
        for i in self.characters:
            print("|", i.name.center(93), "|")
            print("+" + "".join(["-" for c in range(95)]) + "+")
            print("|", "Name".rjust(20), "|", i.name[0:70].ljust(70), "|")
            print("|", "Party".rjust(20), "|", str(i.party.fullname)[0:70].ljust(70), "|")
            print("|", "Ideologies".rjust(20), "|", ", ".join(i.ideologies)[0:70].ljust(70), "|")
            print("+" + "".join(["-" for c in range(95)]) + "+")
      def printalldata(self):
        self.printbase()
        print("")
        self.printparties()
        print("")
        self.printregions()
        print("")
        self.printcharacters()
        print("")


def getbase(scenarioname):
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

def getmain(scenarioname, base):
    class Main:
        def __init__(self, currentdate, turnlength):
            self.currentdate = currentdate
            self.turnlength = turnlength

        def newturn(self):
            self.currentdate+=self.turnlength

        def validvariables(self):
            return {"currentdate": "date"}
        
        def getvariable(self, attr):
            return super(Main, self).__getattribute__(attr)
    
        def setvariable(self, attr, newvalue):
            object.__setattr__(self, attr, newvalue)

    currentdate=base.startdate
    turnlength=(base.enddate-currentdate)/base.turns

    return Main(currentdate, turnlength)

def getissues(scenarioname):
    issues=[]

    class Issue:
      def __init__(self, name, fullname, levels, parties, regions):
        self.name = name
        self.fullname = fullname
        self.levels = levels
        self.parties = parties
        self.regions = regions
    
    
    f = open ( 'scenario/' + scenarioname + '/issues.txt' , 'r')
    l = []
    l = np.array([ line.split() for line in f], dtype=object)
    
    currentissue=None
    fullname, levels=None,[]
    levelreader=None
    
    for i in l:
        newi=" ".join(i).split('#')[0] #Joins all the characters, and then takes all of them until the first hashtag
        if not newi:
            continue
        string=re.search("(.*):", newi)
        if string:
            levelreader=None
            if string.group(1)=='levels':
                levelreader='levels'
            else:
                if currentissue!=None:
                    issues.append(Issue(currentissue, fullname, levels, [], []))
                currentissue="".join(string[1].rstrip().lstrip())
                fullname, levels=None,[]
        else:
            if levelreader!=None:
                string=re.search("(.*)", newi)
                if string:
                    levels.append("".join(string[1].rstrip().lstrip()))
            else:
                string=re.search(".*fullname.*=(.*)", newi)
                if string:
                    fullname="".join(string[1].rstrip().lstrip())
                    continue
    
    issues.append(Issue(currentissue, fullname, levels, [], []))

    return np.array(issues)

def getpopulations(scenarioname):
    populations=[]

    class Population:
      def __init__(self, name, fullname, pollingbias, financialpower, regions, parties):
        self.name = name
        self.fullname = fullname
        self.pollingbias = pollingbias
        self.financialpower = financialpower
        self.regions=regions
        self.parties=parties
    
    
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

def getregions(scenarioname, base):
    regions=[]

    class Region:
      def __init__(self, name, population, eligiblepopulation, seats, color, issues=None, populations=None, resultcolor=None):
        self.name = name
        self.population = population
        self.eligiblepopulation = eligiblepopulation
        self.seats = seats
        self.color = color
        self.issues = issues
        self.populations = populations
        self.resultcolor = resultcolor
    
    
    f = open ( 'scenario/' + scenarioname + '/regions.txt' , 'r')
    l = []
    l = np.array([ line.split() for line in f], dtype=object)
    
    currentregion=None
    population, eligiblepopulation, seats, color=None,None,None,None
    
    for i in l:
        newi=" ".join(i).split('#')[0] #Joins all the characters, and then takes all of them until the first hashtag
        if not newi:
            continue
        string=re.search("(.*):", newi)
        if string:
            if currentregion!=None:
                regions.append(Region(currentregion, population, eligiblepopulation, seats, color))
            currentregion="".join(string[1].rstrip().lstrip())
            population, eligiblepopulation, seats, color=None,None,None,None
        else:
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
    
    regions.append(Region(currentregion, population, eligiblepopulation, seats, color))

    base.seats=sum(region.seats for region in regions)
    base.population=sum(region.population for region in regions)


    regions.sort(key=lambda x: x.population, reverse=True)
    return np.array(regions)

def getparties(scenarioname):
    parties=[]
    
    class Party:
      def __init__(self, name, fullname, power, playable, color, ideologies, ruling=False, issues=None, populations=None, leader=None, player=False, nationalseats=0):
        self.name = name
        self.fullname = fullname
        self.leader = leader
        self.power = power
        self.playable = playable
        self.color = color
        self.ideologies = ideologies
        self.issues = issues
        self.populations = populations
        self.player = player
        self.ruling = ruling
        self.nationalseats = nationalseats


    
      def validvariables(self):
          #The key is the name of the attribute. The value describes how the variable is formatted.
          return {"leader": self.name+".leader", "power": self.name+".power"}
      
      def getvariable(self, attr):
          if attr=="leader":
            return super(Party, self).__getattribute__(attr).identifier
          else:
            return super(Party, self).__getattribute__(attr)
    
      def setvariable(self, attr, variable, operator):
          if attr=="leader":
              pass
          else:
            if operator=="+":
                object.__setattr__(self, attr, super(Party, self).__getattribute__(attr)+float(variable))
            elif operator=="-":
                object.__setattr__(self, attr, super(Party, self).__getattribute__(attr)-float(variable))
            elif operator=="=":
                object.__setattr__(self, attr, float(variable))
    
    
    f = open ( 'scenario/' + scenarioname + '/parties.txt' , 'r')
    l = []
    l = np.array([ line.split() for line in f], dtype=object)
    
    currentparty=None
    fullname,playable,ruling,power,ideologies,color=None,False,False,None,[],None
    ideologyreader=None
    
    for i in l:
        newi=" ".join(i).split('#')[0] #Joins all the characters, and then takes all of them until the first hashtag
        if not newi:
            continue
        string=re.search("(.*):", newi)
        if string:
            ideologyreader=None
            if string.group(1)=='aiideologies':
                ideologyreader='aiideologies'
            elif string.group(1)=='extraideologies':
                ideologyreader='extraideologies'
            else:
                if currentparty!=None:
                    parties.append(Party(currentparty, fullname, power, playable, color, ideologies, ruling))
                currentparty="".join(string[1].rstrip().lstrip())
                fullname,playable,ruling,power,ideologies,color=None,False,False,None,[],None
        else:
            if ideologyreader!=None:
                string=re.search("(.*)", newi)
                if string:
                    ideologies.append("".join(string[1].rstrip().lstrip()))
            else:
                string=re.search(".*playable.*=(.*)", newi)
                if string:
                    if "".join(string[1].rstrip().lstrip())=="True":
                        playable=True
                    else:
                        playable=False
                    continue
                string=re.search(".*ruling.*=(.*)", newi)
                if string:
                    if "".join(string[1].rstrip().lstrip())=="True":
                        ruling=True
                    else:
                        ruling=False
                    continue
                string=re.search(".*power.*=(.*)", newi)
                if string:
                    power=float("".join(string[1].rstrip().lstrip()))
                    continue
                string=re.search(".*fullname.*=(.*)", newi)
                if string:
                    fullname="".join(string[1].rstrip().lstrip())
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
    
    parties.append(Party(currentparty, fullname, power, playable, color, ideologies, ruling))

    return np.array(parties)

def getcharacters(scenarioname, parties):
    characters=[]
    
    class Character:
      def __init__(self, identifier, name, party, leader, ideologies):
        self.identifier = identifier
        self.name = name
        self.party = party
        self.leader = leader
        self.ideologies = ideologies
    
    
    f = open ( 'scenario/' + scenarioname + '/characters.txt' , 'r')
    l = []
    l = np.array([ line.split() for line in f], dtype=object)
    
    currentcharacter=None
    name, party,leader,ideologies=None, None,False,[]
    ideologyreader=None
    currentparty, currentindex=None,None
    
    for i in l:
        newi=" ".join(i).split('#')[0] #Joins all the characters, and then takes all of them until the first hashtag
        if not newi:
            continue
        string=re.search("(.*):", newi)
        if string:
            ideologyreader=None
            if string.group(1)=='aiideologies':
                ideologyreader='aiideologies'
            else:
                if currentcharacter!=None:
                    characters.append(Character(currentcharacter, name, party, leader, ideologies))
                    if leader==True:
                        currentindex.leader=characters[len(characters)-1]
                currentcharacter="".join(string[1].rstrip().lstrip())
                name, party,leader,ideologies=None, None,False,[]
        else:
            if ideologyreader!=None:
                string=re.search("(.*)", newi)
                if string:
                    ideologies.append("".join(string[1].rstrip().lstrip()))
            else:
                string=re.search(".*name.*=(.*)", newi)
                if string:
                    name="".join(string[1].rstrip().lstrip())
                    continue
                string=re.search(".*party.*=(.*)", newi)
                if string:
                    party="".join(string[1].rstrip().lstrip())
                    if party==currentparty:
                        party=currentindex
                    else:
                        currentindex=next((x for x in parties if x.name == party), None)
                        party=currentindex
                    continue
                string=re.search(".*leader.*=(.*)", newi)
                if string:
                    if "".join(string[1].rstrip().lstrip())=="True":
                        leader=True
                    else:
                        leader=False
                    continue
    
    characters.append(Character(currentcharacter, name, party, leader, ideologies))
    if leader==True:
        currentindex.leader=characters[len(characters)-1]

    characters.sort(key=lambda x: x.leader, reverse=True)
    return np.array(characters)

def partyissuehandler(scenarioname, parties, issues):
    partyissues={}

    class PartyIssue:
      def __init__(self, party, issue, mean, variance):
        self.party = party
        self.issue = issue
        self.mean = mean
        self.variance = variance

      def validvariables(self):
          #The key is the name of the attribute. The value describes how the variable is formatted.
          return {"mean": self.issue.name+"."+self.party.name+".mean",
                  "variance": self.issue.name+"."+self.party.name+".variance"}
      
      def getvariable(self, attr):
          return super(PartyIssue, self).__getattribute__(attr)
    
      def setvariable(self, attr, variable, operator):
          if operator=="+":
              object.__setattr__(self, attr, super(PartyIssue, self).__getattribute__(attr)+float(variable))
          elif operator=="-":
              object.__setattr__(self, attr, super(PartyIssue, self).__getattribute__(attr)-float(variable))
          elif operator=="=":
              object.__setattr__(self, attr, float(variable))

    f = open ( 'scenario/' + scenarioname + '/partyissue.txt' , 'r')
    l = []
    l = np.array([ line.split() for line in f], dtype=object)

    for i in parties:
        for j in issues:
            partyissues[str(str(i.name)+"-"+str(j.name))]=PartyIssue(i,j,0,1)

    partynames=[x.name for x in parties]
    issuenames=[x.name for x in issues]

    party,issue=None,None

    for i in l:
        newi=" ".join(i).split('#')[0] #Joins all the characters, and then takes all of them until the first hashtag
        if not newi:
            continue
        string=re.search("(.*):", newi)
        if string:
            if string[1] in partynames:
                party=next((x for x in parties if x.name == string[1]), None)
            elif string[1] in issuenames:
                issue=next((x for x in issues if x.name == string[1]), None)
            else:
                issue=None
        else:
            if issue!=None:
                string=re.search(".*mean.*=(.*)", newi)
                if string:
                    partyissues[str(party.name + "-" + issue.name)].mean=float("".join(string[1].rstrip().lstrip()))
                    continue
                string=re.search(".*variance.*=(.*)", newi)
                if string:
                    partyissues[str(party.name + "-" + issue.name)].variance=float("".join(string[1].rstrip().lstrip()))
                    continue

    for i in parties:
        i.issues=[]
        for j in partyissues.values():
            if j.party==i:
                j.issue.parties.append(j)
                i.issues.append(j)

    f = open ( 'scenario/' + scenarioname + '/partyissue.txt' , 'w')
    f.write("### DO NOT WRITE ANY COMMENTS, THEY WILL BE REFRESHED.\n")
    for i in parties:
        f.write(i.name + ":" + "\n")
        for j in i.issues:
            f.write("\t" + j.issue.name + ":" + "\n")
            f.write("\t\t" + "mean=" + str(j.mean) + "\n")
            f.write("\t\t" + "variance=" + str(j.variance) + "\n")
        
    return list(partyissues.values())

def regionissuehandler(scenarioname, regions, issues):
    regionissues={}

    class RegionIssue:
      def __init__(self, region, issue, mean, variance, importance):
        self.region = region
        self.issue = issue
        self.mean = mean
        self.variance = variance
        self.importance = importance

      def validvariables(self):
          #The key is the name of the attribute. The value describes how the variable is formatted.
          return {"mean": self.issue.name+"."+self.region.name+".mean",
                  "variance": self.issue.name+"."+self.region.name+".variance",
                  "importance": self.issue.name+"."+self.region.name+".importance"}
      
      def getvariable(self, attr):
          return super(RegionIssue, self).__getattribute__(attr)
    
      def setvariable(self, attr, variable, operator):
          if operator=="+":
              object.__setattr__(self, attr, super(RegionIssue, self).__getattribute__(attr)+float(variable))
          elif operator=="-":
              object.__setattr__(self, attr, super(RegionIssue, self).__getattribute__(attr)-float(variable))
          elif operator=="=":
              object.__setattr__(self, attr, float(variable))


    f = open ( 'scenario/' + scenarioname + '/regionissue.txt' , 'r')
    l = []
    l = np.array([ line.split() for line in f], dtype=object)

    for i in regions:
        for j in issues:
            regionissues[str(str(i.name)+"-"+str(j.name))]=RegionIssue(i,j,0,1,0)


    regionnames=[x.name for x in regions]
    issuenames=[x.name for x in issues]

    region,issue=None,None

    for i in l:
        newi=" ".join(i).split('#')[0] #Joins all the characters, and then takes all of them until the first hashtag
        if not newi:
            continue
        string=re.search("(.*):", newi)
        if string:
            if string[1] in regionnames:
                region=next((x for x in regions if x.name == string[1]), None)
            elif string[1] in issuenames:
                issue=next((x for x in issues if x.name == string[1]), None)
            else:
                issue=None
        else:
            if issue!=None:
                string=re.search(".*mean.*=(.*)", newi)
                if string:
                    regionissues[str(region.name + "-" + issue.name)].mean=float("".join(string[1].rstrip().lstrip()))
                    continue
                string=re.search(".*variance.*=(.*)", newi)
                if string:
                    regionissues[str(region.name + "-" + issue.name)].variance=float("".join(string[1].rstrip().lstrip()))
                    continue
                string=re.search(".*importance.*=(.*)", newi)
                if string:
                    regionissues[str(region.name + "-" + issue.name)].importance=float("".join(string[1].rstrip().lstrip()))
                    continue

    for i in regions:
        i.issues=[]
        for j in regionissues.values():
            if j.region==i:
                j.issue.regions.append(j)
                i.issues.append(j)

    f = open ( 'scenario/' + scenarioname + '/regionissue.txt' , 'w')
    f.write("### DO NOT WRITE ANY COMMENTS, THEY WILL BE REFRESHED.\n")
    for i in regions:
        f.write(i.name + ":" + "\n")
        for j in i.issues:
            f.write("\t" + j.issue.name + ":" + "\n")
            f.write("\t\t" + "mean=" + str(j.mean) + "\n")
            f.write("\t\t" + "variance=" + str(j.variance) + "\n")
            f.write("\t\t" + "importance=" + str(j.importance) + "\n")

    return list(regionissues.values())

def regionpopulationhandler(scenarioname, regions, populations):
    regionpopulations={}

    class RegionPopulation:
      def __init__(self, region, population, influence):
        self.region = region
        self.population = population
        self.influence = influence

      def validvariables(self):
          #The key is the name of the attribute. The value describes how the variable is formatted.
          return {"influence": self.population.name+"."+self.region.name+".influence"}
      
      def getvariable(self, attr):
          return super(RegionPopulation, self).__getattribute__(attr)
    
      def setvariable(self, attr, variable, operator):
          if operator=="+":
              object.__setattr__(self, attr, super(RegionPopulation, self).__getattribute__(attr)+float(variable))
          elif operator=="-":
              object.__setattr__(self, attr, super(RegionPopulation, self).__getattribute__(attr)-float(variable))
          elif operator=="=":
              object.__setattr__(self, attr, float(variable))

    f = open ( 'scenario/' + scenarioname + '/regionpopulation.txt' , 'r')
    l = []
    l = np.array([ line.split() for line in f], dtype=object)

    for i in regions:
        for j in populations:
            regionpopulations[str(str(i.name)+"-"+str(j.name))]=RegionPopulation(i,j,0)


    regionnames=[x.name for x in regions]
    populationnames=[x.name for x in populations]

    region,population=None,None

    for i in l:
        newi=" ".join(i).split('#')[0] #Joins all the characters, and then takes all of them until the first hashtag
        if not newi:
            continue
        string=re.search("(.*):", newi)
        if string:
            if string[1] in regionnames:
                region=next((x for x in regions if x.name == string[1]), None)
            elif string[1] in populationnames:
                population=next((x for x in populations if x.name == string[1]), None)
            else:
                population=None
        else:
            if population!=None:
                string=re.search(".*influence.*=(.*)", newi)
                if string:
                    regionpopulations[str(region.name + "-" + population.name)].influence=float("".join(string[1].rstrip().lstrip()))
                    continue

    for i in regions:
        i.populations=[]
        for j in regionpopulations.values():
            if j.region==i:
                j.population.regions.append(j)
                i.populations.append(j)

    f = open ( 'scenario/' + scenarioname + '/regionpopulation.txt' , 'w')
    f.write("### DO NOT WRITE ANY COMMENTS, THEY WILL BE REFRESHED.\n")
    for i in regions:
        f.write(i.name + ":" + "\n")
        for j in i.populations:
            f.write("\t" + j.population.name + ":" + "\n")
            f.write("\t\t" + "influence=" + str(j.influence) + "\n")

    return list(regionpopulations.values())

def partypopulationhandler(scenarioname, parties, populations):
    partypopulations={}

    class PartyPopulation:
      def __init__(self, party, population, appeal):
        self.party = party
        self.population = population
        self.appeal = appeal

      def validvariables(self):
          #The key is the name of the attribute. The value describes how the variable is formatted.
          return {"appeal": self.population.name+"."+self.party.name+".appeal"}
      
      def getvariable(self, attr):
          return super(PartyPopulation, self).__getattribute__(attr)
    
      def setvariable(self, attr, variable, operator):
          if operator=="+":
              object.__setattr__(self, attr, super(PartyPopulation, self).__getattribute__(attr)+float(variable))
          elif operator=="-":
              object.__setattr__(self, attr, super(PartyPopulation, self).__getattribute__(attr)-float(variable))
          elif operator=="=":
              object.__setattr__(self, attr, float(variable))

    f = open ( 'scenario/' + scenarioname + '/partypopulation.txt' , 'r')
    l = []
    l = np.array([ line.split() for line in f], dtype=object)

    for i in parties:
        for j in populations:
            partypopulations[str(str(i.name)+"-"+str(j.name))]=PartyPopulation(i,j,0)


    partynames=[x.name for x in parties]
    populationnames=[x.name for x in populations]

    party,population=None,None

    for i in l:
        newi=" ".join(i).split('#')[0] #Joins all the characters, and then takes all of them until the first hashtag
        if not newi:
            continue
        string=re.search("(.*):", newi)
        if string:
            if string[1] in partynames:
                party=next((x for x in parties if x.name == string[1]), None)
            elif string[1] in populationnames:
                population=next((x for x in populations if x.name == string[1]), None)
            else:
                population=None
        else:
            if population!=None:
                string=re.search(".*appeal.*=(.*)", newi)
                if string:
                    partypopulations[str(party.name + "-" + population.name)].appeal=float("".join(string[1].rstrip().lstrip()))
                    continue

    for i in parties:
        i.populations=[]
        for j in partypopulations.values():
            if j.party==i:
                j.population.parties.append(j)
                i.populations.append(j)

    f = open ( 'scenario/' + scenarioname + '/partypopulation.txt' , 'w')
    f.write("### DO NOT WRITE ANY COMMENTS, THEY WILL BE REFRESHED.\n")
    for i in parties:
        f.write(i.name + ":" + "\n")
        for j in i.populations:
            f.write("\t" + j.population.name + ":" + "\n")
            f.write("\t\t" + "appeal=" + str(j.appeal) + "\n")

    return list(partypopulations.values())

def getpartyregions(scenarioname, parties, regions):
    partyregions={}

    class PartyRegion:
      def __init__(self, party, region, power, controlledseats, guaranteedseats):
        self.party = party
        self.region = region
        self.power = power
        self.controlledseats = controlledseats
        self.guaranteedseats = guaranteedseats

    f = open ( 'scenario/' + scenarioname + '/partyregion.txt' , 'r')
    l = []
    l = np.array([ line.split() for line in f], dtype=object)

    for i in parties:
        for j in regions:
            partyregions[str(str(i.name)+"-"+str(j.name))]=PartyRegion(i,j,0,0,0)


    partynames=[x.name for x in parties]
    regionnames=[x.name for x in regions]

    party,region=None,None

    for i in l:
        newi=" ".join(i).split('#')[0] #Joins all the characters, and then takes all of them until the first hashtag
        if not newi:
            continue
        string=re.search("(.*):", newi)
        if string:
            if string[1] in partynames:
                party=next((x for x in parties if x.name == string[1]), None)
            elif string[1] in regionnames:
                region=next((x for x in regions if x.name == string[1]), None)
            else:
                region=None
        else:
            if region!=None:
                string=re.search(".*power.*=(.*)", newi)
                if string:
                    partyregions[str(party.name + "-" + region.name)].power=float("".join(string[1].rstrip().lstrip()))
                    continue
                string=re.search(".*controlledseats.*=(.*)", newi)
                if string:
                    partyregions[str(party.name + "-" + region.name)].controlledseats=max(0, int("".join(string[1].rstrip().lstrip())))
                    party.nationalseats+=partyregions[str(party.name + "-" + region.name)].controlledseats
                    continue
                string=re.search(".*guaranteedseats.*=(.*)", newi)
                if string:
                    partyregions[str(party.name + "-" + region.name)].guaranteedseats=max(0, int("".join(string[1].rstrip().lstrip())))
                    continue

    f = open ( 'scenario/' + scenarioname + '/partyregion.txt' , 'w')
    f.write("### DO NOT WRITE ANY COMMENTS, THEY WILL BE REFRESHED.\n")
    party=None
    for i in partyregions.values():
        if i.party!=party:
            party=i.party
            f.write(i.party.name + ":" + "\n")
            for j in partyregions.values():
                if i.party==j.party:
                    f.write("\t" + j.region.name + ":" + "\n")
                    f.write("\t\t" + "power=" + str(j.power) + "\n")
                    f.write("\t\t" + "controlledseats=" + str(j.controlledseats) + " #These are seats that party currently has in parliament." + "\n")
                    f.write("\t\t" + "guaranteedseats=" + str(j.guaranteedseats) + " #This is the lowest amount of seats the party will win in next election." + "\n")

    return list(partyregions.values())

def getevents(scenarioname):
    events=[]

    class Event:
      def __init__(self, identifier, name, hidden, description, effects):
        self.identifier = identifier
        self.name = name
        self.hidden = hidden
        self.description = description
        self.effects = effects
    
    
    f = open ( 'scenario/' + scenarioname + '/events.txt' , 'r')
    l = []
    l = np.array([ line.split() for line in f], dtype=object)
    
    currentevent=None
    name, description, effects, hidden=None,[],[], False
    descriptionreader=effectsreader=False
    
    for i in l:
        newi=" ".join(i).split('#')[0] #Joins all the characters, and then takes all of them until the first hashtag
        if not newi:
            continue
        string=re.search("(.*):", newi)
        if string:
            descriptionreader=effectsreader=False
            if string.group(1)=='description':
                descriptionreader=True
            elif string.group(1)=='effects':
                effectsreader=True
            else:
                if currentevent!=None:
                    events.append(Event(currentevent, name, hidden, description, effects))
                currentevent="".join(string[1].rstrip().lstrip())
                name, description, effects, hidden=None,[],[], False
        else:
            if effectsreader==True:
                string=re.search("(.*)", newi)
                if string:
                    effects.append("".join(string[1].rstrip().lstrip()))
            elif descriptionreader==True:
                string=re.search("(.*)", newi)
                if string:
                    description.append("".join(string[1].rstrip().lstrip()))
            else:
                string=re.search(".*name.*=(.*)", newi)
                if string:
                    name="".join(string[1].rstrip().lstrip())
                    continue
                string=re.search(".*hidden.*=(.*)", newi)
                if string:
                    text="".join(string[1].rstrip().lstrip())
                    if text=="True":
                        hidden=True
                    else:
                        hidden=False
                    continue

    
    events.append(Event(currentevent, name, hidden, description, effects))
     
    return np.array(events)

def getdecisions(scenarioname):
    return None

def gettriggers(scenarioname, events, decisions):
    triggers=[]

    class Trigger:
      def __init__(self, identifier, condition, triggered, triggerable, triggeronce, chance):
        self.identifier = identifier
        self.condition = condition
        self.triggered = triggered
        self.triggerable = triggerable
        self.triggeronce = triggeronce
        self.chance = chance
    
    
    f = open ( 'scenario/' + scenarioname + '/triggers.txt' , 'r')
    l = []
    l = np.array([ line.split() for line in f], dtype=object)
    
    currenttrigger=None
    condition, triggered, triggerable, triggeronce, chance ="",[], True, True, 0
    conditionreader, triggeredreader=False, False
    
    for i in l:
        newi=" ".join(i).split('#')[0] #Joins all the characters, and then takes all of them until the first hashtag
        if not newi:
            continue
        string=re.search("(.*):", newi)
        if string:
            conditionreader, triggeredreader=False, False
            if string.group(1)=='if':
                conditionreader=True
            elif string.group(1)=='trigger':
                triggeredreader=True
            else:
                if currenttrigger!=None:
                    triggers.append(Trigger(currenttrigger, condition, triggered, triggerable, triggeronce, chance))
                currenttrigger="".join(string[1].rstrip().lstrip())
                condition, triggered, triggerable, triggeronce, chance ="",[], True, True, 0
        else:
            if conditionreader==True:
                string=re.search("(.*)", newi)
                if string:
                    condition+=" " + "".join(string[1].rstrip().lstrip())
            elif triggeredreader==True:
                string=re.search("(.*)", newi)
                #print(currenttrigger)
                if string:
                    string="".join(string[1].rstrip().lstrip())
                    typeoftrigger=re.search("(.*)\.", string)
                    if typeoftrigger:
                        typeoftrigger="".join(typeoftrigger[1].rstrip().lstrip())
                        if typeoftrigger=='event':
                            event=re.search("\.(.*)", string)
                            event="".join(event[1].rstrip().lstrip())
                            triggered.append(next((x for x in events if x.identifier == event), None))
                        elif typeoftrigger=='decision':
                            decision=re.search("\.(.*)", string)
                            decision="".join(decision[1].rstrip().lstrip())
                            triggered.append(next((x for x in decisions if x.identifier == decision), None))

            else:
                string=re.search(".*triggerable.*=(.*)", newi)
                if string:
                    word="".join(string[1].rstrip().lstrip())
                    if word=="True":
                        triggerable=True
                    elif word=="False":
                        triggerable=False
                    continue
                string=re.search(".*triggeronce.*=(.*)", newi)
                if string:
                    word="".join(string[1].rstrip().lstrip())
                    if word=="True":
                        triggeronce=True
                    elif word=="False":
                        triggeronce=False
                    continue
                string=re.search(".*chance.*=(.*)%", newi)
                if string:
                    chance=float("".join(string[1].rstrip().lstrip()))/100
                    continue
    
    triggers.append(Trigger(currenttrigger, condition, triggered, triggerable, triggeronce, chance))

    return np.array(triggers)

def getvariables(scenarioname):
    variables=[]

    class Variable:
      def __init__(self, identifier, value):
        self.identifier = identifier
        self.value = value

      def validvariables(self):
          #The key is the name of the attribute. The value describes how the variable is formatted.
          return {"value": self.identifier}
      
      def getvariable(self, attr):
          return super(Variable, self).__getattribute__(attr)
    
      def setvariable(self, attr, variable, operator):
          if operator=="+":
              object.__setattr__(self, attr, super(Variable, self).__getattribute__(attr)+float(variable))
          elif operator=="-":
              object.__setattr__(self, attr, super(Variable, self).__getattribute__(attr)-float(variable))
          elif operator=="=":
              object.__setattr__(self, attr, float(variable))

    f = open ( 'scenario/' + scenarioname + '/variables.txt' , 'r')
    l = []
    l = np.array([ line.split() for line in f], dtype=object)
    
    identifier=value=None
    
    for i in l:
        newi=" ".join(i).split('#')[0] #Joins all the characters, and then takes all of them until the first hashtag
        if not newi:
            continue
        string1=re.search("(.*)=.*", newi)
        string2=re.search(".*=(.*)", newi)
        if string1 and string2:
            identifier="".join(string1[1].rstrip().lstrip())
            value=float("".join(string2[1].rstrip().lstrip()))
            variables.append(Variable(identifier, value))
            continue

    return variables

def main(scenarioname):
    scenario=Scenario(scenarioname)
    scenario.base=getbase(scenarioname)
    scenario.main=getmain(scenarioname, scenario.base)
    scenario.parties=getparties(scenarioname)
    scenario.issues=getissues(scenarioname)
    scenario.populations=getpopulations(scenarioname)
    scenario.regions=getregions(scenarioname, scenario.base)
    scenario.characters=getcharacters(scenarioname,scenario.parties)
    scenario.partyissues=partyissuehandler(scenarioname,scenario.parties,scenario.issues)
    scenario.regionissues=regionissuehandler(scenarioname,scenario.regions,scenario.issues)
    scenario.regionpopulations=regionpopulationhandler(scenarioname,scenario.regions,scenario.populations)
    scenario.partypopulations=partypopulationhandler(scenarioname,scenario.parties,scenario.populations)
    scenario.partyregions=getpartyregions(scenarioname, scenario.parties, scenario.regions)
    scenario.events=getevents(scenarioname)
    scenario.decisions=getdecisions(scenarioname)
    scenario.triggers=gettriggers(scenarioname, scenario.events, scenario.decisions)
    scenario.variables=getvariables(scenarioname)

    #scenario.printalldata()

    #print(next((x for x in scenario.partyissues if x.party.name == "labour" and x.issue.name== "tariffs"), None).variance)
    #print(next((x for x in scenario.regionissues if x.region.name == "Wales" and x.issue.name== "immigration"), None).variance)

    return scenario