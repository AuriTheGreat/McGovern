from doctest import register_optionflag
from numpy import arange
from scipy.stats import norm
import matplotlib.pyplot as plt
import statsmodels.api as sm
import numpy as np
import random
import math
#from datetime import datetime

#####################################################################################
###################################### Results ######################################
#####################################################################################

class Results:
    def __init__(self, scenario, partyregionresults=None, totalpartyresults=None):
        self.scenario=scenario
        self.partyregionresults=partyregionresults
        self.totalpartyresults=totalpartyresults

    def printresults(self):
        print("+" + "".join([chr(0x2015) for c in range(95)]) + "+")
        print("|", "RESULTS".center(93), "|")
        print("+" + "".join([chr(0x2015) for c in range(95)]) + "+")
        print("|", "Party".center(48), "|", "Votes".center(20), "|", "Percentage".center(10), "|", "Seats".center(6), "|")
        
        region=None
        regionvotes=None
        
        for i in self.partyregionresults:
            if i.region!=region:
                print("+" + "".join([chr(0x2015) for c in range(95)]) + "+")
                if region!=None:
                    print("|", "Total".rjust(48), "|", "Votes".center(20), "|", "Percentage".center(10), "|", "Seats".center(6), "|")
                    print("+" + "".join([chr(0x2015) for c in range(95)]) + "+")
                    print("|", "".rjust(48), "|", f'{regionvotes:,}'[0:20].center(20), "|", "100.0%".center(10), "|", str(region.seats).center(6), "|")
                    print("+" + "".join([chr(0x2015) for c in range(95)]) + "+")
                print("|", i.region.name.center(93), "|")
                print("+" + "".join([chr(0x2015) for c in range(95)]) + "+")
                region=i.region
                regionvotes=round(sum([i.votes for i in self.partyregionresults if i.region==region]))
            if i.votes>0 or i.percentage>0:
                print("|", i.party.fullname[0:48].rjust(48), "|", f'{(i.votes):,}'[0:20].center(20), "|",
                      str(str(round(i.percentage,1))+"%")[0:10].center(10), "|", 
                      str(i.seats)[0:6].center(6), "|")
        
        print("+" + "".join([chr(0x2015) for c in range(95)]) + "+")
        print("|", "Total".rjust(48), "|", "Votes".center(20), "|", "Percentage".center(10), "|", "Seats".center(6), "|")
        print("+" + "".join([chr(0x2015) for c in range(95)]) + "+")
        print("|", "".rjust(48), "|", f'{regionvotes:,}'[0:20].center(20), "|", "100.0%".center(10), "|", str(i.region.seats).center(6), "|")
        print("+" + "".join([chr(0x2015) for c in range(95)]) + "+")

        #Total
        print("+" + "".join([chr(0x2015) for c in range(95)]) + "+")
        print("|", "TOTAL".center(93), "|")
        print("+" + "".join([chr(0x2015) for c in range(95)]) + "+")
        print("|", "Party".center(48), "|", "Votes".center(20), "|", "Percentage".center(10), "|", "Seats".center(6), "|")
        print("+" + "".join([chr(0x2015) for c in range(95)]) + "+")

        for i in self.totalpartyresults:
            print("|", i.party.fullname[0:48].rjust(48), "|", f'{(i.votes):,}'[0:20].center(20), "|",
                  str(str(round(i.percentage,1))+"%")[0:10].center(10), "|", 
                  str(i.seats)[0:6].center(6), "|")
        print("+" + "".join([chr(0x2015) for c in range(95)]) + "+")


class PartyRegionResult:
      def __init__(self, region, party, votes=None, seats=None, percentage=None):
        self.region = region
        self.party = party
        self.votes=votes
        self.seats=seats
        self.percentage=percentage

