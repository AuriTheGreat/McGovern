from doctest import register_optionflag
from numpy import arange
from scipy.stats import norm
import matplotlib.pyplot as plt

class PartyRegionResult:
      def __init__(self, region, party, regionaxes, partyaxes):
        self.region = region
        self.party = party
        self.regionaxes=regionaxes
        self.partyaxes=partyaxes


def printresults(results):
    print("+" + "".join([chr(0x2015) for c in range(95)]) + "+")
    print("|", "RESULTS".center(93), "|")
    print("+" + "".join([chr(0x2015) for c in range(95)]) + "+")
    print("|", "Party".center(48), "|", "Votes".center(20), "|", "Percentage".center(10), "|", "Seats".center(6), "|")
    
    region=None
    regionvotes=None
    
    for i in results:
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
            regionvotes=round(sum([sum(i.partyaxes[1]) for i in results if i.region==region]))
        print("|", i.party.fullname[0:48].rjust(48), "|", f'{(round(sum(i.partyaxes[1]))):,}'[0:20].center(20), "|",
              (str(round(round(sum(i.partyaxes[1]))/sum([sum(i.partyaxes[1]) for i in results if i.region==region])*100,1)) + "%")[0:10].center(10), "|", 
              str(round(sum(i.partyaxes[1])/sum([sum(i.partyaxes[1]) for i in results if i.region==region])*i.region.seats))[0:6].center(6), "|")
    
    print("+" + "".join([chr(0x2015) for c in range(95)]) + "+")
    print("|", "Total".rjust(48), "|", "Votes".center(20), "|", "Percentage".center(10), "|", "Seats".center(6), "|")
    print("+" + "".join([chr(0x2015) for c in range(95)]) + "+")
    print("|", "".rjust(48), "|", f'{regionvotes:,}'[0:20].center(20), "|", "100.0%".center(10), "|", str(i.region.seats).center(6), "|")
    print("+" + "".join([chr(0x2015) for c in range(95)]) + "+")


def issuepartyregiongrouper(scenario):
    x_axis=arange(-10, 10, 0.01)
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
    """

    return list(partyregionresults.values())

def partyregiondistributer(scenario, partyregionresults):
    regionsums={}

    for i in partyregionresults:
        i.partyaxes[1]=i.partyaxes[1]*i.party.power

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
            print(i.region.name, round(sum(i.regionaxes[1])))
            print(i.party.name, i.region.name, round(sum(i.partyaxes[1])))
    """

    partyregionresults.sort(key=lambda x: (x.region.seats, x.region.population, sum(x.partyaxes[1])), reverse=True)

    return partyregionresults


def main(scenario):
    issuepartyregionresults=issuepartyregiongrouper(scenario)
    partyregionresults=partyregionsummation(scenario, issuepartyregionresults)
    return partyregiondistributer(scenario, partyregionresults)