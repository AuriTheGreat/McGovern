from source.ResultHandler.Classes import TotalPartyResult

def gettotalresults(scenario, partyregionresults):
    totalpartyresults={}
    totalvotes=0

    for i in partyregionresults:
        if i.party not in totalpartyresults:
            totalpartyresults[i.party]=TotalPartyResult(i.party)
        totalpartyresults[i.party].votes+=i.votes
        totalpartyresults[i.party].seats+=i.seats
        totalvotes+=i.votes

    totalpartyresults=list(totalpartyresults.values())
    totalpartyresults.sort(key=lambda x: (x.seats, x.votes), reverse=True)

    for i in totalpartyresults:
        i.percentage=i.votes/totalvotes*100

    return totalpartyresults