from cmath import e
import os
import re
from source.ScenarioHandler import GetMain, GetBase, GetIssues, GetParties, GetIdeologies, \
GetTraits, GetCharacters, GetRegions, GetPopulations, GetPartyIssues, GetPartyPopulations, \
GetRegionIssues, GetRegionPopulations, GetPartyRegions, GetEvents, GetDecisions, GetTriggers, \
GetVariables
import source.TriggerHandler as TriggerHandler

class Scenario:
      def __init__(self, name):
        self.name = name
        self.main = None
        self.base = None
        self.issues = None
        self.parties = None
        self.ideologies = None
        self.traits = None
        self.characters = None
        self.outcomes = None
        self.regions = None
        self.populations = None
        self.partyissues = None
        self.partypopulations = None
        self.regionissues = None
        self.regionpopulations = None
        self.partyregions = None
        self.events = None
        self.decisions = None
        self.triggers = None
        self.variables = None

        self.news = []
      def print(self):
          def printheader(string):
              print("")
              print("+" + "".join(["-" for c in range(95)]) + "+")
              print("|", string.capitalize().center(93), "|")
              print("+" + "".join(["-" for c in range(95)]) + "+")

          self.base.print()
          printheader("Parties")
          for i in self.parties:
              i.print()
          printheader("Regions")
          for i in self.regions:
              i.print()
          printheader("Characters")
          for i in self.characters:
              i.print()

      def validvariables(self):
          variables={}
          issuenames=[i.name for i in self.issues]
          populationnames=[i.name for i in self.populations]
          variables.update({i+"-"+j:"nationwide."+i+"."+j for i in issuenames for j in ["mean", "variance", "importance"]})
          variables.update({i+"-"+j:"nationwide."+i+"."+j for i in populationnames for j in ["influence"]})
          return variables
         

      def getvariable(self, attr):
          issuename=re.search("(.*)-", attr)[1]
          measurename=re.search("-(.*)", attr)[1]
          return
    
      def setvariable(self, attr, variable, operator):
          issuenames=[i.name for i in self.issues]
          populationnames=[i.name for i in self.populations]

          issuename=re.search("(.*)-", attr)[1]
          measurename=re.search("-(.*)", attr)[1]

          if issuename in issuenames:
            if operator=="+":
                for i in self.regionissues:
                    if i.issue.name==issuename:
                        if measurename=="mean":
                            i.mean+=float(variable)
                        elif measurename=="variance":
                            i.variance+=float(variable)
                        elif measurename=="importance":
                            i.importance+=float(variable)
            elif operator=="-":
                for i in self.regionissues:
                    if i.issue.name==issuename:
                        if measurename=="mean":
                            i.mean-=float(variable)
                        elif measurename=="variance":
                            i.variance-=float(variable)
                        elif measurename=="importance":
                            i.importance-=float(variable)
            elif operator=="*":
                  for i in self.regionissues:
                    if i.issue.name==issuename:
                        if measurename=="mean":
                            i.mean*=float(variable)
                        elif measurename=="variance":
                            i.variance*=float(variable)
                        elif measurename=="importance":
                            i.importance*=float(variable)
            elif operator=="=":
                for i in self.regionissues:
                    if i.issue.name==issuename:
                        if measurename=="mean":
                            i.mean=float(variable)
                        elif measurename=="variance":
                            i.variance=float(variable)
                        elif measurename=="importance":
                            i.importance=float(variable)
          elif issuename in populationnames:
              if operator=="+":
                  for i in self.regionpopulations:
                      if i.population.name==issuename:
                          if measurename=="influence":
                              i.influence+=float(variable)
              elif operator=="-":
                  for i in self.regionpopulations:
                      if i.population.name==issuename:
                          if measurename=="influence":
                              i.influence-=float(variable)
              elif operator=="*":
                  for i in self.regionpopulations:
                      if i.population.name==issuename:
                          if measurename=="influence":
                              i.influence*=float(variable)
              elif operator=="=":
                  for i in self.regionpopulations:
                      if i.population.name==issuename:
                          if measurename=="influence":
                              i.influence=float(variable)
            


def initialisescenario(scenario): #is executed after trigger variable creation
    #Triggering leader ideological effects
    for i in scenario.parties:
        if i.leader:
            for j in i.leader.ideologies:
                for k in j.effects:
                    TriggerHandler.executeeffect(k.replace('party', i.name))
            for j in i.leader.traits:
                for k in j.effects:
                    TriggerHandler.executeeffect(k.replace('party', i.name))

def createmissingfiles(scenarioname):
    files=os.listdir('scenario/'+scenarioname)

    neededfiles=['characters.txt', 'decisions.txt', 'events.txt', 'gfx', 'historicalresults.txt', 'ideologies.txt', 'issues.txt', 'main.txt', 'outcomes.txt', 'parties.txt', 'partyissue.txt', 'partypopulation.txt', 'partyregion.txt', 'populations.txt', 'regionissue.txt', 'regionpopulation.txt', 'regions.txt', 'traits.txt', 'triggers.txt', 'variables.txt']

    for i in neededfiles:
        if i not in files:
            f = open('scenario/'+scenarioname+"/"+i, "w")
            f.close()

def main(scenarioname):
    scenario=Scenario(scenarioname)
    createmissingfiles(scenarioname)
    scenario.base=GetBase.main(scenarioname)
    scenario.main=GetMain.main(scenarioname, scenario.base)
    scenario.parties=GetParties.main(scenarioname)
    scenario.issues=GetIssues.main(scenarioname)
    scenario.populations=GetPopulations.main(scenarioname)
    scenario.ideologies=GetIdeologies.main(scenarioname)
    scenario.traits=GetTraits.main(scenarioname)
    scenario.regions=GetRegions.main(scenarioname, scenario.base)
    scenario.characters=GetCharacters.main(scenarioname,scenario.parties,scenario.ideologies,scenario.traits,scenario.regions)
    scenario.partyissues=GetPartyIssues.main(scenarioname,scenario.parties,scenario.issues)
    scenario.regionissues=GetRegionIssues.main(scenarioname,scenario.regions,scenario.issues)
    scenario.regionpopulations=GetRegionPopulations.main(scenarioname,scenario.regions,scenario.populations)
    scenario.partypopulations=GetPartyPopulations.main(scenarioname,scenario.parties,scenario.populations)
    scenario.partyregions=GetPartyRegions.main(scenarioname, scenario.parties, scenario.regions)
    scenario.events=GetEvents.main(scenarioname)
    scenario.decisions=GetDecisions.main(scenarioname)
    scenario.triggers=GetTriggers.main(scenarioname, scenario.events, scenario.decisions)
    scenario.variables=GetVariables.main(scenarioname)

    #scenario.print()
    return scenario