import numpy as np
import re
import datetime

class Main:
        def __init__(self, currentdate, turnlength):
            self.currentdate = currentdate
            self.turnlength = turnlength

        def newturn(self):
            self.currentdate+=self.turnlength

        def validvariables(self):
            return {"currentdate": "date"}
        
        def getvariable(self, attr):
            return super(Main, self).__getattribute__(attr)
    
        def setvariable(self, attr, newvalue):
            object.__setattr__(self, attr, newvalue)

def main(scenarioname, base):
    currentdate=base.startdate
    turnlength=(base.enddate-currentdate)/base.turns

    return Main(currentdate, turnlength)