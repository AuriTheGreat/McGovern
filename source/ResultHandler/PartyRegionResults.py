from scipy.stats import norm
import matplotlib.pyplot as plt
import statsmodels.api as sm
import numpy as np
import math



class IssuePartyRegionResult:
      def __init__(self, region, party, issue, regionaxes, partyaxes):
        self.region = region
        self.party = party
        self.issue = issue
        self.regionaxes=regionaxes
        self.partyaxes=partyaxes

class PartyRegionResult:
      def __init__(self, region, party, votes=None, seats=None, percentage=None):
        self.region = region
        self.party = party
        self.votes=votes
        self.seats=seats
        self.percentage=percentage

def partyregionissuehandler(scenario):
    x=np.arange(-20, 20, 0.1)

    issuepartyregionresults=[]

    for i in scenario.regionissues:
        for j in scenario.partyissues:
            if i.issue==j.issue:
                regionpopulationinfluence=[x.influence for x in i.region.populations]
                partypopulationappeal=[x.appeal for x in j.party.populations]
                populationinfluence=sum([a*b for a,b in zip(regionpopulationinfluence,partypopulationappeal)])/sum(regionpopulationinfluence)
                localpower=next((x.power for x in scenario.partyregions if x.party == j.party and x.region==i.region), None)

                newissuepartyregionresult=IssuePartyRegionResult(i.region, j.party, i.issue, 
                                                                      [x, norm.pdf(x, i.mean, i.variance)],
                                                                      [x, norm.pdf(x, j.mean, j.variance)])
                newissuepartyregionresult.regionaxes[1]*=i.region.population*i.region.eligiblepopulation/sum(newissuepartyregionresult.regionaxes[1])
                newissuepartyregionresult.partyaxes[1]*=max(0,j.party.power*populationinfluence+localpower)
                issuepartyregionresults.append(newissuepartyregionresult)

    for i in scenario.issues:
        for j in scenario.regions:
            axessum=sum([x.partyaxes[1] for x in issuepartyregionresults if x.issue==i and x.region==j])
            regionissues=[x for x in issuepartyregionresults if x.issue==i and x.region==j]
            importancesum=sum([x.importance for x in scenario.regionissues if x.region==j])
            for k in regionissues:
                k.partyaxes[1]=k.partyaxes[1]/axessum*k.regionaxes[1]*(next((x.importance for x in k.region.issues if x.issue == i), None)/importancesum)

    """
    for i in issuepartyregionresults:
        print(i.region.name, i.party.name, i.issue.name, sum(i.regionaxes[1]), sum(i.partyaxes[1]))
    """

    return issuepartyregionresults


def convertissuepartyregionresults(scenario, issuepartyregionresults):
        partyregionresults=[]
        for i in scenario.regions:
            for j in scenario.parties:
                votes=round(sum([sum(x.partyaxes[1]) for x in issuepartyregionresults if x.region==i and x.party==j]))
                partyregionresults.append(PartyRegionResult(i,j,votes))
        return partyregionresults

def calculationbalancer(partyshares, partyseats, neededseats): #function for distributing seats if the amount of seats doesn't match amount of distributed seats
    while neededseats!=sum(partyseats.values()):
        if neededseats>sum(partyseats.values()):
            maximalvalue,party=0,None
            for i in partyshares:
                 if partyseats[i]==0:
                     value=partyshares[i]
                 else:
                     value=partyshares[i]/partyseats[i]
                 if value>maximalvalue:
                     maximalvalue,party=value,i
            partyseats[party]+=1
            #print(region.name, party.name, "+1")
        else:
            minimalvalue,party=1,None
            for i in partyshares:
                if partyseats[i]>0 and min(partyshares[i]/partyseats[i],partyshares[i])<minimalvalue:
                    minimalvalue,party=min(partyshares[i]/partyseats[i],partyshares[i]),i
            partyseats[party]-=1
            #print(region.name, party.name, "-1")
    return partyseats

def seatcalculation(partyregionresults, partypercentages, region, scenario):
    partyshares={}
    partyseats={}
    for j in partypercentages:
        partyshares[j]=(0.00104*(partypercentages[j]*100)**2.8+0.17)/100
    for j in partyshares:
        partyseats[j]=round((partyshares[j]/sum(partyshares.values()))*region.seats)
    partyseats=calculationbalancer(partyshares, partyseats, region.seats-sum([x.guaranteedseats for x in scenario.partyregions if x.region == region]))
    for j in partyregionresults:
        reachedregion=False
        if j.region==region:
            reachedregion=True
            j.seats=partyseats[j.party]+next((x for x in scenario.partyregions if x.region==j.region and x.party==j.party), None).guaranteedseats
        elif reachedregion:
            break
    return partyseats


def partyregionresulthandler(scenario, issuepartyregionresults=None, mode='normal', partyregionresults=None):
    if issuepartyregionresults:
        partyregionresults=convertissuepartyregionresults(scenario, issuepartyregionresults)

    region=partyregionresults[0].region
    partypercentages={}

    for i in partyregionresults:
        i.percentage=i.votes/sum([x.votes for x in partyregionresults if x.region==i.region])*100
        if i.region!=region:
            seatcalculation(partyregionresults, partypercentages, region, scenario)
            region=i.region
            partypercentages={}
        partypercentages[i.party]=i.percentage/100

    seatcalculation(partyregionresults, partypercentages, region, scenario)

    partyregionresults.sort(key=lambda x: (x.region.seats, x.region.population, x.region.name, x.seats, x.votes), reverse=True)

    return partyregionresults

def main(scenario, mode='normal'):
    issuepartyregionresults=partyregionissuehandler(scenario)
    partyregionresults=partyregionresulthandler(scenario, issuepartyregionresults, mode)
    return partyregionresults