from pickle import TRUE
import numpy as np
import re

class Scenario:
      def __init__(self, name, main=None, issues=None, parties=None, ideologies=None, characters=None, outcomes=None, regions=None, populations=None, partyissues=None, partydemographics=None, regionissues=None, regiondemographics=None):
        self.name = name
        self.main = main
        self.issues = issues
        self.parties = parties
        self.ideologies = ideologies
        self.characters = characters
        self.outcomes = outcomes
        self.regions = regions
        self.populations = populations
        self.partyissues = partyissues
        self.partydemographics = partydemographics
        self.regionissues = regionissues
        self.regiondemographics = regiondemographics
      def printmain(self):
        print("+" + "".join([chr(0x2015) for c in range(95)]) + "+")
        print("|", "MAIN".center(93), "|")
        print("+" + "".join([chr(0x2015) for c in range(95)]) + "+")
        print("|", "Name".rjust(20), "|", self.main.name[0:70].ljust(70), "|")
        print("|", "Nation".rjust(20), "|", self.main.nation[0:70].ljust(70), "|")
        print("|", "Year".rjust(20), "|", str(self.main.year)[0:70].ljust(70), "|")
        print("|", "Fiction".rjust(20), "|", self.main.fiction[0:70].ljust(70), "|")
        print("|", "Description".rjust(20), "|", self.main.description[0:70].ljust(70), "|")
        print("|", "Start date".rjust(20), "|", self.main.startdate[0:70].ljust(70), "|")
        print("|", "End date".rjust(20), "|", self.main.enddate[0:70].ljust(70), "|")
        print("|", "Election date".rjust(20), "|", self.main.electiondate[0:70].ljust(70), "|")
        print("|", "Turns".rjust(20), "|", str(self.main.turns)[0:70].ljust(70), "|")
        print("|", "Population".rjust(20), "|", f'{self.main.population:,}'[0:70].ljust(70), "|")
        print("|", "Seats".rjust(20), "|", str(self.main.seats)[0:70].ljust(70), "|")
        print("+" + "".join([chr(0x2015) for c in range(95)]) + "+")
      def printparties(self):
        print("+" + "".join([chr(0x2015) for c in range(95)]) + "+")
        print("|", "PARTIES".center(93), "|")
        print("+" + "".join([chr(0x2015) for c in range(95)]) + "+")
        for i in self.parties:
            print("|", i.name.center(93), "|")
            print("+" + "".join([chr(0x2015) for c in range(95)]) + "+")
            print("|", "Full name".rjust(20), "|", i.fullname[0:70].ljust(70), "|")
            print("|", "Leader".rjust(20), "|", str(i.leader.name)[0:70].ljust(70), "|")
            print("|", "Power".rjust(20), "|", str(round(i.power,4))[0:70].ljust(70), "|")
            print("|", "Ideologies".rjust(20), "|", ", ".join(i.ideologies)[0:70].ljust(70), "|")
            print("+" + "".join([chr(0x2015) for c in range(22)]) + "+" + "".join([chr(0x2015) for c in range(72)]) + "+")
            print("|", "".rjust(20), "|", "Issues"[0:70].center(70).ljust(70), "|")
            print("|", "".rjust(20), "|", "Name"[0:20].center(20).ljust(20), "Mean"[0:70].center(24).ljust(24), "Variance"[0:70].center(24).ljust(24), "|")
            print("|" + "".rjust(22) + "+" + "".join([chr(0x2015) for c in range(72)]) + "+")
            for j in i.issues:
                print("|", "".rjust(20), "|", j.issue.fullname[0:20].center(20).ljust(20), str(round(j.mean,4)).center(24).ljust(24), str(round(j.variance,4)).center(24).ljust(24), "|")
            print("+" + "".join([chr(0x2015) for c in range(95)]) + "+")
      def printregions(self):
        print("+" + "".join([chr(0x2015) for c in range(95)]) + "+")
        print("|", "REGIONS".center(93), "|")
        print("+" + "".join([chr(0x2015) for c in range(95)]) + "+")
        for i in self.regions:
            print("|", i.name.center(93), "|")
            print("+" + "".join([chr(0x2015) for c in range(95)]) + "+")
            print("|", "Population".rjust(20), "|", f'{i.population:,}'[0:70].ljust(70), "|")
            print("|", "Eligible Population".rjust(20), "|", str(i.eligiblepopulation)[0:70].ljust(70), "|")
            print("|", "Seats".rjust(20), "|", str(i.seats)[0:70].ljust(70), "|")
            print("+" + "".join([chr(0x2015) for c in range(22)]) + "+" + "".join([chr(0x2015) for c in range(72)]) + "+")
            print("|", "".rjust(20), "|", "Issues"[0:70].center(70).ljust(70), "|")
            print("|", "".rjust(20), "|", "Name"[0:20].center(20).ljust(20), "Mean"[0:70].center(15).ljust(15), "Variance"[0:70].center(16).ljust(16), "Importance"[0:70].center(16).ljust(16), "|")
            print("|" + "".rjust(22) + "+" + "".join([chr(0x2015) for c in range(72)]) + "+")
            for j in i.issues:
                print("|", "".rjust(20), "|", j.issue.fullname[0:20].center(20).ljust(20), str(round(j.mean,4)).center(15).ljust(15), str(round(j.variance,4)).center(16).ljust(16), str(round(j.importance,4)).center(16).ljust(16), "|")
            print("+" + "".join([chr(0x2015) for c in range(95)]) + "+")
      def printcharacters(self):
        print("+" + "".join([chr(0x2015) for c in range(95)]) + "+")
        print("|", "CHARACTERS".center(93), "|")
        print("+" + "".join([chr(0x2015) for c in range(95)]) + "+")
        for i in self.characters:
            print("|", i.name.center(93), "|")
            print("+" + "".join([chr(0x2015) for c in range(95)]) + "+")
            print("|", "Name".rjust(20), "|", i.name[0:70].ljust(70), "|")
            print("|", "Party".rjust(20), "|", str(i.party.fullname)[0:70].ljust(70), "|")
            print("|", "Ideologies".rjust(20), "|", ", ".join(i.ideologies)[0:70].ljust(70), "|")
            print("+" + "".join([chr(0x2015) for c in range(95)]) + "+")
      def printalldata(self):
        self.printmain()
        print("")
        self.printparties()
        print("")
        self.printregions()
        print("")
        self.printcharacters()
        print("")


