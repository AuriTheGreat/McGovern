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
    iterablevariableobjects=[gamedata.scenario.parties, gamedata.scenario.regionissues, gamedata.scenario.partyissues, 
                             gamedata.scenario.partypopulations, gamedata.scenario.regionpopulations, gamedata.scenario.partyregions,
                             gamedata.scenario.variables]
    variableobjects=[gamedata.scenario.main]
    #listofvariables.update({"date": currentscenario.main.currentdate})
    for i in variableobjects:
            listofvariables.update({i.validvariables()[k]:((i.getvariable, [k]), (i.setvariable, [k])) for k in i.validvariables()})

    for i in iterablevariableobjects:
        for j in i:
            """
            The variable key is described in the object function, and is used by users to describe variables when writing triggers.
            The variable value is more complicated; the value is a tuple, consisting out of two other tuples - the first used for 
            getting the variable and the second used for setting the variable. Getter and setter tuples are made up of two members - 
            the first one directs to the getting/setting function of the object, and second one are the parameters for the function.
            """
            listofvariables.update({j.validvariables()[k]:((j.getvariable, [k]), (j.setvariable, [k])) for k in j.validvariables()})

    """
    print("####################################################################")
    print(listofvariables.keys())
    print(listofvariables["date"][0][0](*listofvariables["date"][0][1]))
    """


def variablehandler(value, mode='get', variable=None, operator=None):
    #modes: 'get', 'set'
    errorcount=0
    if value in listofvariables:
        if mode=='get':
            return listofvariables[value][0][0](*listofvariables[value][0][1])
        else:
            print(mode, value, operator, variable)
            listofvariables[value][1][0](*listofvariables[value][1][1], variable, operator)
            return None
    else:
        errorcount+=1

    try:
        return datetime.datetime.strptime(str(value), '"%Y-%m-%d"')
        #print(datetime.datetime.strptime(value, '"%Y-%m-%d"'))
    except ValueError:
        errorcount+=1

    if errorcount==2:
        print(mode, value, operator, variable, "NOT FOUND")
    

    return value

def calculatequerydeeper(parsedtext):
    debuggingmode=False

    if debuggingmode==True:
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
    
    if debuggingmode==True:
        print("OPERATIONS ON", parsedtext)
    
    #Executing Operations
    value=0
    action=None
    for i in parsedtext:
        if isinstance(i, list):
            answer=calculatequerydeeper(i)
            if action==None:
                value=answer
            else:
                if debuggingmode==True:
                    print(value, action, answer)
                value=ops[action] (value,answer)
                if debuggingmode==True:
                    print(value)
        else:
            if i in ops:
                action=i
            elif i.isnumeric():
                if action==None:
                    value=float(i)
                else:
                    if debuggingmode==True:
                        print(value, action, float(i))
                    value=ops[action] (value,float(i))
                    if debuggingmode==True:
                        print(value)
            else:
                newvalue=variablehandler(i)
                if newvalue!=None:
                    if action==None:
                        value=newvalue
                    else:
                        if debuggingmode==True:
                            print(value, action, newvalue)
                        value=ops[action] (value,newvalue)
                        if debuggingmode==True:
                            print(value)
            #print(i)
    if debuggingmode==True:
        print(value)
    return value

def checkcondition(condition):
    condition=condition.replace('^', '**').replace('&&', ' and ').replace('||', ' or ')
    condition='('+condition+')'

    thecontent = pyparsing.Word(pyparsing.alphanums) | 'not' | 'and' | 'or' | '>=' | '>' | '<=' | '<' | '==' | '!=' | '**' | '+' | '-' | '*' | '/' | '.'
    parens     = pyparsing.nestedExpr( '(', ')', content=thecontent)
    parsedtext=parens.parseString(condition).asList()

    value=calculatequerydeeper(parsedtext)

    print(value, parsedtext)

    return value
    

def checktriggers():
    triggeredevents=[]

    triggeredtriggers=[i for i in currentscenario.triggers if i.triggerable==True and checkcondition(i.condition)==True and random.uniform(0, 1)<=i.chance]
    for i in triggeredtriggers:
        if i.triggeronce==True:
            i.triggerable=False

    [triggeredevents.extend(i.triggered) for i in triggeredtriggers]

    triggeredevents=set(triggeredevents)

    return triggeredevents

def executeeffect(effect, reverse=False):
    if effect=="":
        return
    operator, value=None, None
    string=re.search(".*\+(.*)", effect)
    if string:
        value="".join(string[1].rstrip().lstrip())
        operator="+"
    string=re.search(".*\-(.*)", effect)
    if string:
        value="".join(string[1].rstrip().lstrip())
        operator="-"
    string=re.search(".*\*(.*)", effect)
    if string:
        value="".join(string[1].rstrip().lstrip())
        operator="*"
    string=re.search(".*\=(.*)", effect)
    if string:
        value="".join(string[1].rstrip().lstrip())
        operator="="

    string=re.search("(.*)[\+\-\*\=].*", effect)
    if string:
        variable="".join(string[1].rstrip().lstrip())

    if reverse: # makes operator the opposite, for example if you want to add to variable, it will remove instead
        if operator=="+":
            variablehandler(variable, "set", value, "-")
        elif operator=="-":
            variablehandler(variable, "set", value, "+")
        else:
            variablehandler(variable, "set", value, operator)
    else:
        variablehandler(variable, "set", value, operator)


def executeevents(triggeredevents):
    [executeeffect(j) for i in triggeredevents for j in i.effects]

def main(scenario):
    class NewsEvent:
        def __init__(self, date, event):
            self.date = date
            self.event = event
    global currentscenario
    currentscenario=scenario
    triggeredevents=checktriggers()
    scenario.news.extend([NewsEvent(scenario.main.currentdate, i) for i in triggeredevents if i.hidden==False])
    executeevents(triggeredevents)
    print(triggeredevents)