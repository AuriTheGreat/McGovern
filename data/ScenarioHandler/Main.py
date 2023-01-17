import os
from data.ScenarioHandler import GetMain, GetBase, GetIssues, GetParties, GetIdeologies, \
GetTraits, GetCharacters, GetRegions, GetPopulations, GetPartyIssues, GetPartyPopulations, \
GetRegionIssues, GetRegionPopulations, GetPartyRegions, GetEvents, GetDecisions, GetTriggers, \
GetVariables
import data.TriggerHandler as TriggerHandler

class Scenario:
      def __init__(self, name, main=None, base=None, issues=None, parties=None, ideologies=None, traits=None, characters=None, outcomes=None, regions=None, populations=None, partyissues=None, partypopulations=None, regionissues=None, regionpopulations=None, partyregions=None, events=None, decisions=None, triggers=None, news=None, variables=None):
        self.name = name
        self.main = main
        self.base = base
        self.issues = issues
        self.parties = parties
        self.ideologies = ideologies
        self.traits = traits
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
        self.news = []
        self.variables = variables

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

    #scenario.printalldata()

    #print(next((x for x in scenario.partyissues if x.party.name == "labour" and x.issue.name== "tariffs"), None).variance)
    #print(next((x for x in scenario.regionissues if x.region.name == "Wales" and x.issue.name== "immigration"), None).variance)

    return scenario