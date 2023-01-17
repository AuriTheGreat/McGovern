import numpy as np
import re
import datetime

class Variable:
      def __init__(self, identifier, value):
        self.identifier = identifier
        self.value = value

      def validvariables(self):
          #The key is the name of the attribute. The value describes how the variable is formatted.
          return {"value": self.identifier}
      
      def getvariable(self, attr):
          return super(Variable, self).__getattribute__(attr)
    
      def setvariable(self, attr, variable, operator):
          if operator=="+":
              object.__setattr__(self, attr, super(Variable, self).__getattribute__(attr)+float(variable))
          elif operator=="-":
              object.__setattr__(self, attr, super(Variable, self).__getattribute__(attr)-float(variable))
          elif operator=="*":
                object.__setattr__(self, attr, super(Variable, self).__getattribute__(attr)*float(variable))
          elif operator=="=":
              object.__setattr__(self, attr, float(variable))

def main(scenarioname):
    variables=[]
    f = open ( 'scenario/' + scenarioname + '/variables.txt' , 'r')
    l = []
    l = np.array([ line.split() for line in f], dtype=object)
    
    identifier=value=None
    
    for i in l:
        newi=" ".join(i).split('#')[0] #Joins all the characters, and then takes all of them until the first hashtag
        if not newi:
            continue
        string1=re.search("(.*)=.*", newi)
        string2=re.search(".*=(.*)", newi)
        if string1 and string2:
            identifier="".join(string1[1].rstrip().lstrip())
            value=float("".join(string2[1].rstrip().lstrip()))
            variables.append(Variable(identifier, value))
            continue

    return variables