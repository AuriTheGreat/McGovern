import source.ResultHandler.PartyRegionResults as prr
import source.ResultHandler.TotalPartyResults as tpr
import source.ResultHandler.Polling as Polling
from source.ResultHandler.Classes import Results, PollingInfo, Poll
import random

def getresults(scenario):
    results=Results(scenario)
    results.partyregionresults=prr.main(scenario)
    results.totalpartyresults=tpr.gettotalresults(scenario, results.partyregionresults)

    #results.print()
    return results

def makepoll(gamedata):
    poll=Poll(gamedata.scenario, gamedata.scenario.main.currentdate-gamedata.scenario.main.turnlength*random.uniform(0,1)) #randomizes date inbetween interval of previous turn and current one
    poll=Polling.getnewpoll(gamedata, poll)
    return poll

def getpolling(gamedata, polling=None, count=1):
    if polling==None:
        polling=PollingInfo(gamedata.scenario, None, [])

    for i in range(count):
        poll=Poll(gamedata.scenario, gamedata.scenario.main.currentdate-gamedata.scenario.main.turnlength*random.uniform(0,1)) #randomizes date inbetween interval of previous turn and current one
        polling.polls.append(Polling.getnewpoll(gamedata, poll))

    polling.aggregated=Polling.aggregatepolls(gamedata, polling)

    #Sort polls by current winner
    regionsort=[str(i.party.fullname+"-"+i.region.name) for i in polling.aggregated.partyregionresults]
    totalsort=[str(i.party.fullname) for i in polling.aggregated.totalpartyresults]
    
    for i in polling.polls:
        i.partyregionresults=sorted(i.partyregionresults, key=lambda x: regionsort.index(str(x.party.fullname+"-"+x.region.name)))
        i.totalpartyresults=sorted(i.totalpartyresults, key=lambda x: totalsort.index(str(x.party.fullname)))

    return polling

def getelection(gamedata, turns):
    

    return None