def getmain(scenarioname):
    class Main:
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
        newi=" ".join(i)
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
            continue
        string=re.search(".*enddate.*=(.*)", newi)
        if string:
            enddate="".join(string[1].rstrip().lstrip())
            continue
        string=re.search(".*electiondate.*=(.*)", newi)
        if string:
            electiondate="".join(string[1].rstrip().lstrip())
            continue
        string=re.search(".*turns.*=(.*)", newi)
        if string:
            turns=int("".join(string[1].rstrip().lstrip()))
            continue

    return Main(name, nation, year, fiction, description, startdate, enddate, electiondate, turns)

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
        newi=" ".join(i)
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

    return issues

def getregions(scenarioname, main):
    regions=[]

    class Region:
      def __init__(self, name, population, eligiblepopulation, seats, issues=None):
        self.name = name
        self.population = population
        self.eligiblepopulation = eligiblepopulation
        self.seats = seats
        self.issues = issues
    
    
    f = open ( 'scenario/' + scenarioname + '/regions.txt' , 'r')
    l = []
    l = np.array([ line.split() for line in f], dtype=object)
    
    currentregion=None
    population, eligiblepopulation, seats=None,None,None
    
    for i in l:
        newi=" ".join(i)
        string=re.search("(.*):", newi)
        if string:
            if currentregion!=None:
                regions.append(Region(currentregion, population, eligiblepopulation, seats))
            currentregion="".join(string[1].rstrip().lstrip())
            population, eligiblepopulation, seats=None,None,None
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
    
    regions.append(Region(currentregion, population, eligiblepopulation, seats))

    main.seats=sum(region.seats for region in regions)
    main.population=sum(region.population for region in regions)


    regions.sort(key=lambda x: x.population, reverse=True)
    return regions