def partyregionissuehandler(scenario):
    x=arange(-20, 20, 0.1)

    issuepartyregionresults=[]

    class IssuePartyRegionResult:
      def __init__(self, region, party, issue, regionaxes, partyaxes):
        self.region = region
        self.party = party
        self.issue = issue
        self.regionaxes=regionaxes
        self.partyaxes=partyaxes

    for i in scenario.regionissues:
        for j in scenario.partyissues:
            if i.issue==j.issue:
                regionpopulationinfluence=[x.influence for x in scenario.regionpopulations if x.region==i.region]
                partypopulationappeal=[x.appeal for x in scenario.partypopulations if x.party==j.party]
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


def partyregionresulthandler(scenario, issuepartyregionresults=None, mode='normal', partyregionresults=None):
    def convertissuepartyregionresults(scenario, issuepartyregionresults):
        partyregionresults=[]
        for i in scenario.regions:
            for j in scenario.parties:
                votes=round(sum([sum(x.partyaxes[1]) for x in issuepartyregionresults if x.region==i and x.party==j]))
                partyregionresults.append(PartyRegionResult(i,j,votes))
        return partyregionresults


    def seatcalculation(partyregionresults, partypercentages, region):
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

    def regionresultcolorcalculation(regions, partyregionresults):
        for i in regions:
            maxvalue, party=-1, None

            #seatweights=[j.seats/i.seats for j in partyregionresults if i==j.region]

            seatweights=[(j.seats/i.seats)**2.5 for j in partyregionresults if i==j.region]
            seatweights=[j/sum(seatweights) for j in seatweights]
            resultcolor=[0,0,0]
            for count, j in enumerate([k for k in partyregionresults if i==k.region]):
                resultcolor=[seatweights[count]*j.party.color[colorcount]+k for colorcount,k in enumerate(resultcolor)]

            #print(seatweights)
            #print(resultcolor)
            i.resultcolor=tuple(resultcolor)

    if issuepartyregionresults:
        partyregionresults=convertissuepartyregionresults(scenario, issuepartyregionresults)

    region=partyregionresults[0].region
    partypercentages={}

    for i in partyregionresults:
        i.percentage=i.votes/sum([x.votes for x in partyregionresults if x.region==i.region])*100
        if i.region!=region:
            seatcalculation(partyregionresults, partypercentages, region)
            region=i.region
            partypercentages={}
        partypercentages[i.party]=i.percentage/100

    seatcalculation(partyregionresults, partypercentages, region)
    if mode=='normal':
        regionresultcolorcalculation(scenario.regions, partyregionresults)

    partyregionresults.sort(key=lambda x: (x.region.seats, x.region.population,  x.seats, x.votes), reverse=True)

    return partyregionresults


def getpartyregionresults(scenario, mode='normal'):
    issuepartyregionresults=partyregionissuehandler(scenario)
    partyregionresults=partyregionresulthandler(scenario, issuepartyregionresults, mode)
    return partyregionresults

def gettotalresults(scenario, partyregionresults):
    totalpartyresults=[]
    class TotalPartyResult:
          def __init__(self, party, votes, seats, percentage):
            self.party = party
            self.votes=votes
            self.seats=seats
            self.percentage=percentage

    for i in scenario.parties:
        if sum([j.votes for j in partyregionresults])*100>0:
            totalpartyresults.append(TotalPartyResult(i, 
            sum([j.votes for j in partyregionresults if i==j.party]),
            sum([j.seats for j in partyregionresults if i==j.party]),
            sum([j.votes for j in partyregionresults if i==j.party])/sum([j.votes for j in partyregionresults])*100
            ))
        else:
            totalpartyresults.append(TotalPartyResult(i, 
            sum([j.votes for j in partyregionresults if i==j.party]),
            sum([j.seats for j in partyregionresults if i==j.party]),
            sum([j.percentage for j in partyregionresults if i==j.party])/sum([j.percentage for j in partyregionresults])*100
            ))

    totalpartyresults.sort(key=lambda x: (x.seats, x.votes), reverse=True)
    return totalpartyresults


def getresults(scenario):
    results=Results(scenario)
    results.partyregionresults=getpartyregionresults(scenario)
    results.totalpartyresults=gettotalresults(scenario, results.partyregionresults)

    #results.printresults()
    return results



