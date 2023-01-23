import numpy as np
import re
import datetime

class PartyRegion:
      def __init__(self, party, region, power, controlledseats, guaranteedseats):
        self.party = party
        self.region = region
        self.power = power
        self.controlledseats = controlledseats
        self.guaranteedseats = guaranteedseats

      def validvariables(self):
          #The key is the name of the attribute. The value describes how the variable is formatted.
          return {"controlledseats": self.party.name+"."+self.region.name+".controlledseats", 
                  "guaranteedseats": self.party.name+"."+self.region.name+".guaranteedseats",
                  "power": self.party.name+"."+self.region.name+".power"}
      
      def getvariable(self, attr):
          return super(PartyRegion, self).__getattribute__(attr)
    
      def setvariable(self, attr, variable, operator):
          if attr=="controlledseats" or attr=="guaranteedseats":
              if operator=="*":
                  print("Can't multiply controlledseats or guaranteedseats")
                  return
              variable=int(variable)
          else:
              variable=float(variable)

          if attr=="controlledseats":
              if operator=="+":
                self.party.nationalseats+=variable
                object.__setattr__(self, attr, super(PartyRegion, self).__getattribute__(attr)+variable)
              elif operator=="-":
                self.party.nationalseats-=variable
                object.__setattr__(self, attr, super(PartyRegion, self).__getattribute__(attr)-variable)
              elif operator=="=":
                self.party.nationalseats-=self.controlledseats
                object.__setattr__(self, attr, variable)
                self.party.nationalseats+=self.controlledseats
          else:
            if operator=="+":
                object.__setattr__(self, attr, super(PartyRegion, self).__getattribute__(attr)+variable)
            elif operator=="-":
                object.__setattr__(self, attr, super(PartyRegion, self).__getattribute__(attr)-variable)
            elif operator=="*":
                object.__setattr__(self, attr, super(PartyRegion, self).__getattribute__(attr)*variable)
            elif operator=="=":
                object.__setattr__(self, attr, variable)

def main(scenarioname, parties, regions):
    partyregions={}
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