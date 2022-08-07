import pyparsing
import operator
import datetime
import re
import random

ops = {"+": (lambda x,y: x+y), 
   "-": (lambda x,y: x-y),
   "*": (lambda x,y: x*y),
   "/": (lambda x,y: x/y),
   "not": (lambda x,y: not y),
   "and": (lambda x,y: x and y),
   "or": (lambda x,y: x or y),
   ">": (lambda x,y: x>y),
   ">=": (lambda x,y: x>=y),
   "<": (lambda x,y: x<y),
   "<=": (lambda x,y: x<=y),
   "==": (lambda x,y: x==y),
   "!=": (lambda x,y: x!=y),
   "**": (lambda x,y: x**y)}

orderofoperations=[['.'], ['**'], ['*','/'], ['+', '-'], ['>', '>=', '<', '<=', '==', '!='], ['not'], ['and'], ['or']]

listofvariables={}

def generatevariables(gamedata):
    listofvariables.update({"date": gamedata.scenario.main.currentdate})
    """
    listofvariables.update({i.party.name+"."+"leader":i.identifier for i in gamedata.scenario.characters if i.leader==True})
    listofvariables.update({i.issue.name+'.'+ i.region.name+"."+"mean":i.mean for i in gamedata.scenario.regionissues})
    listofvariables.update({i.issue.name+'.'+ i.region.name+"."+"variance":i.variance for i in gamedata.scenario.regionissues})
    listofvariables.update({i.issue.name+'.'+ i.region.name+"."+"importance":i.importance for i in gamedata.scenario.regionissues})
    listofvariables.update({i.issue.name+'.'+ i.party.name+"."+"mean":i.mean for i in gamedata.scenario.partyissues})
    listofvariables.update({i.issue.name+'.'+ i.party.name+"."+"variance":i.variance for i in gamedata.scenario.partyissues})
    listofvariables.update({i.population.name+'.'+ i.party.name+"."+"appeal":i.appeal for i in gamedata.scenario.partypopulations})
    listofvariables.update({i.population.name+'.'+ i.region.name+"."+"influence":i.influence for i in gamedata.scenario.regionpopulations})
    """


