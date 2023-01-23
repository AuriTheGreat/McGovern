import numpy as np
import re
import datetime

class RegionIssue:
      def __init__(self, region, issue, mean, variance, importance):
        self.region = region
        self.issue = issue
        self.mean = mean
        self.variance = variance
        self.importance = importance

      def __getattribute__(self, item):
        if item=="mean":
            return min(max(super(RegionIssue, self).__getattribute__(item), -5.0),5.0)
        return super(RegionIssue, self).__getattribute__(item)

      def validvariables(self):
          #The key is the name of the attribute. The value describes how the variable is formatted.
          return {"mean": self.region.name+"."+self.issue.name+".mean",
                  "variance": self.region.name+"."+self.issue.name+".variance",
                  "importance": self.region.name+"."+self.issue.name+".importance"}
      
      def getvariable(self, attr):
          return super(RegionIssue, self).__getattribute__(attr)
    
      def setvariable(self, attr, variable, operator):
          if operator=="+":
              object.__setattr__(self, attr, super(RegionIssue, self).__getattribute__(attr)+float(variable))
          elif operator=="-":
              object.__setattr__(self, attr, super(RegionIssue, self).__getattribute__(attr)-float(variable))
          elif operator=="*":
                object.__setattr__(self, attr, super(RegionIssue, self).__getattribute__(attr)*float(variable))
          elif operator=="=":
              object.__setattr__(self, attr, float(variable))

def main(scenarioname, regions, issues):
    regionissues={}
    f = open ( 'scenario/' + scenarioname + '/regionissue.txt' , 'r')
    l = []
    l = np.array([ line.split() for line in f], dtype=object)

    for i in regions:
        for j in issues:
            regionissues[str(str(i.name)+"-"+str(j.name))]=RegionIssue(i,j,0,1,0)


    regionnames=[x.name for x in regions]
    issuenames=[x.name for x in issues]

    region,issue=None,None

    for i in l:
        newi=" ".join(i).split('#')[0] #Joins all the characters, and then takes all of them until the first hashtag
        if not newi:
            continue
        string=re.search("(.*):", newi)
        if string:
            if string[1] in regionnames:
                region=next((x for x in regions if x.name == string[1]), None)
            elif string[1] in issuenames:
                issue=next((x for x in issues if x.name == string[1]), None)
            else:
                issue=None
        else:
            if issue!=None:
                string=re.search(".*mean.*=(.*)", newi)
                if string:
                    regionissues[str(region.name + "-" + issue.name)].mean=float("".join(string[1].rstrip().lstrip()))
                    continue
                string=re.search(".*variance.*=(.*)", newi)
                if string:
                    regionissues[str(region.name + "-" + issue.name)].variance=float("".join(string[1].rstrip().lstrip()))
                    continue
                string=re.search(".*importance.*=(.*)", newi)
                if string:
                    regionissues[str(region.name + "-" + issue.name)].importance=float("".join(string[1].rstrip().lstrip()))
                    continue

    for i in regions:
        i.issues=[]
        for j in regionissues.values():
            if j.region==i:
                j.issue.regions.append(j)
                i.issues.append(j)

    f = open ( 'scenario/' + scenarioname + '/regionissue.txt' , 'w')
    f.write("### DO NOT WRITE ANY COMMENTS, THEY WILL BE REFRESHED.\n")
    for i in regions:
        f.write(i.name + ":" + "\n")
        for j in i.issues:
            f.write("\t" + j.issue.name + ":" + "\n")
            f.write("\t\t" + "mean=" + str(j.mean) + "\n")
            f.write("\t\t" + "variance=" + str(j.variance) + "\n")
            f.write("\t\t" + "importance=" + str(j.importance) + "\n")

    return list(regionissues.values())