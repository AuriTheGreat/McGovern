import source.ResultHandler.PartyRegionResults as prr
import source.ResultHandler.TotalPartyResults as tpr
import random
import numpy as np
import statsmodels.api as sm
from source.ResultHandler.Classes import Poll, PartyRegionResult

currentdate=None
regiontotalinfluencesums={}
partypopulationappeals={}
regionpopulationinfluences={}
pollingbiases={}

def getnewpoll(gamedata, poll):
    poll.partyregionresults=[]

    #calculating pollingbias if it's a new turn
    global currentdate
    global regiontotalinfluencesums
    global partypopulationappeals
    global pollingbiases
    if gamedata.scenario.main.currentdate!=currentdate:
        currentdate=gamedata.scenario.main.currentdate
        regiontotalinfluencesums.clear()
        partypopulationappeals.clear()
        regionpopulationinfluences.clear()
        pollingbiases.clear()
        #gets total influence of all populations within region combined and also region population influence multiplied by population polling bias
        for i in gamedata.scenario.regionpopulations:
            if i.region not in regiontotalinfluencesums:
                regiontotalinfluencesums[i.region]=0
                regionpopulationinfluences[i.region]=[]
            regiontotalinfluencesums[i.region]+=i.influence
            regionpopulationinfluences[i.region].append(i.influence)

        for i in gamedata.scenario.partypopulations:
            if i.party not in partypopulationappeals:
                partypopulationappeals[i.party]=[]
            partypopulationappeals[i.party].append(i.appeal*i.population.pollingbias)

        for i in gamedata.results.partyregionresults:
            #calculates pollingbias by:
            #1) Appropriate PartyPopulation and RegionPopulation are found according to partyregionresult
            #2) The relative (in regards to total region influence) influence of population is multiplied to the party's appeal among the population.
            #3) All calculated sums are added up to calculate total party's appeal among populations of the region.
            pollingbiases[i.party.name+"-"+i.region.name]=np.sum(np.array(regionpopulationinfluences[i.region])/regiontotalinfluencesums[i.region]*np.array(partypopulationappeals[i.party]))

    #randomizing percentages
    for i in gamedata.results.partyregionresults:
        pollingbias=pollingbiases[i.party.name+"-"+i.region.name]
        #randomvalue=random.uniform(0.85, 1+pollingbias)
        randomvalue=random.triangular(0.85+pollingbias, 1+pollingbias, 1.15+pollingbias)
        poll.partyregionresults.append(PartyRegionResult(i.region, i.party, i.votes*randomvalue, 0, i.percentage*randomvalue))

    #fixing percentages so they add to 1
    totalpercentage={i.region: sum([j.percentage for j in poll.partyregionresults if i.region==j.region]) for i in poll.partyregionresults}

    for count,i in enumerate(poll.partyregionresults):
        i.percentage=i.percentage/totalpercentage[i.region]*100
        i.votes=round(i.votes/totalpercentage[i.region]*100)

    #getting seat counts for the result
    prr.partyregionresulthandler(gamedata.scenario, partyregionresults=poll.partyregionresults)

    poll.totalpartyresults=tpr.gettotalresults(gamedata.scenario, poll.partyregionresults)

    #poll.print()

    return poll

def aggregatepolls(gamedata, polling):
    #x = np.linspace(1,len([j for i in polling.polls for j in i.partyregionresults]),len([j for i in polling.polls for j in i.partyregionresults]))
    #print([i.totalpartyresults.percentage for i in polling.polls if i.totalpartyresults.party.name=='labour'])

    aggregated=Poll(gamedata.scenario, gamedata.scenario.main.currentdate, [], [])

    #Pretty much turns partyregionresults into a dictionary
    votes={}
    for i in polling.polls[-20:]:
        for j in i.partyregionresults:
            if j.party.name+"-"+j.region.name not in votes:
                votes[j.party.name+"-"+j.region.name]=[]
            votes[j.party.name+"-"+j.region.name].append(j.votes)

    for count,k in enumerate([i for i in polling.polls[0].partyregionresults]):
        y = votes[k.party.name+"-"+k.region.name]
        x=range(len(y))
        lowess = sm.nonparametric.lowess(y, x, frac=0.6)

        aggregated.partyregionresults.append(PartyRegionResult(k.region, k.party, max(0,round(lowess[len(y)-1][1])), 0, 0))

        """
        if count==0:
            print(y)
            print(lowess)
            print(lowess[len(y)-1][1])
            plt.plot(x, y, '+')
            plt.plot(lowess[:, 0], lowess[:, 1])
            plt.show()
        """
        
    aggregated.partyregionresults=prr.partyregionresulthandler(gamedata.scenario, partyregionresults=aggregated.partyregionresults)
    aggregated.totalpartyresults=tpr.gettotalresults(gamedata.scenario, aggregated.partyregionresults)

    #aggregated.print()
    return aggregated