def variablehandler(gamedata, value, mode='get', variable=None, operator=None):
    #modes: 'get', 'set'
    if value in listofvariables:
        return listofvariables[value]

    if value.count('.')==1:
        string=re.search("(.*)\.", value)
        if string:
            foundstring="".join(string[1].rstrip().lstrip())
            party=next((x for x in gamedata.scenario.parties if x.name == foundstring), None)
            if party:
                string=re.search("\.(.*)", value)
                if string:
                    foundstring="".join(string[1].rstrip().lstrip())
                    if foundstring=="leader":
                        if mode=='get':
                            return party.leader.identifier
                        elif mode=='set':
                            if operator=='=':
                                pass #Write the function to replace party leader
                    if foundstring=="power":
                        if mode=='get':
                            return party.power
                        elif mode=='set':
                            if operator=='=':
                                party.power=float(variable)
                                return None
                            elif operator=='+':
                                party.power+=float(variable)
                                return None
                            elif operator=='-':
                                party.power-=float(variable)
                                return None
                        
    elif value.count('.')==2:
        string=re.search("(.*)\..*\.", value)
        if string:
            foundstring="".join(string[1].rstrip().lstrip())
            issue=next((x for x in gamedata.scenario.issues if x.name == foundstring), None)
            if issue:
                string=re.search("\.(.*)\.", value)
                if string:
                    foundstring="".join(string[1].rstrip().lstrip())
                    region=next((x for x in gamedata.scenario.regions if x.name == foundstring), None)
                    if region:
                        string=re.search("\..*\.(.*)", value)
                        if string:
                            foundstring="".join(string[1].rstrip().lstrip())
                            if foundstring=='mean':
                                if mode=='get':
                                    return next((x for x in gamedata.scenario.regionissues if x.issue == issue and x.region==region), None).mean
                                elif mode=='set':
                                    if operator=='=':
                                        next((x for x in gamedata.scenario.regionissues if x.issue == issue and x.region==region), None).mean=float(variable)
                                        return None
                                    elif operator=='+':
                                        next((x for x in gamedata.scenario.regionissues if x.issue == issue and x.region==region), None).mean+=float(variable)
                                        return None
                                    elif operator=='-':
                                        next((x for x in gamedata.scenario.regionissues if x.issue == issue and x.region==region), None).mean-=float(variable)
                                        return None
                            elif foundstring=='variance':
                                if mode=='get':
                                    return next((x for x in gamedata.scenario.regionissues if x.issue == issue and x.region==region), None).variance
                                elif mode=='set':
                                    if operator=='=':
                                        next((x for x in gamedata.scenario.regionissues if x.issue == issue and x.region==region), None).variance=float(variable)
                                        return None
                                    elif operator=='+':
                                        next((x for x in gamedata.scenario.regionissues if x.issue == issue and x.region==region), None).variance+=float(variable)
                                        return None
                                    elif operator=='-':
                                        next((x for x in gamedata.scenario.regionissues if x.issue == issue and x.region==region), None).variance-=float(variable)
                                        return None
                            elif foundstring=='importance':
                                if mode=='get':
                                    return next((x for x in gamedata.scenario.regionissues if x.issue == issue and x.region==region), None).importance
                                elif mode=='set':
                                    if operator=='=':
                                        next((x for x in gamedata.scenario.regionissues if x.issue == issue and x.region==region), None).importance=float(variable)
                                        return None
                                    elif operator=='+':
                                        next((x for x in gamedata.scenario.regionissues if x.issue == issue and x.region==region), None).importance+=float(variable)
                                        return None
                                    elif operator=='-':
                                        next((x for x in gamedata.scenario.regionissues if x.issue == issue and x.region==region), None).importance-=float(variable)
                                        return None
                    
                    party=next((x for x in gamedata.scenario.parties if x.name == foundstring), None)
                    if party:
                        string=re.search("\..*\.(.*)", value)
                        if string:
                            foundstring="".join(string[1].rstrip().lstrip())
                            if foundstring=='mean':
                                if mode=='get':
                                    return next((x for x in gamedata.scenario.partyissues if x.issue == issue and x.party==party), None).mean
                                elif mode=='set':
                                    if operator=='=':
                                        next((x for x in gamedata.scenario.partyissues if x.issue == issue and x.party==party), None).mean=float(variable)
                                        return None
                                    elif operator=='+':
                                        next((x for x in gamedata.scenario.partyissues if x.issue == issue and x.party==party), None).mean+=float(variable)
                                        return None
                                    elif operator=='-':
                                        next((x for x in gamedata.scenario.partyissues if x.issue == issue and x.party==party), None).mean-=float(variable)
                                        return None
                            elif foundstring=='variance':
                                if mode=='get':
                                    return next((x for x in gamedata.scenario.partyissues if x.issue == issue and x.party==party), None).variance
                                elif mode=='set':
                                    if operator=='=':
                                        next((x for x in gamedata.scenario.partyissues if x.issue == issue and x.party==party), None).variance=float(variable)
                                        return None
                                    elif operator=='+':
                                        next((x for x in gamedata.scenario.partyissues if x.issue == issue and x.party==party), None).variance+=float(variable)
                                        return None
                                    elif operator=='-':
                                        next((x for x in gamedata.scenario.partyissues if x.issue == issue and x.party==party), None).variance-=float(variable)
                                        return None
            population=next((x for x in gamedata.scenario.populations if x.name == foundstring), None)
            if population:
                string=re.search("\.(.*)\.", value)
                if string:
                    foundstring="".join(string[1].rstrip().lstrip())
                    region=next((x for x in gamedata.scenario.regions if x.name == foundstring), None)
                    if region:
                        string=re.search("\..*\.(.*)", value)
                        if string:
                            foundstring="".join(string[1].rstrip().lstrip())
                            if foundstring=='influence':
                                if mode=='get':
                                    return next((x for x in gamedata.scenario.regionpopulations if x.population == population and x.region==region), None).influence
                                elif mode=='set':
                                    if operator=='=':
                                        next((x for x in gamedata.scenario.regionpopulations if x.population == population and x.region==region), None).influence=float(variable)
                                        return None
                                    elif operator=='+':
                                        next((x for x in gamedata.scenario.regionpopulations if x.population == population and x.region==region), None).influence+=float(variable)
                                        return None
                                    elif operator=='-':
                                        next((x for x in gamedata.scenario.regionpopulations if x.population == population and x.region==region), None).influence-=float(variable)
                                        return None
                    party=next((x for x in gamedata.scenario.parties if x.name == foundstring), None)
                    if party:
                        string=re.search("\..*\.(.*)", value)
                        if string:
                            foundstring="".join(string[1].rstrip().lstrip())
                            if foundstring=='appeal':
                                if mode=='get':
                                    return next((x for x in gamedata.scenario.partypopulations if x.population == population and x.party==party), None).appeal
                                elif mode=='set':
                                    if operator=='=':
                                        next((x for x in gamedata.scenario.partypopulations if x.population == population and x.party==party), None).appeal=float(variable)
                                        return None
                                    elif operator=='+':
                                        next((x for x in gamedata.scenario.partypopulations if x.population == population and x.party==party), None).appeal+=float(variable)
                                        return None
                                    elif operator=='-':
                                        next((x for x in gamedata.scenario.partypopulations if x.population == population and x.party==party), None).appeal-=float(variable)
                                        return None

    try:
        return datetime.datetime.strptime(str(value), '"%Y-%m-%d"')
        #print(datetime.datetime.strptime(value, '"%Y-%m-%d"'))
    except ValueError:
        pass

    return value


