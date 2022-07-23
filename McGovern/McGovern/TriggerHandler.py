import pyparsing
import operator


"""
values={'a':2, 'b':5, 'c':6, 'd':2}

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
       "!=": (lambda x,y: x==y),
       "**": (lambda x,y: x**y)}

operators=[['**'], ['*','/'], ['+', '-'], ['>', '>=', '<', '<=', '==', '!='], ['not'], ['and'], ['or']]


test=' (5 + 4 < 3 && 7 + 3 <= 20 )'
test=test.replace('^', '**').replace('&&', ' and ').replace('||', ' or ')
test='('+test+')'

thecontent = pyparsing.Word(pyparsing.alphanums) | 'not' | 'and' | 'or' | '>=' | '>' | '<=' | '<' | '==' | '!=' | '**' | '+' | '-' | '*' | '/'
parens     = pyparsing.nestedExpr( '(', ')', content=thecontent)

parsedtext=parens.parseString(test).asList()

def godeeper(parsedtext):
    print("ORDERING ON", parsedtext)
    #Order of Operations 
    for i in operators:
        while any(item in parsedtext for item in i) and len(parsedtext)>3:
            for count,j in enumerate(parsedtext):
                if j in i:
                    if i[0]=='not':
                        #print(0, parsedtext[count], parsedtext[count+1])
                        parsedtext[count]=[0, parsedtext[count], parsedtext[count+1]]
                        del parsedtext[count+1]
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
            answer=godeeper(i)
            if action==None:
                value=answer
            else:
                print(value, action, answer)
                value=ops[action] (value,answer)
                print(value)
        else:
            if i in values:
                if action==None:
                    value=values[i]
                else:
                    print(value, action, values[i])
                    value=ops[action] (value,values[i])
                    print(value)
            elif i in ops:
                action=i
            elif type(i) == int or float:
                if action==None:
                    value=float(i)
                else:
                    print(value, action, float(i))
                    value=ops[action] (value,float(i))
                    print(value)
                
            #print(i)
    print(value)
    return value
    
answer=godeeper(parsedtext)
"""