def getparties(scenarioname):
    parties=[]
    
    class Party:
      def __init__(self, name, fullname, power, ideologies, leader=None, issues=None, demographics=None):
        self.name = name
        self.fullname = fullname
        self.leader = leader
        self.power = power
        self.ideologies = ideologies
    
    
    f = open ( 'scenario/' + scenarioname + '/parties.txt' , 'r')
    l = []
    l = np.array([ line.split() for line in f], dtype=object)
    
    currentparty=None
    fullname,power,ideologies=None,None,[]
    ideologyreader=None
    
    for i in l:
        newi=" ".join(i)
        string=re.search("(.*):", newi)
        if string:
            ideologyreader=None
            if string.group(1)=='aiideologies':
                ideologyreader='aiideologies'
            elif string.group(1)=='extraideologies':
                ideologyreader='extraideologies'
            else:
                if currentparty!=None:
                    parties.append(Party(currentparty, fullname, power, ideologies))
                currentparty="".join(string[1].rstrip().lstrip())
                fullname,power,ideologies=None,None,[]
        else:
            if ideologyreader!=None:
                string=re.search("(.*)", newi)
                if string:
                    ideologies.append("".join(string[1].rstrip().lstrip()))
            else:
                string=re.search(".*power.*=(.*)", newi)
                if string:
                    power=float("".join(string[1].rstrip().lstrip()))
                    continue
                string=re.search(".*fullname.*=(.*)", newi)
                if string:
                    fullname="".join(string[1].rstrip().lstrip())
                    continue
    
    parties.append(Party(currentparty, fullname, power, ideologies))

    return parties

def getcharacters(scenarioname, parties):
    characters=[]
    
    class Character:
      def __init__(self, name, party, leader, ideologies):
        self.name = name
        self.party = party
        self.leader = leader
        self.ideologies = ideologies
    
    
    f = open ( 'scenario/' + scenarioname + '/characters.txt' , 'r')
    l = []
    l = np.array([ line.split() for line in f], dtype=object)
    
    currentcharacter=None
    party,leader,ideologies=None,False,[]
    ideologyreader=None
    currentparty, currentindex=None,None
    
    for i in l:
        newi=" ".join(i)
        string=re.search("(.*):", newi)
        if string:
            ideologyreader=None
            if string.group(1)=='aiideologies':
                ideologyreader='aiideologies'
            else:
                if currentcharacter!=None:
                    characters.append(Character(currentcharacter, party, leader, ideologies))
                    if leader==True:
                        currentindex.leader=characters[len(characters)-1]
                currentcharacter="".join(string[1].rstrip().lstrip())
                party,leader,ideologies=None,False,[]
        else:
            if ideologyreader!=None:
                string=re.search("(.*)", newi)
                if string:
                    ideologies.append("".join(string[1].rstrip().lstrip()))
            else:
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
    
    characters.append(Character(currentcharacter, party, leader, ideologies))
    if leader==True:
        currentindex.leader=characters[len(characters)-1]

    characters.sort(key=lambda x: x.leader, reverse=True)
    return characters

def partyissuehandler(scenarioname, parties, issues):
    neededelements = [str(p + "-" + i) for p in (o.name for o in parties) for i in (o.name for o in issues)]
    elements=[]
    partyissues=[]

    class PartyIssue:
      def __init__(self, party, issue, mean, variance):
        self.party = party
        self.issue = issue
        self.mean = mean
        self.variance = variance

    f = open ( 'scenario/' + scenarioname + '/partyissue.txt' , 'r')
    l = []
    l = np.array([ line.split() for line in f], dtype=object)

    currentpartyissue=None
    party,issue,mean,variance=None,None,None,None

    for i in l:
        newi=" ".join(i)
        string=re.search("(.*):", newi)
        if string:
            if currentpartyissue!=None:
                partyissues.append(PartyIssue(party, issue, mean, variance))
            currentpartyissue="".join(string[1].rstrip().lstrip())
            elements.append(currentpartyissue)
            party=next((x for x in parties if x.name == re.search("(.*)-", currentpartyissue)[1]), None)
            issue=next((x for x in issues if x.name == re.search("-(.*)", currentpartyissue)[1]), None)
            mean,variance=None,None
        else:
            string=re.search(".*mean.*=(.*)", newi)
            if string:
                mean=float("".join(string[1].rstrip().lstrip()))
                continue
            string=re.search(".*variance.*=(.*)", newi)
            if string:
                variance=float("".join(string[1].rstrip().lstrip()))
                continue

    partyissues.append(PartyIssue(party, issue, mean, variance))

    neededelements = [x for x in neededelements if x not in elements]

    f = open ( 'scenario/' + scenarioname + '/partyissue.txt' , 'a')
    for i in neededelements:
        f.write(i + ":" + "\n")
        f.write("\t" + "mean=0" + "\n")
        f.write("\t" + "variance=0" + "\n")

    for i in parties:
        i.issues=[]
        for j in partyissues:
            if j.party==i:
                j.issue.parties.append(j)
                i.issues.append(j)
        
    return partyissues

