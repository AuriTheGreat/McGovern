import numpy as np
import re
import datetime

class PartyIssue:
      def __init__(self, party, issue, mean, variance):
        self.party = party
        self.issue = issue
        self.mean = mean
        self.variance = variance

      def __getattribute__(self, item):
          if item=="mean":
              return min(max(super(PartyIssue, self).__getattribute__(item), -5.0),5.0)
          return super(PartyIssue, self).__getattribute__(item)

      def validvariables(self):
          #The key is the name of the attribute. The value describes how the variable is formatted.
          return {"mean": self.party.name+"."+self.issue.name+".mean",
                  "variance": self.party.name+"."+self.issue.name+".variance"}
      
      def getvariable(self, attr):
          return super(PartyIssue, self).__getattribute__(attr)
    
      def setvariable(self, attr, variable, operator):
          if operator=="+":
              object.__setattr__(self, attr, super(PartyIssue, self).__getattribute__(attr)+float(variable))
          elif operator=="-":
              object.__setattr__(self, attr, super(PartyIssue, self).__getattribute__(attr)-float(variable))
          elif operator=="*":
                object.__setattr__(self, attr, super(PartyIssue, self).__getattribute__(attr)*float(variable))
          elif operator=="=":
              object.__setattr__(self, attr, float(variable))

def main(scenarioname, parties, issues):
    partyissues={}
    f = open ( 'scenario/' + scenarioname + '/partyissue.txt' , 'r')
    l = []
    l = np.array([ line.split() for line in f], dtype=object)

    for i in parties:
        for j in issues:
            partyissues[str(str(i.name)+"-"+str(j.name))]=PartyIssue(i,j,0,1)

    partynames=[x.name for x in parties]
    issuenames=[x.name for x in issues]

    party,issue=None,None

    for i in l:
        newi=" ".join(i).split('#')[0] #Joins all the characters, and then takes all of them until the first hashtag
        if not newi:
            continue
        string=re.search("(.*):", newi)
        if string:
            if string[1] in partynames:
                party=next((x for x in parties if x.name == string[1]), None)
            elif string[1] in issuenames:
                issue=next((x for x in issues if x.name == string[1]), None)
            else:
                issue=None
        else:
            if issue!=None:
                string=re.search(".*mean.*=(.*)", newi)
                if string:
                    partyissues[str(party.name + "-" + issue.name)].mean=float("".join(string[1].rstrip().lstrip()))
                    continue
                string=re.search(".*variance.*=(.*)", newi)
                if string:
                    partyissues[str(party.name + "-" + issue.name)].variance=float("".join(string[1].rstrip().lstrip()))
                    continue

    for i in parties:
        i.issues=[]
        for j in partyissues.values():
            if j.party==i:
                j.issue.parties.append(j)
                i.issues.append(j)

    f = open ( 'scenario/' + scenarioname + '/partyissue.txt' , 'w')
    f.write("### DO NOT WRITE ANY COMMENTS, THEY WILL BE REFRESHED.\n")
    for i in parties:
        f.write(i.name + ":" + "\n")
        for j in i.issues:
            f.write("\t" + j.issue.name + ":" + "\n")
            f.write("\t\t" + "mean=" + str(j.mean) + "\n")
            f.write("\t\t" + "variance=" + str(j.variance) + "\n")
        
    return list(partyissues.values())