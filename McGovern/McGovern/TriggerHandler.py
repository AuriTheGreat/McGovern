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
                             gamedata.scenario.partypopulations, gamedata.scenario.regionpopulations]
    variableobjects=[gamedata.scenario.main]
    #listofvariables.update({"date": gamedata.scenario.main.currentdate})
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
    print(listofvariables)
    print(listofvariables["date"][0][0](*listofvariables["date"][0][1]))
    """


def variablehandler(gamedata, value, mode='get', variable=None, operator=None):
    #modes: 'get', 'set'
    if value in listofvariables:
        if mode=='get':
            return listofvariables[value][0][0](*listofvariables[value][0][1])
        else:
            listofvariables[value][1][0](*listofvariables[value][1][1], variable, operator)
            return None
    
    try:
        return datetime.datetime.strptime(str(value), '"%Y-%m-%d"')
        #print(datetime.datetime.strptime(value, '"%Y-%m-%d"'))
    except ValueError:
        pass

    return value

def calculatequerydeeper(gamedata, parsedtext):
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
            answer=calculatequerydeeper(gamedata, i)
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
                newvalue=variablehandler(gamedata, i)
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
    if effect=="":
        return
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
    if len(listofvariables)==0:
        generatevariables(gamedata)
    triggeredevents=checktriggers(gamedata)
    executeevents(gamedata, triggeredevents)
    print(triggeredevents)