import numpy as np
import re
import datetime

class Party:
      def __init__(self, name, fullname, power, playable, color, ideologies, ruling=False, issues=None, populations=None, leader=None, player=False, characters=None, nationalseats=0):
        self.name = name
        self.fullname = fullname
        self.leader = leader
        self.characters=characters
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
              if operator=="=":
                  newleader=next((x for x in self.characters if x.identifier == variable), None)
                  if newleader:
                    #Removes effects from old leader
                    for i in self.leader.ideologies:
                        for j in i.effects:
                            TriggerHandler.executeeffect(j.replace('party', self.name), True)
                    for i in self.leader.traits:
                        for j in i.effects:
                            TriggerHandler.executeeffect(j.replace('party', self.name), True)
                    #Adds effcets from new leader
                    for i in newleader.ideologies:
                        for j in i.effects:
                            TriggerHandler.executeeffect(j.replace('party', self.name))
                    for i in newleader.traits:
                        for j in i.effects:
                            TriggerHandler.executeeffect(j.replace('party', self.name))
                    object.__setattr__(self, attr, newleader)
          else:
            if operator=="+":
                object.__setattr__(self, attr, super(Party, self).__getattribute__(attr)+float(variable))
            elif operator=="-":
                object.__setattr__(self, attr, super(Party, self).__getattribute__(attr)-float(variable))
            elif operator=="*":
                object.__setattr__(self, attr, super(Party, self).__getattribute__(attr)*float(variable))
            elif operator=="=":
                object.__setattr__(self, attr, float(variable))

def main(scenarioname):
    parties=[]
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