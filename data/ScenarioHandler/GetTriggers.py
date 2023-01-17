import numpy as np
import re
import datetime

class Trigger:
      def __init__(self, identifier, condition, triggered, triggerable, triggeronce, chance):
        self.identifier = identifier
        self.condition = condition
        self.triggered = triggered
        self.triggerable = triggerable
        self.triggeronce = triggeronce
        self.chance = chance

def main(scenarioname, events, decisions):
    triggers=[]
    f = open ( 'scenario/' + scenarioname + '/triggers.txt' , 'r')
    l = []
    l = np.array([ line.split() for line in f], dtype=object)
    
    currenttrigger=None
    condition, triggered, triggerable, triggeronce, chance ="",[], True, True, 0
    conditionreader, triggeredreader=False, False
    
    for i in l:
        newi=" ".join(i).split('#')[0] #Joins all the characters, and then takes all of them until the first hashtag
        if not newi:
            continue
        string=re.search("(.*):", newi)
        if string:
            conditionreader, triggeredreader=False, False
            if string.group(1)=='if':
                conditionreader=True
            elif string.group(1)=='trigger':
                triggeredreader=True
            else:
                if currenttrigger!=None:
                    triggers.append(Trigger(currenttrigger, condition, triggered, triggerable, triggeronce, chance))
                currenttrigger="".join(string[1].rstrip().lstrip())
                condition, triggered, triggerable, triggeronce, chance ="",[], True, True, 0
        else:
            if conditionreader==True:
                string=re.search("(.*)", newi)
                if string:
                    condition+=" " + "".join(string[1].rstrip().lstrip())
            elif triggeredreader==True:
                string=re.search("(.*)", newi)
                #print(currenttrigger)
                if string:
                    string="".join(string[1].rstrip().lstrip())
                    typeoftrigger=re.search("(.*)\.", string)
                    if typeoftrigger:
                        typeoftrigger="".join(typeoftrigger[1].rstrip().lstrip())
                        if typeoftrigger=='event':
                            event=re.search("\.(.*)", string)
                            event="".join(event[1].rstrip().lstrip())
                            triggered.append(next((x for x in events if x.identifier == event), None))
                        elif typeoftrigger=='decision':
                            decision=re.search("\.(.*)", string)
                            decision="".join(decision[1].rstrip().lstrip())
                            triggered.append(next((x for x in decisions if x.identifier == decision), None))

            else:
                string=re.search(".*triggerable.*=(.*)", newi)
                if string:
                    word="".join(string[1].rstrip().lstrip())
                    if word=="True":
                        triggerable=True
                    elif word=="False":
                        triggerable=False
                    continue
                string=re.search(".*triggeronce.*=(.*)", newi)
                if string:
                    word="".join(string[1].rstrip().lstrip())
                    if word=="True":
                        triggeronce=True
                    elif word=="False":
                        triggeronce=False
                    continue
                string=re.search(".*chance.*=(.*)%", newi)
                if string:
                    chance=float("".join(string[1].rstrip().lstrip()))/100
                    continue
    
    triggers.append(Trigger(currenttrigger, condition, triggered, triggerable, triggeronce, chance))

    return np.array(triggers)