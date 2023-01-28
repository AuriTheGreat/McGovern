class Results:
    def __init__(self, scenario, partyregionresults=None, totalpartyresults=None):
        self.scenario=scenario
        self.partyregionresults=partyregionresults
        self.totalpartyresults=totalpartyresults

    def print(self):
        print("+" + "".join(["-" for c in range(95)]) + "+")
        print("|", "RESULTS".center(93), "|")
        print("+" + "".join(["-" for c in range(95)]) + "+")
        print("|", "Party".center(48), "|", "Votes".center(20), "|", "Percentage".center(10), "|", "Seats".center(6), "|")
        
        region=None
        regionvotes=None
        
        for i in self.partyregionresults:
            if i.region!=region:
                print("+" + "".join(["-" for c in range(95)]) + "+")
                if region!=None:
                    print("|", "Total".rjust(48), "|", "Votes".center(20), "|", "Percentage".center(10), "|", "Seats".center(6), "|")
                    print("+" + "".join(["-" for c in range(95)]) + "+")
                    print("|", "".rjust(48), "|", f'{regionvotes:,}'[0:20].center(20), "|", "100.0%".center(10), "|", str(region.seats).center(6), "|")
                    print("+" + "".join(["-" for c in range(95)]) + "+")
                print("|", i.region.name.center(93), "|")
                print("+" + "".join(["-" for c in range(95)]) + "+")
                region=i.region
                regionvotes=round(sum([i.votes for i in self.partyregionresults if i.region==region]))
            if i.votes>0 or i.percentage>0:
                print("|", i.party.fullname[0:48].rjust(48), "|", f'{(i.votes):,}'[0:20].center(20), "|",
                      str(str(round(i.percentage,1))+"%")[0:10].center(10), "|", 
                      str(i.seats)[0:6].center(6), "|")
        
        print("+" + "".join(["-" for c in range(95)]) + "+")
        print("|", "Total".rjust(48), "|", "Votes".center(20), "|", "Percentage".center(10), "|", "Seats".center(6), "|")
        print("+" + "".join(["-" for c in range(95)]) + "+")
        print("|", "".rjust(48), "|", f'{regionvotes:,}'[0:20].center(20), "|", "100.0%".center(10), "|", str(i.region.seats).center(6), "|")
        print("+" + "".join(["-" for c in range(95)]) + "+")

        #Total
        print("+" + "".join(["-" for c in range(95)]) + "+")
        print("|", "TOTAL".center(93), "|")
        print("+" + "".join(["-" for c in range(95)]) + "+")
        print("|", "Party".center(48), "|", "Votes".center(20), "|", "Percentage".center(10), "|", "Seats".center(6), "|")
        print("+" + "".join(["-" for c in range(95)]) + "+")

        for i in self.totalpartyresults:
            print("|", i.party.fullname[0:48].rjust(48), "|", f'{(i.votes):,}'[0:20].center(20), "|",
                  str(str(round(i.percentage,1))+"%")[0:10].center(10), "|", 
                  str(i.seats)[0:6].center(6), "|")
        print("+" + "".join(["-" for c in range(95)]) + "+")

class PollingInfo:
    def __init__(self, scenario, aggregated=None, polls=None):
        self.scenario=scenario
        self.aggregated=aggregated
        if polls:
            self.polls=polls
        else:
            self.polls=[]

class Poll(Results):
    def __init__(self, scenario, date, partyregionresults=None, totalpartyresults=None):
        super().__init__(scenario, partyregionresults, totalpartyresults)
        self.date=date


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

class TotalPartyResult:
    def __init__(self, party):
        self.party = party
        self.votes = 0
        self.seats = 0
        self.percentage = 0