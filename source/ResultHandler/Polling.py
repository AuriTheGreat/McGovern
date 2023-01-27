import source.ResultHandler.PartyRegionResults as prr
import source.ResultHandler.TotalPartyResults as tpr
import random
import statsmodels.api as sm

def getnewpoll(gamedata, poll):
    poll.partyregionresults=[]

    #randomizing percentages
    for i in gamedata.results.partyregionresults:
        pollingbias=sum([x.influence/sum([k.influence for k in gamedata.scenario.regionpopulations if x.region==i.region])*y.appeal for x in gamedata.scenario.regionpopulations for y in gamedata.scenario.partypopulations if x.region==i.region and x.population==y.population and i.party==y.party])
        #randomvalue=random.uniform(0.85, 1+pollingbias)
        randomvalue=random.triangular(0.85+pollingbias, 1+pollingbias, 1.15+pollingbias)
        poll.partyregionresults.append(prr.PartyRegionResult(i.region, i.party, i.votes*randomvalue, 0, i.percentage*randomvalue))

    #fixing percentages so they add to 1
    totalpercentage={i.region: sum([j.percentage for j in poll.partyregionresults if i.region==j.region]) for i in poll.partyregionresults}

    for count,i in enumerate(poll.partyregionresults):
        i.percentage=i.percentage/totalpercentage[i.region]*100
        i.votes=round(i.votes/totalpercentage[i.region]*100)

    #getting seat counts for the result
    prr.partyregionresulthandler(gamedata.scenario, mode='polling', partyregionresults=poll.partyregionresults)

    poll.totalpartyresults=tpr.gettotalresults(gamedata.scenario, poll.partyregionresults)

    #poll.print()

    return poll

def aggregatepolls(gamedata, polling):
    #x = np.linspace(1,len([j for i in polling.polls for j in i.partyregionresults]),len([j for i in polling.polls for j in i.partyregionresults]))
    #print([i.totalpartyresults.percentage for i in polling.polls if i.totalpartyresults.party.name=='labour'])

    for count,k in enumerate([i for i in polling.polls[0].partyregionresults]):
        y = [j.votes for i in polling.polls for j in i.partyregionresults if j.party==k.party and j.region==k.region]
        x=range(len(y))
        lowess = sm.nonparametric.lowess(y, x, frac=0.6)

        polling.aggregated.partyregionresults.append(prr.PartyRegionResult(k.region, k.party, max(0,round(lowess[len(y)-1][1])), 0, 0))

        """
        if count==0:
            print(y)
            print(lowess)
            print(lowess[len(y)-1][1])
            plt.plot(x, y, '+')
            plt.plot(lowess[:, 0], lowess[:, 1])
            plt.show()
        """
        
    polling.aggregated.partyregionresults=prr.partyregionresulthandler(gamedata.scenario, mode='polling', partyregionresults=polling.aggregated.partyregionresults)
    polling.aggregated.totalpartyresults=tpr.gettotalresults(gamedata.scenario, polling.aggregated.partyregionresults)

    #polling.aggregated.print()

    return polling.aggregated