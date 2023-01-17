import numpy as np
import re
import datetime

class Character:
      def __init__(self, identifier, name, party, leader, homeregion, ideologies, traits):
        self.identifier = identifier
        self.name = name
        self.party = party
        self.leader = leader
        self.homeregion = homeregion
        self.ideologies = ideologies
        self.traits = traits

def main(scenarioname, parties, mainideologies, maintraits, regions):
    characters=[]
    f = open ( 'scenario/' + scenarioname + '/characters.txt' , 'r')
    l = []
    l = np.array([ line.split() for line in f], dtype=object)
    
    currentcharacter=None
    name, party, leader, homeregion, ideologies, traits=None, None, False, regions[0], [], []
    ideologyreader, traitreader=False, False
    currentparty, currentindex=None,None

    for i in l:
        newi=" ".join(i).split('#')[0] #Joins all the characters, and then takes all of them until the first hashtag
        if not newi:
            continue
        string=re.search("(.*):", newi)
        if string:
            ideologyreader, traitreader=False, False
            if string.group(1)=='ideologies':
                ideologyreader=True
            elif string.group(1)=='traits':
                traitreader=True
            else:
                if currentcharacter!=None:
                    characters.append(Character(currentcharacter, name, party, leader, homeregion, ideologies, traits))
                    if leader==True:
                        currentindex.leader=characters[len(characters)-1]
                currentcharacter="".join(string[1].rstrip().lstrip())
                name, party, leader, homeregion, ideologies, traits=None, None, False, regions[0], [], []
        else:
            if ideologyreader:
                string=re.search("(.*)", newi)
                if string:
                    string="".join(string[1].rstrip().lstrip())
                    ideology=next((x for x in mainideologies if x.name == string), None)
                    if ideology:
                        ideologies.append(ideology)
            elif traitreader:
                string=re.search("(.*)", newi)
                if string:
                    string="".join(string[1].rstrip().lstrip())
                    trait=next((x for x in maintraits if x.name == string), None)
                    if trait:
                        traits.append(trait)
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
                string=re.search(".*homeregion.*=(.*)", newi)
                if string:
                    homeregion="".join(string[1].rstrip().lstrip())
                    homeregion=next((x for x in regions if x.name == homeregion), regions[0])
                    continue
                string=re.search(".*leader.*=(.*)", newi)
                if string:
                    if "".join(string[1].rstrip().lstrip())=="True":
                        leader=True
                    else:
                        leader=False
                    continue
    
    characters.append(Character(currentcharacter, name, party, leader, homeregion, ideologies, traits))
    if leader==True:
        currentindex.leader=characters[len(characters)-1]

    characters.sort(key=lambda x: x.leader, reverse=True)

    for i in parties:
        i.characters=[]
        for j in characters:
            if j.party==i:
                i.characters.append(j)

    return np.array(characters)