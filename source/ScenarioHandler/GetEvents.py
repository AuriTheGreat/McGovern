import numpy as np
import re
import datetime

class Event:
      def __init__(self, identifier, name, hidden, description, effects):
        self.identifier = identifier
        self.name = name
        self.hidden = hidden
        self.description = description
        self.effects = effects

def main(scenarioname):
    events=[]
    f = open ( 'scenario/' + scenarioname + '/events.txt' , 'r')
    l = []
    l = np.array([ line.split() for line in f], dtype=object)
    
    currentevent=None
    name, description, effects, hidden=None,[],[], False
    descriptionreader=effectsreader=False
    
    for i in l:
        newi=" ".join(i).split('#')[0] #Joins all the characters, and then takes all of them until the first hashtag
        if not newi and descriptionreader==False:
            continue
        string=re.search("(.*):", newi)
        if string:
            descriptionreader=effectsreader=False
            if string.group(1)=='description':
                descriptionreader=True
            elif string.group(1)=='effects':
                effectsreader=True
            else:
                if currentevent!=None:
                    events.append(Event(currentevent, name, hidden, description, effects))
                currentevent="".join(string[1].rstrip().lstrip())
                name, description, effects, hidden=None,[],[], False
        else:
            if effectsreader==True:
                string=re.search("(.*)", newi)
                if string:
                    effects.append("".join(string[1].rstrip().lstrip()))
            elif descriptionreader==True:
                string=re.search("(.*)", newi)
                if string:
                    description.append("".join(string[1].rstrip().lstrip()))
                else:
                    description.append("")
            else:
                string=re.search(".*name.*=(.*)", newi)
                if string:
                    name="".join(string[1].rstrip().lstrip())
                    continue
                string=re.search(".*hidden.*=(.*)", newi)
                if string:
                    text="".join(string[1].rstrip().lstrip())
                    if text=="True":
                        hidden=True
                    else:
                        hidden=False
                    continue

    
    events.append(Event(currentevent, name, hidden, description, effects))
     
    return np.array(events)