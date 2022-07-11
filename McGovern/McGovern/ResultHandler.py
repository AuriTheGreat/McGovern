from doctest import register_optionflag
from numpy import arange
from scipy.stats import norm
import matplotlib.pyplot as plt

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
                regionvotes=round(sum([sum(i.partyaxes[1]) for i in self.partyregionresults if i.region==region]))
            if round(sum(i.partyaxes[1]))>0:
                print("|", i.party.fullname[0:48].rjust(48), "|", f'{(round(sum(i.partyaxes[1]))):,}'[0:20].center(20), "|",
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
      def __init__(self, region, party, regionaxes, partyaxes, seats=None, percentage=None):
        self.region = region
        self.party = party
        self.regionaxes=regionaxes
        self.partyaxes=partyaxes
        self.seats=seats
        self.percentage=percentage

def issuepartyregiongrouper(scenario):
    x_axis=arange(-20, 20, 0.1)
    issuepartyregionresults=[]
    class IssuePartyRegionResult:
      def __init__(self, region, party, issue, regionaxes, partyaxes):
        self.region = region
        self.party = party
        self.issue = issue
        self.regionaxes=regionaxes
        self.partyaxes=partyaxes

    for i in scenario.regions:
        for j in scenario.parties:
            for regionissue in i.issues:
                partyissue=next((x for x in j.issues if x.issue == regionissue.issue), None)
                issuepartyregionresults.append(
                    IssuePartyRegionResult(
                        i, j, regionissue.issue, 
                        [x_axis, norm.pdf(x_axis, regionissue.mean, regionissue.variance)],
                        [x_axis, norm.pdf(x_axis, partyissue.mean, partyissue.variance)]))


    """
    for i in issuepartyregionresults:
        print(i.issue.name)
        print(i.region.name, i.regionaxes)
        print(i.party.name, i.partyaxes)
    """
                
    return issuepartyregionresults

def partyregionsummation(scenario, issuepartyregionresults):
    importances={}
    partyregionresults={}

    for i in scenario.regions:
        for j in i.issues:
            importances[str(i.name + "-" + j.issue.name)]=(j.importance)/sum([k.importance for k in i.issues])

    for i in issuepartyregionresults:
        if str(i.region.name + '-' + i.party.name) in partyregionresults:
            #print(i.region.name, i.party.name, i.issue.name, partyregionresults[str(i.region.name + '-' + i.party.name)].regionaxes[1])
            partyregionresults[str(i.region.name + '-' + i.party.name)].partyaxes[1]+=i.partyaxes[1]*importances[str(i.region.name + "-" + i.issue.name)]
            partyregionresults[str(i.region.name + '-' + i.party.name)].regionaxes[1]+=i.regionaxes[1]*importances[str(i.region.name + "-" + i.issue.name)]
            #print(i.region.name, i.party.name,  i.issue.name, partyregionresults[str(i.region.name + '-' + i.party.name)].regionaxes[1])
        else:
            partyregionresults[str(i.region.name + '-' + i.party.name)]=PartyRegionResult(
                i.region, i.party, 
                [i.regionaxes[0], i.regionaxes[1]*importances[str(i.region.name + "-" + i.issue.name)]], 
                [i.partyaxes[0], i.partyaxes[1]*importances[str(i.region.name + "-" + i.issue.name)]])

    for i in partyregionresults.values():
        i.regionaxes[1]=i.regionaxes[1]*(i.region.population/sum(i.regionaxes[1]))
        
    """
    for i in partyregionresults.values():
        if i.region.name=='London':
            #plt.plot(i.regionaxes[0], i.regionaxes[1]) 
            plt.plot(i.partyaxes[0], i.partyaxes[1]) 
        #print(i.region.name, round(sum(i.regionaxes[1])))
        #print(i.party.name, i.region.name, round(sum(i.partyaxes[1])))
    plt.show()
    """

    return list(partyregionresults.values())

def partyregiondistributer(scenario, partyregionresults):
    regionsums={}

    for i in partyregionresults:
        regionpopulationinfluence=[x.influence for x in scenario.regionpopulations if x.region==i.region]
        partypopulationappeal=[x.appeal for x in scenario.partypopulations if x.party==i.party]
        populationinfluence=sum([a*b for a,b in zip(regionpopulationinfluence,partypopulationappeal)])/sum(regionpopulationinfluence)
        localpower=next((x.power for x in scenario.partyregions if x.party == i.party and x.region==i.region), None)
        i.partyaxes[1]=i.partyaxes[1]*max(0,i.party.power*populationinfluence+localpower)
        """
        print(i.region.name, regionpopulationinfluence)
        print(i.party.name, partypopulationappeal)
        print(populationinfluence)
        """

    for i in partyregionresults:
        if i.region.name in regionsums:
            regionsums[i.region.name]=regionsums[i.region.name]+i.partyaxes[1]
        else:
            regionsums[i.region.name]=i.partyaxes[1]

    for i in partyregionresults:
        i.partyaxes[1]=i.partyaxes[1]/regionsums[i.region.name]*i.regionaxes[1]

    """
    for i in partyregionresults:
        if i.region.name=='London':
            plt.plot(i.regionaxes[0], i.regionaxes[1]) 
            plt.plot(i.partyaxes[0], i.partyaxes[1]) 
            #print(i.region.name, round(sum(i.regionaxes[1])))
            #print(i.party.name, i.region.name, round(sum(i.partyaxes[1])))
    plt.show()
    """

    partyregionresults.sort(key=lambda x: (x.region.seats, x.region.population, sum(x.partyaxes[1])), reverse=True)


    return partyregionresults

def partyregionseats(scenario, partyregionresults):
    def seatcalculation(partyregionresults, partypercentages, region):
        def calculationbalancer(partyshares, partyseats, region): #function for distributing seats if the amount of seats doesn't match amount of distributed seats
           while region.seats!=sum(partyseats.values()):
               if region.seats>sum(partyseats.values()):
                   maximalvalue,party=0,None
                   for i in partyshares:
                        if min(partyshares[i]/partyseats[i],partyshares[i])>maximalvalue:
                            maximalvalue,party=min(partyshares[i]/partyseats[i],partyshares[i]),i
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
        partyseats=calculationbalancer(partyshares, partyseats, region)
        for j in partyregionresults:
            reachedregion=False
            if j.region==region:
                reachedregion=True
                j.seats=partyseats[j.party]
            elif reachedregion:
                break


    region=partyregionresults[0].region
    partypercentages={}

    for i in partyregionresults:
        i.percentage=(sum(i.partyaxes[1])/sum([sum(j.partyaxes[1]) for j in partyregionresults if i.region==j.region]))*100
        if i.region!=region:
            seatcalculation(partyregionresults, partypercentages, region)
            region=i.region
            partypercentages={}
        partypercentages[i.party]=sum(i.partyaxes[1])/sum(i.regionaxes[1])
    seatcalculation(partyregionresults, partypercentages, region)

    return partyregionresults

def getpartyregionresults(scenario):
    issuepartyregionresults=issuepartyregiongrouper(scenario)
    partyregionresults=partyregionsummation(scenario, issuepartyregionresults)
    partyregionresults=partyregiondistributer(scenario, partyregionresults)
    return partyregionseats(scenario, partyregionresults)

def gettotalresults(scenario, partyregionresults):
    totalpartyresults=[]
    class TotalPartyResult:
          def __init__(self, party, votes, seats, percentage):
            self.party = party
            self.votes=votes
            self.seats=seats
            self.percentage=percentage

    for i in scenario.parties:
        totalpartyresults.append(TotalPartyResult(i, 
        int(round(sum([sum(j.partyaxes[1]) for j in partyregionresults if i==j.party]),0)),
        sum([j.seats for j in partyregionresults if i==j.party]),
        sum([sum(j.partyaxes[1]) for j in partyregionresults if i==j.party])/sum([sum(j.partyaxes[1]) for j in partyregionresults])*100
        ))

    totalpartyresults.sort(key=lambda x: (x.seats, x.votes), reverse=True)
    return totalpartyresults


def main(scenario):
    results=Results(scenario)
    results.partyregionresults=getpartyregionresults(scenario)
    results.totalpartyresults=gettotalresults(scenario, results.partyregionresults)
    results.printresults()
    return results