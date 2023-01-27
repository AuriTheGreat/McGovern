
class TotalPartyResult:
    def __init__(self, party, votes, seats, percentage):
        self.party = party
        self.votes=votes
        self.seats=seats
        self.percentage=percentage

def gettotalresults(scenario, partyregionresults):
    totalpartyresults=[]

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