def calculatequerydeeper(gamedata, parsedtext):
    print("ORDERING ON", parsedtext)
    #Order of Operations 

    for i in orderofoperations:
        while any(item in parsedtext for item in i) and len(parsedtext)>3:
            for count,j in enumerate(parsedtext):
                if j in i:
                    if i[0]=='not':
                        #print(0, parsedtext[count], parsedtext[count+1])
                        parsedtext[count]=[0, parsedtext[count], parsedtext[count+1]]
                        del parsedtext[count+1]
                    elif i[0]=='.':
                        parsedtext[count]=''.join([parsedtext[count-1] + parsedtext[count] + parsedtext[count+1]])
                        del parsedtext[count+1]
                        del parsedtext[count-1]
                    else:
                        #print(parsedtext[count-1], parsedtext[count], parsedtext[count+1])
                        parsedtext[count]=[parsedtext[count-1], parsedtext[count], parsedtext[count+1]]
                        del parsedtext[count+1]
                        del parsedtext[count-1]
    
    
    print("OPERATIONS ON", parsedtext)
    
    #Executing Operations
    value=0
    action=None
    for i in parsedtext:
        if isinstance(i, list):
            answer=calculatequerydeeper(gamedata, i)
            if action==None:
                value=answer
            else:
                print(value, action, answer)
                value=ops[action] (value,answer)
                print(value)
        else:
            if i in ops:
                action=i
            elif i.isnumeric():
                if action==None:
                    value=float(i)
                else:
                    print(value, action, float(i))
                    value=ops[action] (value,float(i))
                    print(value)
            else:
                newvalue=variablehandler(gamedata, i)
                if newvalue!=None:
                    if action==None:
                        value=newvalue
                    else:
                        print(value, action, newvalue)
                        value=ops[action] (value,newvalue)
                        print(value)
            #print(i)
    print(value)
    return value

def checkcondition(gamedata, condition):
    condition=condition.replace('^', '**').replace('&&', ' and ').replace('||', ' or ')
    condition='('+condition+')'

    thecontent = pyparsing.Word(pyparsing.alphanums) | 'not' | 'and' | 'or' | '>=' | '>' | '<=' | '<' | '==' | '!=' | '**' | '+' | '-' | '*' | '/' | '.'
    parens     = pyparsing.nestedExpr( '(', ')', content=thecontent)
    parsedtext=parens.parseString(condition).asList()

    value=calculatequerydeeper(gamedata, parsedtext)

    print(value, parsedtext)

    return value
    

def checktriggers(gamedata):
    triggeredevents=[]

    triggeredtriggers=[i for i in gamedata.scenario.triggers if i.triggerable==True and checkcondition(gamedata, i.condition)==True and random.uniform(0, 1)<=i.chance]
    for i in triggeredtriggers:
        if i.triggeronce==True:
            i.triggerable=False

    [triggeredevents.extend(i.triggered) for i in triggeredtriggers]

    triggeredevents=set(triggeredevents)

    return triggeredevents

def executeeffect(gamedata, effect):
    print(effect)
    operator, value=None, None
    string=re.search(".*\+(.*)", effect)
    if string:
        value="".join(string[1].rstrip().lstrip())
        operator="+"
    string=re.search(".*\-(.*)", effect)
    if string:
        value="".join(string[1].rstrip().lstrip())
        operator="-"
    string=re.search(".*\=(.*)", effect)
    if string:
        value="".join(string[1].rstrip().lstrip())
        operator="="

    string=re.search("(.*)[\+\-\=].*", effect)
    if string:
        variable="".join(string[1].rstrip().lstrip())

    variablehandler(gamedata, variable, "set", value, operator)


def executeevents(gamedata, triggeredevents):
    [executeeffect(gamedata, j) for i in triggeredevents for j in i.effects]

def main(gamedata):
    generatevariables(gamedata)
    triggeredevents=checktriggers(gamedata)
    executeevents(gamedata, triggeredevents)
    print(triggeredevents)