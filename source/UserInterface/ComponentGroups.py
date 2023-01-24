import math
import source.UserInterface.UIComponents as c #component

def partysharechart(s, x, y, width, height, gamedata, region='National', mode='votes'):
    reachedsize=0
    sizes={}

    if region=='National':
        if mode=='votes':
            sizes={i:i.percentage/100*width for i in gamedata.polling.aggregated.totalpartyresults}
        else:
            sizes={i:i.seats/sum([j.seats for j in gamedata.polling.aggregated.totalpartyresults])*width for i in gamedata.polling.aggregated.totalpartyresults}
    else:
        partyregionresultslist=[j for j in gamedata.polling.aggregated.partyregionresults if j.region.name==region and j.votes>0]
        if mode=='votes':
            sizes={i:i.percentage/100*width for i in partyregionresultslist}
        else:
            sizes={i:i.seats/sum([j.seats for j in partyregionresultslist])*width for i in partyregionresultslist}

    while sum([int(i) for i in sizes.values()])<width:
        maximal=max([i%1 for i in sizes.values()])
        for i in sizes:
            if sizes[i]%1==maximal:
                sizes[i]=math.ceil(sizes[i])
                break

    sizes={i:int(sizes[i]) for i in sizes}


    if region=='National':
        for i in gamedata.polling.aggregated.totalpartyresults:
            c.Rectangle(s, x+reachedsize,y,sizes[i], height, i.party.color)
            reachedsize+=sizes[i]
    else:
        partyregionresultslist=[j for j in gamedata.polling.aggregated.partyregionresults if j.region.name==region and j.votes>0]
        for i in partyregionresultslist:
            size=i.percentage/100*width
            c.Rectangle(s, x+reachedsize,y,sizes[i], height, i.party.color)
            reachedsize+=sizes[i]

    #25%, 50% and 75% markers on vote charts
    c.Rectangle(s, x+width/4,y, width/(360/1), height/(50/5), (255,255,255))
    c.Rectangle(s, x+width/4,y+(height-height/(50/5)), width/(360/1), height/(50/5), (255,255,255))

    c.Rectangle(s, x+width/2,y, width/(360/1), height/(50/5), (255,255,255))
    c.Rectangle(s, x+width/2,y+(height-height/(50/5)), width/(360/1), height/(50/5), (255,255,255))

    c.Rectangle(s, x+width/2+width/4,y, width/(360/1), height/(50/5), (255,255,255))
    c.Rectangle(s, x+width/2+width/4,y+(height-height/(50/5)), width/(360/1), height/(50/5), (255,255,255))

def parliamentarychart(s, x, y, width, height, gamedata, mode='westminster', rulingparties=None, speaker=None, columns=8):
    y+=height/2


    rulingparties=[i for i in gamedata.scenario.parties if i.ruling==True]

    if len(rulingparties)==0:
        maximalseats=max([i.nationalseats for i in gamedata.scenario.parties])
        rulingparties=[i for i in gamedata.scenario.parties if i.nationalseats==maximalseats][0]

    speaker=next((x for x in gamedata.scenario.parties if x.name.lower()=="speaker" and x.nationalseats==1), rulingparties[0])

    if speaker not in rulingparties:
        lengthinseats=max(sum([i.nationalseats for i in gamedata.scenario.parties if i in rulingparties]), sum([i.nationalseats for i in gamedata.scenario.parties if i not in rulingparties])-1)
    else:
        lengthinseats=max(sum([i.nationalseats for i in gamedata.scenario.parties if i in rulingparties]), sum([i.nationalseats for i in gamedata.scenario.parties if i not in rulingparties]))

    radius=min(height/((columns+1.5)*2)/2, (width/(math.ceil((lengthinseats)/columns)+1))/2)

    c.Circle(s, x+radius, y, radius, speaker.color)

    frontrowposition=[x+radius*3, y+radius*3]
    position=[0, 0]

    for i in [j for j in gamedata.scenario.parties if j in rulingparties]:
        for j in range(next((x.nationalseats for x in gamedata.scenario.parties if i == x), None)):
            if i==speaker:
                if j+1==i.nationalseats:
                    continue
            c.Circle(s, frontrowposition[0]+position[0]*(radius*2), frontrowposition[1]+position[1]*(radius*2), radius, i.color)
            position[1]+=1
            #print(frontrowposition[1]+position[1]*10, frontrowposition[0]+position[0]*10)
            if position[1]>columns-1:
                position[0]+=1
                position[1]=0

    frontrowposition=[x+radius*3, y-radius*3]
    position=[0, 0]

    for i in [j for j in gamedata.scenario.parties if j not in rulingparties]:
        for j in range(next((x.nationalseats for x in gamedata.scenario.parties if i == x), None)):
            if i==speaker:
                if j+1==i.nationalseats:
                    continue
            c.Circle(s, frontrowposition[0]+position[0]*(radius*2), frontrowposition[1]-position[1]*(radius*2), radius, i.color)
            position[1]+=1
            #print(frontrowposition[1]+position[1]*10, frontrowposition[0]-position[0]*10)
            if position[1]>columns-1:
                position[0]+=1
                position[1]=0