import numpy as np
import re
import datetime

class RegionPopulation:
      def __init__(self, region, population, influence):
        self.region = region
        self.population = population
        self.influence = influence

      def __getattribute__(self, item):
          if item=="influence":
              return max(super(RegionPopulation, self).__getattribute__(item), 0)
          return super(RegionPopulation, self).__getattribute__(item)

      def validvariables(self):
          #The key is the name of the attribute. The value describes how the variable is formatted.
          return {"influence": self.region.name+"."+self.population.name+".influence"}
      
      def getvariable(self, attr):
          return super(RegionPopulation, self).__getattribute__(attr)
    
      def setvariable(self, attr, variable, operator):
          if operator=="+":
              object.__setattr__(self, attr, super(RegionPopulation, self).__getattribute__(attr)+float(variable))
          elif operator=="-":
              object.__setattr__(self, attr, super(RegionPopulation, self).__getattribute__(attr)-float(variable))
          elif operator=="*":
                object.__setattr__(self, attr, super(RegionPopulation, self).__getattribute__(attr)*float(variable))
          elif operator=="=":
              object.__setattr__(self, attr, float(variable))

def main(scenarioname, regions, populations):
    regionpopulations={}
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