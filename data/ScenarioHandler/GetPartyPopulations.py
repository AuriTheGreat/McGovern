import numpy as np
import re
import datetime

class PartyPopulation:
      def __init__(self, party, population, appeal):
        self.party = party
        self.population = population
        self.appeal = appeal

      def validvariables(self):
          #The key is the name of the attribute. The value describes how the variable is formatted.
          return {"appeal": self.party.name+"."+self.population.name+".appeal"}
      
      def getvariable(self, attr):
          return super(PartyPopulation, self).__getattribute__(attr)
    
      def setvariable(self, attr, variable, operator):
          if operator=="+":
              object.__setattr__(self, attr, super(PartyPopulation, self).__getattribute__(attr)+float(variable))
          elif operator=="-":
              object.__setattr__(self, attr, super(PartyPopulation, self).__getattribute__(attr)-float(variable))
          elif operator=="*":
                object.__setattr__(self, attr, super(PartyPopulation, self).__getattribute__(attr)*float(variable))
          elif operator=="=":
              object.__setattr__(self, attr, float(variable))

def main(scenarioname, parties, populations):
    partypopulations={}
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