from doctest import register_optionflag
from numpy import arange
from matplotlib import pyplot
from scipy.stats import norm
import matplotlib.pyplot as plt


def issueregionresulthandler(scenario): #Function creates normal distributions for each region and party, per each issue
    class IssueRegionResult:
      def __init__(self, issue, regionaxes, partyaxes):
        self.issue = issue
        self.regionaxes = regionaxes
        self.partyaxes = partyaxes

    issuedictionary={}
    regionresults=[]
    issueregionresults=[]
    issue,regionaxes,partyaxes=None,{},{}

    
    # Issue dictionary example with names used instead of objects for demonstrative purposes
    """
    for i in scenario.issues:
        for j in i.parties:
            if i.name in issuedictionary:
                issuedictionary[i.name][j.party.name]=(j.mean, j.variance)

            else:
                issuedictionary[i.name]={}
                issuedictionary[i.name][j.party.name]=(j.mean, j.variance)
        for j in i.regions:
            if i.name in issuedictionary:
                issuedictionary[i.name][j.region.name]=(j.mean, j.variance, j.importance)

            else:
                issuedictionary[i.name]={}
                issuedictionary[i.name][j.region.name]=(j.mean, j.variance, j.importance)
    """

    for i in scenario.issues:
        for j in i.parties:
            if i in issuedictionary:
                issuedictionary[i][j.party]=(j.mean, j.variance)

            else:
                issuedictionary[i]={}
                issuedictionary[i][j.party]=(j.mean, j.variance)
        for j in i.regions:
            if i in issuedictionary:
                issuedictionary[i][j.region]=(j.mean, j.variance, j.importance)

            else:
                issuedictionary[i]={}
                issuedictionary[i][j.region]=(j.mean, j.variance, j.importance)

    x_axis=arange(-10, 10, 0.01)
    for i in issuedictionary:
        issue=i
        for j in issuedictionary[i]:
            if j in scenario.regions:
                region=next((x for x in scenario.regionissues if x.region == j and x.issue==i), None)
                y_axis=norm.pdf(x_axis, region.mean, region.variance)
                y_axis=y_axis*(region.region.population/sum(y_axis))
                regionaxes[region.region]=(x_axis, y_axis)
            elif j in scenario.parties:
                party=next((x for x in scenario.partyissues if x.party == j and x.issue==i), None)
                y_axis=norm.pdf(x_axis, party.mean, party.variance)
                partyaxes[party]=(x_axis, y_axis)
        issueregionresults.append(IssueRegionResult(issue, regionaxes, partyaxes))
    
    return issueregionresults

def regionresulthandler(scenario, issueregionresults): # Changes issueregionresults to be relative, and returns each region result
    class RegionResult:
      def __init__(self, region, regionaxes, partyaxes):
        self.region = region
        self.regionaxes = regionaxes
        self.partyaxes = partyaxes
    
    mainregionresults=[]
    importances={}
    regionresults={}
    partyresults={}
    region=None

    for i in scenario.regions:
        for j in i.issues:
            importances[str(i.name + "-" + j.issue.name)]=(j.importance)/sum([k.importance for k in i.issues])

    for i in issueregionresults:
        for j in i.regionaxes:
            if j in regionresults:
                regionresults[j][1]+=i.regionaxes[j][1]*importances[str(j.name + "-" + i.issue.name)]
            else:
                regionresults[j]=[i.regionaxes[j][0], i.regionaxes[j][1]*importances[str(j.name + "-" + i.issue.name)]]
        for j in i.partyaxes:
            if j.party in partyresults:
                partyresults[j.party][1]+=i.partyaxes[j][1]*(1/len(scenario.issues))
            else:
                partyresults[j.party]=[i.partyaxes[j][0], i.partyaxes[j][1]*(1/len(scenario.issues))]

    for i in regionresults:
        region=i
        mainpartyresults={}
        plt.plot(regionresults[i][0],regionresults[i][1]) 
        regionpartypowersum=0
        for j in partyresults:
            regionpartypowersum+=partyresults[j][1]*j.power
        for j in partyresults:
            newaxis=partyresults[j][1]*j.power/regionpartypowersum*regionresults[i][1]
            plt.plot(partyresults[j][0],newaxis) 
            mainpartyresults[j]=[partyresults[j][0], newaxis]
        mainregionresults.append(RegionResult(region, regionresults[region], mainpartyresults))
        
    for i in mainregionresults:
        print(i.region.name)
        for j in i.partyaxes:
            print(j.fullname + ": " + str(int(round(sum(i.partyaxes[j][1]),0))))
   
    return mainregionresults



def main(scenario):
    issueregionresults=issueregionresulthandler(scenario)
    regionresults=regionresulthandler(scenario,issueregionresults)