#####################################################################################
###################################### Polling ######################################
#####################################################################################

class Polling:
    def __init__(self, scenario, aggregated=None, polls=None):
        self.scenario=scenario
        self.aggregated=aggregated
        self.polls=polls

class Poll(Results):
    def __init__(self, scenario, date, partyregionresults=None, totalpartyresults=None):
        super().__init__(scenario, partyregionresults, totalpartyresults)
        self.date=date


def getnewpoll(gamedata):
    poll=Poll(gamedata.scenario, gamedata.scenario.main.currentdate)
    poll.partyregionresults=[]

    #randomizing percentages
    for i in gamedata.results.partyregionresults:
        pollingbias=sum([x.influence/sum([k.influence for k in gamedata.scenario.regionpopulations if x.region==i.region])*y.appeal for x in gamedata.scenario.regionpopulations for y in gamedata.scenario.partypopulations if x.region==i.region and x.population==y.population and i.party==y.party])
        randomvalue=random.uniform(0.85, 1+pollingbias)
        poll.partyregionresults.append(PartyRegionResult(i.region, i.party, i.votes*randomvalue, 0, i.percentage*randomvalue))

    #fixing percentages so they add to 1
    totalpercentage={i.region: sum([j.percentage for j in poll.partyregionresults if i.region==j.region]) for i in poll.partyregionresults}

    for count,i in enumerate(poll.partyregionresults):
        i.percentage=i.percentage/totalpercentage[i.region]*100
        i.votes=round(i.votes/totalpercentage[i.region]*100)

    #getting seat counts for the result
    partyregionresulthandler(gamedata.scenario, mode='polling', partyregionresults=poll.partyregionresults)

    poll.totalpartyresults=gettotalresults(gamedata.scenario, poll.partyregionresults)

    #poll.printresults()

    return poll

def aggregatepolls(gamedata, polling):
    poll=Poll(gamedata.scenario, gamedata.scenario.main.currentdate)
    poll.partyregionresults=[]

    #x = np.linspace(1,len([j for i in polling.polls for j in i.partyregionresults]),len([j for i in polling.polls for j in i.partyregionresults]))
    #print([i.totalpartyresults.percentage for i in polling.polls if i.totalpartyresults.party.name=='labour'])

    for k in [i for i in polling.polls[0].partyregionresults]:
        y = [j.votes for i in polling.polls for j in i.partyregionresults if j.party==k.party and j.region==k.region]
        x=range(len(y))
        lowess = sm.nonparametric.lowess(y, x, frac=0.6)

        poll.partyregionresults.append(PartyRegionResult(k.region, k.party, round(lowess[len(y)-1][1]), 0, 0))

        """
        print(y)
        print(lowess)
        print(lowess[len(y)-1][1])
        plt.plot(x, y, '+')
        plt.plot(lowess[:, 0], lowess[:, 1])
        plt.show()
        """
    partyregionresulthandler(gamedata.scenario, mode='polling', partyregionresults=poll.partyregionresults)

    poll.totalpartyresults=gettotalresults(gamedata.scenario, poll.partyregionresults)

    #poll.printresults()

    return poll


def getpolling(gamedata, polling=None, count=1):
    if polling==None:
        polling=Polling(gamedata.scenario, None, [])

    for i in range(count):
        polling.polls.append(getnewpoll(gamedata))

    polling.aggregated=aggregatepolls(gamedata, polling)


    #Sort polls by current winner
    regionsort=[str(i.party.fullname+"-"+i.region.name) for i in polling.aggregated.partyregionresults]
    totalsort=[str(i.party.fullname) for i in polling.aggregated.totalpartyresults]
    
    for i in polling.polls:
        i.partyregionresults=sorted(i.partyregionresults, key=lambda x: regionsort.index(str(x.party.fullname+"-"+x.region.name)))
        i.totalpartyresults=sorted(i.totalpartyresults, key=lambda x: totalsort.index(str(x.party.fullname)))


    return polling