def regionissuehandler(scenarioname, regions, issues):
    neededelements = [str(r + "-" + i) for r in (o.name for o in regions) for i in (o.name for o in issues)]
    elements=[]
    regionissues=[]

    class RegionIssue:
      def __init__(self, region, issue, mean, variance, importance):
        self.region = region
        self.issue = issue
        self.mean = mean
        self.variance = variance
        self.importance = importance

    f = open ( 'scenario/' + scenarioname + '/regionissue.txt' , 'r')
    l = []
    l = np.array([ line.split() for line in f], dtype=object)

    currentregionissue=None
    region,issue,mean,variance,importance=None,None,None,None, None

    for i in l:
        newi=" ".join(i)
        string=re.search("(.*):", newi)
        if string:
            if currentregionissue!=None:
                regionissues.append(RegionIssue(region, issue, mean, variance, importance))
            currentregionissue="".join(string[1].rstrip().lstrip())
            elements.append(currentregionissue)
            region=next((x for x in regions if x.name == re.search("(.*)-", currentregionissue)[1]), None)
            issue=next((x for x in issues if x.name == re.search("-(.*)", currentregionissue)[1]), None)
            mean,variance,importance=None,None,None
        else:
            string=re.search(".*mean.*=(.*)", newi)
            if string:
                mean=float("".join(string[1].rstrip().lstrip()))
                continue
            string=re.search(".*variance.*=(.*)", newi)
            if string:
                variance=float("".join(string[1].rstrip().lstrip()))
                continue
            string=re.search(".*importance.*=(.*)", newi)
            if string:
                importance=float("".join(string[1].rstrip().lstrip()))
                continue

    regionissues.append(RegionIssue(region, issue, mean, variance, importance))

    neededelements = [x for x in neededelements if x not in elements]

    f = open ( 'scenario/' + scenarioname + '/regionissue.txt' , 'a')
    for i in neededelements:
        f.write(i + ":" + "\n")
        f.write("\t" + "mean=0" + "\n")
        f.write("\t" + "variance=0" + "\n")
        f.write("\t" + "importance=0" + "\n")

    for i in regions:
        i.issues=[]
        for j in regionissues:
            if j.region==i:
                j.issue.regions.append(j)
                i.issues.append(j)

    return regionissues



def main(scenarioname):
    scenario=Scenario(scenarioname)
    scenario.main=getmain(scenarioname)
    scenario.parties=getparties(scenarioname)
    scenario.issues=getissues(scenarioname)
    scenario.regions=getregions(scenarioname, scenario.main)
    scenario.characters=getcharacters(scenarioname,scenario.parties)
    scenario.partyissues=partyissuehandler(scenarioname,scenario.parties,scenario.issues)
    scenario.regionissues=regionissuehandler(scenarioname,scenario.regions,scenario.issues)

    #scenario.printalldata()

    #print(next((x for x in scenario.partyissues if x.party.name == "labour" and x.issue.name== "tariffs"), None).variance)
    #print(next((x for x in scenario.regionissues if x.region.name == "Wales" and x.issue.name== "immigration"), None).variance)

    return scenario