import math
import os
import threading
import pygame
import sys
import source.ScenarioHandler.Main as ScenarioHandler
import source.ResultHandler.Main as ResultHandler
import source.TriggerHandler as TriggerHandler
import source.UserInterface.UIComponents as c
import source.UserInterface.ComponentGroups as cg

class GameData:
    def __init__(self, scenario, results=None, polling=None):
        self.scenario = scenario
        self.results = results
        self.polling = polling

def mainmenu(s): #s is UIState
    s.objects.clear()
    #c.Rectangle(0,s.screen_width/(1200/250),s.screen_width,s.screen_height-(s.screen_height/(700/250)), '#D4FFFD')
    c.Image(s,0,s.screen_width/(1200/250),s.screen_width,s.screen_height-(s.screen_height/(700/250)), 'resources/gfx/menu.png')

    button_size_x, button_size_y = s.screen_width/(1200/400), s.screen_height/(700/90)
    c.ImageButton(s,s.screen_width/2-(button_size_x/2), s.screen_width/(1200/300), button_size_x, button_size_y, 'resources/gfx/Button.png', 'Play', choosescenario, [s])
    c.ImageButton(s,s.screen_width/2-(button_size_x/2), s.screen_width/(1200/400), button_size_x, button_size_y, 'resources/gfx/Button.png', 'Options', options, [s])
    c.ImageButton(s,s.screen_width/2-(button_size_x/2), s.screen_width/(1200/500), button_size_x, button_size_y, 'resources/gfx/Button.png', 'Quit', quit)
    c.Image(s, 0,s.screen_width/(1200/10), s.screen_width, s.screen_width/4.8, 'resources/gfx/title.png')

    return s


testscenarios=["nice", "indeed", "hello", "good", "fun", "destroy", "life", "great", "alright", "minecraft", "uk1970", "yes",
               "scenario", "betterscenario", "worstscenario", "bestscenario", "indeed", "i like it", "yes"]

def choosescenario(s):
    s.objects.clear()
    button_size_x, button_size_y = s.screen_width/(1200/400), s.screen_height/(700/90)
    tile_size_x, tile_size_y = s.screen_width/(1200/200), s.screen_height/(700/200)
    c.Button(s,s.screen_width/2-(button_size_x/2), s.screen_width/(1200/550), button_size_x, button_size_y, 'Go back', mainmenu, [s])

    objects_per_row=5
    rows=3
    x_outline, y_outline= s.screen_width/(1200/100),s.screen_height/(700/200)
    tile_size_x=(s.screen_width-(objects_per_row*5+x_outline))/objects_per_row
    tile_size_y=(s.screen_height-(objects_per_row*5+y_outline))/objects_per_row

    for count, i in enumerate(s.scenarios):
        c.Button(s, s.screen_width/(1200/(x_outline/2))+(tile_size_x+5)*(count%objects_per_row), s.screen_height/(700/(y_outline/2))+(tile_size_y+5)*math.floor(count/objects_per_row), tile_size_x, tile_size_y, i , choosescenarioplayer, [s, i])

def choosescenarioplayer(s, scenarioname):
    def playerchosen(s, scenarioname, gamedata, party):
        party.player=True
        scenariomain(s, scenarioname, gamedata)

    s.objects.clear()
    gamedata=GameData(ScenarioHandler.main(scenarioname))
    TriggerHandler.generatevariables(gamedata)
    ScenarioHandler.initialisescenario(gamedata.scenario)

    button_size_x, button_size_y = s.screen_width/(1200/400), s.screen_height/(700/90)
    tile_size_x, tile_size_y = s.screen_width/(1200/200), s.screen_height/(700/200)
    c.Button(s, s.screen_width/2-(button_size_x/2), s.screen_width/(1200/550), button_size_x, button_size_y, 'Go back', choosescenario, [s])

    objects_per_row=5
    rows=3
    x_outline, y_outline= s.screen_width/(1200/100),s.screen_height/(700/200)
    tile_size_x=(s.screen_width-(objects_per_row*5+x_outline))/objects_per_row
    tile_size_y=(s.screen_height-(objects_per_row*5+y_outline))/objects_per_row

    for count, i in enumerate([j for j in gamedata.scenario.parties if j.playable==True]):
        c.Button(s, s.screen_width/(1200/(x_outline/2))+(tile_size_x+5)*(count%objects_per_row), s.screen_height/(700/(y_outline/2))+(tile_size_y+5)*math.floor(count/objects_per_row), tile_size_x, tile_size_y, i.name , playerchosen, [s, scenarioname, gamedata, i], color=i.color)



def scenariomain(s, scenarioname, gamedata=None, recalculate=True):
    s.windowhistory.clear()
    s.windowhistory.append([scenariomain, [s, scenarioname, gamedata, False]])
    if recalculate==True:
        gamedata.results=ResultHandler.getresults(gamedata.scenario)
        gamedata.polling=ResultHandler.getpolling(gamedata, gamedata.polling, 5)

    #gamedata.scenario.print()
    #gamedata.results.print()

    s.objects.clear()
    c.Rectangle(s, 900,0,s.screen_width,s.screen_height, '#006699')
    c.Rectangle(s, 0,680,s.screen_width,s.screen_height, '#003366')
    c.Rectangle(s, 0,0,s.screen_width,s.screen_height-(s.screen_height/(700/600)), '#003366')
    c.Rectangle(s, 0,0,s.screen_width,s.screen_height-(s.screen_height/(700/600)), '#003366', str(gamedata.scenario.main.currentdate.date()))
    button_size_x, button_size_y = s.screen_width/(1200/200), s.screen_height/(700/80)
    playedparty=[i.name for i in gamedata.scenario.parties if i.player==True][0]
    if playedparty+'.png' in os.listdir('scenario/' + scenarioname + '/gfx/'):
        c.Image(s, 980,s.screen_width/(1200/110),150,150, 'scenario/' + scenarioname + '/gfx/'+playedparty+'.png')
    else:
        c.Image(s, 980,s.screen_width/(1200/110),150,150, 'scenario/' + scenarioname + '/gfx/main.png')
    c.Button(s, 10, s.screen_width/(1200/10), button_size_x, button_size_y, 'Escape', escape, [s, scenarioname, gamedata])
    if gamedata.scenario.main.currentdate<=gamedata.scenario.base.electiondate<gamedata.scenario.main.currentdate+gamedata.scenario.main.turnlength:
        c.Button(s, 950, s.screen_width/(1200/10), button_size_x, button_size_y, 'Head to Election', electionscreen, [s, scenarioname, gamedata])
    else:
        c.Button(s, 950, s.screen_width/(1200/10), button_size_x, button_size_y, 'Next Turn', nextturn, [s, scenarioname, gamedata])
    c.Button(s, 950, s.screen_width/(1200/280), button_size_x, button_size_y, 'Government', governmentview, [s, scenarioname, gamedata])
    c.Button(s, 950, s.screen_width/(1200/380), button_size_x, button_size_y, 'Regions', regionview, [s, scenarioname, gamedata])
    c.Button(s, 950, s.screen_width/(1200/480), button_size_x, button_size_y, 'Events', eventview, [s, scenarioname, gamedata])
    c.Button(s, 950, s.screen_width/(1200/580), button_size_x, button_size_y, 'Campaign', escape, [s, scenarioname, gamedata])
    c.Button(s, 905, s.screen_width/(1200/280), s.screen_width/(1200/20), s.screen_height/(700/380), '<', addon, [s, scenarioname, gamedata])
    c.Map(s, 0,125,900,555, 'scenario/' + scenarioname + '/gfx/map.png', gamedata, regionview)

    cg.partysharechart(s, 0, 100, 900, 25, gamedata, 'National', 'seats')

    for i in s.openwindows:
        i(s, scenarioname, gamedata, False)
    
def addon(s, scenarioname, gamedata, affectopenwindows=True):
    if affectopenwindows:
        if addon in s.openwindows:
            s.openwindows.remove(addon)
        else:
            s.openwindows.append(addon)
        scenariomain(s, scenarioname, gamedata, False)
    else:
        for count,i in enumerate(gamedata.scenario.regions):
            c.Rectangle(s,650,120+count*60,s.screen_width/(1200/250), s.screen_height/(700/50), '#003366', str(i.name))

def regionview(s,scenarioname, gamedata, region='National', page=0):
    if s.windowhistory[-1][0]!=regionview:
        s.windowhistory.append([regionview, [s, scenarioname, gamedata, region, page]])
    s.objects.clear()
    partiesperpage=5
    regions=['National'] + [i.name for i in gamedata.scenario.regions]
    c.Rectangle(s,0,680,s.screen_width,s.screen_height, '#003366')
    c.Rectangle(s,0,0,s.screen_width,s.screen_height-(s.screen_height/(700/600)), '#003366')
    c.Rectangle(s,350,0,500,s.screen_height-(s.screen_height/(700/600)), '#003366', "Region Information")
    c.Rectangle(s,950,0,300,s.screen_height-(s.screen_height/(700/600)), '#003366', str(gamedata.scenario.main.currentdate.date()))
    button_size_x, button_size_y = s.screen_width/(1200/200), s.screen_height/(700/80)
    c.Button(s, 10, s.screen_width/(1200/10), button_size_x, button_size_y, 'Back', scenariomain, [s, scenarioname, gamedata, False])
    leftlimit=regions.index(region)-1
    if leftlimit<0:
        leftlimit=len(regions)-1
    rightlimit=regions.index(region)+1
    if rightlimit>len(regions)-1:
        rightlimit=0
    c.Button(s,10,120,s.screen_width/(1200/50), s.screen_height/(700/50), '<', regionview, [s, scenarioname, gamedata, regions[leftlimit]])
    c.Rectangle(s,70,120,s.screen_width/(1200/1060), s.screen_height/(700/50), '#003366', region if region=="National" else [i.fullname for i in gamedata.scenario.regions if region==i.name][0])
    c.Button(s,1140,120,s.screen_width/(1200/50), s.screen_height/(700/50), '>', regionview, [s, scenarioname, gamedata, regions[rightlimit]])
    if region=='National':
        partycount=len([j for j in gamedata.polling.aggregated.totalpartyresults if j.votes>0 or j.seats>0])
        for count, i in enumerate([j for j in gamedata.polling.aggregated.totalpartyresults if j.votes>0 or j.seats>0]):
            if page*partiesperpage<=count<(page+1)*partiesperpage:
                c.Button(s,10,180+count%partiesperpage*60,s.screen_width/(1200/350), s.screen_height/(700/50), str(i.party.fullname), partyview, [s, scenarioname, gamedata, i.party.fullname], "#003366")
                c.Rectangle(s,370,180+count%partiesperpage*60,s.screen_width/(1200/100), s.screen_height/(700/50), '#003366', str(round(i.percentage,1)) + "%")
                c.Rectangle(s,480,180+count%partiesperpage*60,s.screen_width/(1200/100), s.screen_height/(700/50), '#003366', str(i.seats))
                c.Rectangle(s,590,180+count%partiesperpage*60,s.screen_width/(1200/380), s.screen_height/(700/50), '#003366', f'{i.votes:,}')
    else:
        partycount=len([j for j in gamedata.polling.aggregated.partyregionresults if j.region.name==region and (j.votes>0 or j.seats>0)])
        for count, i in enumerate([j for j in gamedata.polling.aggregated.partyregionresults if j.region.name==region and (j.votes>0 or j.seats>0)]):
            if page*partiesperpage<=count<(page+1)*partiesperpage:
                c.Button(s,10,180+count%partiesperpage*60,s.screen_width/(1200/350), s.screen_height/(700/50), str(i.party.fullname), partyview, [s, scenarioname, gamedata, i.party.fullname], "#003366")
                c.Rectangle(s,370,180+count%partiesperpage%partycount*60,s.screen_width/(1200/100), s.screen_height/(700/50), '#003366', str(round(i.percentage,1)) + "%")
                c.Rectangle(s,480,180+count%partiesperpage%partycount*60,s.screen_width/(1200/100), s.screen_height/(700/50), '#003366', str(i.seats))
                c.Rectangle(s,590,180+count%partiesperpage%partycount*60,s.screen_width/(1200/380), s.screen_height/(700/50), '#003366', f'{i.votes:,}')

    c.Rectangle(s,990,240,s.screen_width/(1200/200), s.screen_height/(700/250), '#003366')
    c.Button(s, 1000, s.screen_width/(1200/250), s.screen_width/(1200/180), s.screen_height/(700/50), 'General', regionview, [s, scenarioname, gamedata, region])
    c.Button(s, 1000, s.screen_width/(1200/310), s.screen_width/(1200/180), s.screen_height/(700/50), 'Issues', issueview, [s, scenarioname, gamedata, None, region])
    c.Button(s, 1000, s.screen_width/(1200/370), s.screen_width/(1200/180), s.screen_height/(700/50), 'Influence', escape, [s, scenarioname, gamedata])
    c.Button(s, 1000, s.screen_width/(1200/430), s.screen_width/(1200/180), s.screen_height/(700/50), 'Polling', pollingview, [s, scenarioname, gamedata, region])

    cg.partysharechart(s, 10, 480, 960, 50, gamedata, region, 'votes')
    cg.partysharechart(s, 10, 540, 960, 50, gamedata, region, 'seats')
    
    if page!=0:
        c.Button(s,400,600,s.screen_width/(1200/50), s.screen_height/(700/50), '<', regionview, [s, scenarioname, gamedata, region, page-1])
    if partycount>partiesperpage:
        c.Rectangle(s,460,600,s.screen_width/(1200/50), s.screen_height/(700/50), '#003366', str(page+1))
    if partycount>(page+1)*partiesperpage:
        c.Button(s,520,600,s.screen_width/(1200/50), s.screen_height/(700/50), '>', regionview, [s, scenarioname, gamedata, region, page+1])
            
def partyview(s, scenarioname, gamedata, limit=None):
    if s.windowhistory[-1][0]!=partyview:
        s.windowhistory.append([partyview, [s, scenarioname, gamedata, limit]])
    s.objects.clear()
    parties=[i.fullname for i in gamedata.scenario.parties if next((x.votes for x in gamedata.results.totalpartyresults if x.party == i), 0)>0]
    currentparty=next((x for x in gamedata.scenario.parties if x.fullname == limit), None)
    if limit==None:
        limit=parties[0]
    c.Rectangle(s,0,680,s.screen_width,s.screen_height, '#003366')
    c.Rectangle(s,0,0,s.screen_width,s.screen_height-(s.screen_height/(700/600)), '#003366')
    c.Rectangle(s,350,0,500,s.screen_height-(s.screen_height/(700/600)), '#003366', "Party Information")
    c.Rectangle(s,950,0,300,s.screen_height-(s.screen_height/(700/600)), '#003366', str(gamedata.scenario.main.currentdate.date()))
    button_size_x, button_size_y = s.screen_width/(1200/200), s.screen_height/(700/80)
    c.Button(s, 10, s.screen_width/(1200/10), button_size_x, button_size_y, 'Back', scenariomain, [s, scenarioname, gamedata, False])
    if limit in parties:
        leftlimit=parties.index(limit)-1
        if leftlimit<0:
            leftlimit=len(parties)-1
        rightlimit=parties.index(limit)+1
        if rightlimit>len(parties)-1:
            rightlimit=0
    else:
        leftlimit=rightlimit=0
    c.Button(s,10,120,s.screen_width/(1200/50), s.screen_height/(700/50), '<', partyview, [s, scenarioname, gamedata, parties[leftlimit]])
    c.Rectangle(s,70,120,s.screen_width/(1200/1060), s.screen_height/(700/50), '#003366', limit)
    c.Button(s,1140,120,s.screen_width/(1200/50), s.screen_height/(700/50), '>', partyview, [s, scenarioname, gamedata, parties[rightlimit]])
    
    c.Rectangle(s,10,180,s.screen_width/(1200/200), s.screen_height/(700/50), '#003366', "Leader")
    if currentparty.leader==None:
        c.Rectangle(s,220,180,s.screen_width/(1200/350), s.screen_height/(700/50), '#003366', "None")
    else:
        c.Button(s,220,180,s.screen_width/(1200/350), s.screen_height/(700/50), currentparty.leader.name, leaderview, [s, scenarioname, gamedata, currentparty], '#003366' )
    c.Rectangle(s,10,240,s.screen_width/(1200/200), s.screen_height/(700/50), '#003366', "Votes")
    c.Rectangle(s,220,240,s.screen_width/(1200/250), s.screen_height/(700/50), '#003366', f'{next((x for x in gamedata.polling.aggregated.totalpartyresults if x.party == currentparty), None).votes:,}')
    c.Rectangle(s,480,240,s.screen_width/(1200/90), s.screen_height/(700/50), '#003366', str(round(next((x for x in gamedata.polling.aggregated.totalpartyresults if x.party == currentparty), None).percentage,1))+"%")
    c.Rectangle(s,10,300,s.screen_width/(1200/200), s.screen_height/(700/50), '#003366', "Seats")
    biggestregionpercentage, lowestregionpercentage = None,None
    if next((x.votes for x in gamedata.polling.aggregated.totalpartyresults if x.party.fullname == limit), 0):
        biggestregionpercentage, lowestregionpercentage=max([j.percentage for j in gamedata.polling.aggregated.partyregionresults if j.party.fullname==limit]), min([j.percentage for j in gamedata.polling.aggregated.partyregionresults if j.party.fullname==limit and j.percentage>0])
        biggestregion, lowestregion=next((x for x in gamedata.polling.aggregated.partyregionresults if x.party == currentparty and x.percentage==biggestregionpercentage), None).region.fullname, next((x for x in gamedata.polling.aggregated.partyregionresults if x.party == currentparty and x.percentage==lowestregionpercentage), None).region.fullname
    projectedseats=next((x for x in gamedata.polling.aggregated.totalpartyresults if x.party == currentparty), None).seats
    c.Rectangle(s,220,300,s.screen_width/(1200/350), s.screen_height/(700/50), '#003366', str(currentparty.nationalseats) + " (projecting " + str(projectedseats) + ")")
    if biggestregionpercentage!=None:
        c.Rectangle(s,10,360,s.screen_width/(1200/200), s.screen_height/(700/50), '#003366', "Strongest at")
        c.Button(s,220,360,s.screen_width/(1200/350), s.screen_height/(700/50), biggestregion + " (" + str(round(biggestregionpercentage, 1)) + "%)", regionview,
               [s, scenarioname, gamedata, biggestregion if lowestregion=="National" else [i.name for i in gamedata.scenario.regions if biggestregion==i.fullname][0]], '#003366' )
        c.Rectangle(s,10,420,s.screen_width/(1200/200), s.screen_height/(700/50), '#003366', "Weakest at")
        c.Button(s,220,420,s.screen_width/(1200/350), s.screen_height/(700/50), lowestregion + " (" + str(round(lowestregionpercentage, 1)) + "%)", regionview,
               [s, scenarioname, gamedata, lowestregion if lowestregion=="National" else [i.name for i in gamedata.scenario.regions if lowestregion==i.fullname][0]], '#003366' )

        c.Map(s, 600,180,360,500, 'scenario/' + scenarioname + '/gfx/map.png', gamedata, regionview, 'party', currentparty)

        c.Rectangle(s, 990,240,s.screen_width/(1200/200), s.screen_height/(700/250), '#003366')
        c.Button(s, 1000, s.screen_width/(1200/250), s.screen_width/(1200/180), s.screen_height/(700/50), 'General', escape, [s, scenarioname, gamedata])
        c.Button(s, 1000, s.screen_width/(1200/310), s.screen_width/(1200/180), s.screen_height/(700/50), 'Issues', escape, [s, scenarioname, gamedata])
        c.Button(s, 1000, s.screen_width/(1200/370), s.screen_width/(1200/180), s.screen_height/(700/50), 'Influence', escape, [s, scenarioname, gamedata])
        c.Button(s, 1000, s.screen_width/(1200/430), s.screen_width/(1200/180), s.screen_height/(700/50), 'Polling', pollingview, [s, scenarioname, gamedata])

def leaderview(s, scenarioname, gamedata, party):
    s.windowhistory.append([leaderview, [s, scenarioname, gamedata, party]])
    s.objects.clear()
    #leader=next((x for x in gamedata.scenario.characters if x.name == leadername), None)
    c.Rectangle(s,0,680,s.screen_width,s.screen_height, '#003366')
    c.Rectangle(s,0,0,s.screen_width,s.screen_height-(s.screen_height/(700/600)), '#003366')
    c.Rectangle(s,350,0,500,s.screen_height-(s.screen_height/(700/600)), '#003366', "Leader Information")
    c.Rectangle(s,950,0,300,s.screen_height-(s.screen_height/(700/600)), '#003366', str(gamedata.scenario.main.currentdate.date()))
    button_size_x, button_size_y = s.screen_width/(1200/200), s.screen_height/(700/80)
    c.Button(s, 10, s.screen_width/(1200/10), button_size_x, button_size_y, 'Back', partyview, [s,scenarioname, gamedata, party.fullname])

    c.Rectangle(s,10,120,s.screen_width/(1200/1180), s.screen_height/(700/50), '#003366', party.leader.name)
    c.Rectangle(s,10,180,s.screen_width/(1200/250), s.screen_height/(700/50), '#003366', "Ideologies")
    for count, i in enumerate(party.leader.ideologies):
        c.Rectangle(s,10,240+count*60,s.screen_width/(1200/250), s.screen_height/(700/50), '#003366', i.fullname)
    c.Rectangle(s,270,180,s.screen_width/(1200/250), s.screen_height/(700/50), '#003366', "Traits")
    for count, i in enumerate(party.leader.traits):
        c.Rectangle(s,270,240+count*60,s.screen_width/(1200/250), s.screen_height/(700/50), '#003366', i.fullname)
    c.Rectangle(s,10,480,s.screen_width/(1200/250), s.screen_height/(700/50), '#003366', "Home Region")
    c.Rectangle(s,270,480,s.screen_width/(1200/250), s.screen_height/(700/50), '#003366', party.leader.homeregion.fullname)
    c.Rectangle(s,10,540,s.screen_width/(1200/250), s.screen_height/(700/50), '#003366', "Potential Leaders")
    for count, i in enumerate([j for j in party.characters if j!=party.leader]):
        c.Rectangle(s,10+count*190,600,s.screen_width/(1200/180), s.screen_height/(700/50), '#003366', i.name)

    if party.leader.identifier+'.png' in os.listdir('scenario/' + scenarioname + '/gfx/'):
        c.Image(s,890,180,s.screen_width/(1200/300),s.screen_height/(700/350), 'scenario/' + scenarioname + '/gfx/'+party.leader.identifier+'.png')
    else:
        c.Image(s,890,180,s.screen_width/(1200/300),s.screen_height/(700/350), 'scenario/' + scenarioname + '/gfx/nocharacter.png')


def governmentview(s, scenarioname, gamedata):
    s.windowhistory.append([governmentview, [s, scenarioname, gamedata]])
    s.objects.clear()
    c.Rectangle(s,0,680,s.screen_width,s.screen_height, '#003366')
    c.Rectangle(s,0,0,s.screen_width,s.screen_height-(s.screen_height/(700/600)), '#003366')
    c.Rectangle(s,350,0,500,s.screen_height-(s.screen_height/(700/600)), '#003366', "Government Information")
    c.Rectangle(s,950,0,300,s.screen_height-(s.screen_height/(700/600)), '#003366', str(gamedata.scenario.main.currentdate.date()))
    button_size_x, button_size_y = s.screen_width/(1200/200), s.screen_height/(700/80)
    c.Button(s,10, s.screen_width/(1200/10), button_size_x, button_size_y, 'Back', scenariomain, [s, scenarioname, gamedata, False])
    cg.parliamentarychart(s, 10, 100, 1180, 575, gamedata)

def issueview(s, scenarioname, gamedata, issue=None, region=None, page=0):
    if s.windowhistory[-1][0]!=issueview:
        s.windowhistory.append([issueview, [s, scenarioname, gamedata, issue, region, page]])
    s.objects.clear()
    partiesperpage=5
    c.Rectangle(s,0,680,s.screen_width,s.screen_height, '#003366')
    c.Rectangle(s,0,0,s.screen_width,s.screen_height-(s.screen_height/(700/600)), '#003366')
    c.Rectangle(s,350,0,500,s.screen_height-(s.screen_height/(700/600)), '#003366', "Issue Information")
    c.Rectangle(s,950,0,300,s.screen_height-(s.screen_height/(700/600)), '#003366', str(gamedata.scenario.main.currentdate.date()))
    button_size_x, button_size_y = s.screen_width/(1200/200), s.screen_height/(700/80)
    c.Button(s, 10, s.screen_width/(1200/10), button_size_x, button_size_y, 'Back', scenariomain, [s, scenarioname, gamedata, False])
    regions=['National'] + [i.name for i in gamedata.scenario.regions]
    if not region:
        region=regions[0]
    leftregion=regions.index(region)-1
    if leftregion<0:
        leftregion=len(regions)-1
    rightregion=regions.index(region)+1
    if rightregion>len(regions)-1:
        rightregion=0
    c.Button(s,10,120,s.screen_width/(1200/50), s.screen_height/(700/50), '<', issueview, [s, scenarioname, gamedata, issue, regions[leftregion]])
    c.Rectangle(s,70,120,s.screen_width/(1200/1060), s.screen_height/(700/50), '#003366', region if region=="National" else [i.fullname for i in gamedata.scenario.regions if region==i.name][0])
    c.Button(s,1140,120,s.screen_width/(1200/50), s.screen_height/(700/50), '>', issueview, [s, scenarioname, gamedata, issue, regions[rightregion]])
    issues=[i.fullname for i in gamedata.scenario.issues]
    if not issue:
        issue=issues[0]
    leftissue=issues.index(issue)-1
    if leftissue<0:
        leftissue=len(issues)-1
    rightissue=issues.index(issue)+1
    if rightissue>len(issues)-1:
        rightissue=0
    c.Button(s,10,180,s.screen_width/(1200/50), s.screen_height/(700/50), '<', issueview, [s, scenarioname, gamedata, issues[leftissue], region])
    c.Rectangle(s,70,180,s.screen_width/(1200/1060), s.screen_height/(700/50), '#003366', issue)
    c.Button(s,1140,180,s.screen_width/(1200/50), s.screen_height/(700/50), '>', issueview, [s, scenarioname, gamedata, issues[rightissue], region])

    if region=='National':
        partycount=len(gamedata.scenario.parties)
        for count, i in enumerate([j for j in gamedata.scenario.partyissues if issue==j.issue.fullname]):
            if page*partiesperpage<=count<(page+1)*partiesperpage:
                if i.variance>2:
                    division="Divided"
                else:
                    division="United"
                #print(i.party.name, i.issue.name, i.mean, i.variance, division, min(math.floor((i.mean+5)/+(10/len(i.issue.levels))),len(i.issue.levels)-1))
                #print(i.party.name, i.issue.name, i.mean, i.variance, division, i.issue.levels[min(math.floor((i.mean+5)/+(10/len(i.issue.levels))),len(i.issue.levels)-1)])
                c.Button(s,10,240+count%partiesperpage*60,s.screen_width/(1200/350), s.screen_height/(700/50), str(i.party.fullname), partyview, [s, scenarioname, gamedata, i.party.fullname], "#003366")
                c.Rectangle(s,370,240+count%partiesperpage%partycount*60,s.screen_width/(1200/300), s.screen_height/(700/50), '#003366', division)
                c.Rectangle(s,680,240+count%partiesperpage%partycount*60,s.screen_width/(1200/300), s.screen_height/(700/50), '#003366', i.issue.levels[min(math.floor((i.mean+5)/+(10/len(i.issue.levels))),len(i.issue.levels)-1)])
    else:
        partycount=len(gamedata.scenario.parties)
        currentregionissue=next((x for x in gamedata.scenario.regionissues if issue==x.issue.fullname and region==x.region.name), None)
        if currentregionissue.variance>2:
            division="Divided"
        else:
            division="United"
        c.Button(s,10,240,s.screen_width/(1200/350), s.screen_height/(700/50), str(currentregionissue.region.fullname), regionview, [s, scenarioname, gamedata, region], "#003366")
        c.Rectangle(s,370,240,s.screen_width/(1200/300), s.screen_height/(700/50), '#003366', division)
        c.Rectangle(s,680,240,s.screen_width/(1200/300), s.screen_height/(700/50), '#003366', currentregionissue.issue.levels[min(math.floor((currentregionissue.mean+5)/+(10/len(currentregionissue.issue.levels))),len(currentregionissue.issue.levels)-1)])
        for count, i in enumerate([j for j in gamedata.scenario.partyissues if issue==j.issue.fullname]):
            if page*partiesperpage<=count<(page+1)*partiesperpage:
                if i.variance>2:
                    division="Divided"
                else:
                    division="United"
                #print(i.party.name, i.issue.name, i.mean, i.variance, division, min(math.floor((i.mean+5)/+(10/len(i.issue.levels))),len(i.issue.levels)-1))
                #print(i.party.name, i.issue.name, i.mean, i.variance, division, i.issue.levels[min(math.floor((i.mean+5)/+(10/len(i.issue.levels))),len(i.issue.levels)-1)])
                c.Button(s,10,300+count%partiesperpage*60,s.screen_width/(1200/350), s.screen_height/(700/50), str(i.party.fullname), partyview, [s, scenarioname, gamedata, i.party.fullname], "#003366")
                c.Rectangle(s,370,300+count%partiesperpage%partycount*60,s.screen_width/(1200/300), s.screen_height/(700/50), '#003366', division)
                c.Rectangle(s,680,300+count%partiesperpage%partycount*60,s.screen_width/(1200/300), s.screen_height/(700/50), '#003366', i.issue.levels[min(math.floor((i.mean+5)/+(10/len(i.issue.levels))),len(i.issue.levels)-1)])

    c.Rectangle(s, 990,240,s.screen_width/(1200/200), s.screen_height/(700/250), '#003366')
    c.Button(s, 1000, s.screen_width/(1200/250), s.screen_width/(1200/180), s.screen_height/(700/50), 'General', regionview, [s, scenarioname, gamedata, region])
    c.Button(s, 1000, s.screen_width/(1200/310), s.screen_width/(1200/180), s.screen_height/(700/50), 'Issues', issueview, [s, scenarioname, gamedata, None, region])
    c.Button(s, 1000, s.screen_width/(1200/370), s.screen_width/(1200/180), s.screen_height/(700/50), 'Influence', escape, [s, scenarioname, gamedata])
    c.Button(s, 1000, s.screen_width/(1200/430), s.screen_width/(1200/180), s.screen_height/(700/50), 'Polling', pollingview, [s, scenarioname, gamedata, region])

    if page!=0:
        c.Button(s,400,600,s.screen_width/(1200/50), s.screen_height/(700/50), '<', issueview, [s, scenarioname, gamedata, issue, region, page-1])
    if partycount>partiesperpage:
        c.Rectangle(s,460,600,s.screen_width/(1200/50), s.screen_height/(700/50), '#003366', str(page+1))
    if partycount>(page+1)*partiesperpage:
        c.Button(s,520,600,s.screen_width/(1200/50), s.screen_height/(700/50), '>', issueview, [s, scenarioname, gamedata, issue, region, page+1])

def pollingview(s, scenarioname, gamedata, region="National", page=0):
    if s.windowhistory[-1][0]!=pollingview:
        s.windowhistory.append([pollingview, [s, scenarioname, gamedata, region, page]])
    s.objects.clear()
    pollsperpage=7
    regions=['National'] + [i.name for i in gamedata.scenario.regions]
    c.Rectangle(s,0,680,s.screen_width,s.screen_height, '#003366')
    c.Rectangle(s,0,0,s.screen_width,s.screen_height-(s.screen_height/(700/600)), '#003366')
    c.Rectangle(s,350,0,500,s.screen_height-(s.screen_height/(700/600)), '#003366', "Polling")
    c.Rectangle(s,950,0,300,s.screen_height-(s.screen_height/(700/600)), '#003366', str(gamedata.scenario.main.currentdate.date()))
    button_size_x, button_size_y = s.screen_width/(1200/200), s.screen_height/(700/80)
    c.Button(s, 10, s.screen_width/(1200/10), button_size_x, button_size_y, 'Back', scenariomain, [s, scenarioname, gamedata, False])
    leftlimit=regions.index(region)-1
    if leftlimit<0:
        leftlimit=len(regions)-1
    rightlimit=regions.index(region)+1
    if rightlimit>len(regions)-1:
        rightlimit=0
    c.Button(s,10,120,s.screen_width/(1200/50), s.screen_height/(700/50), '<', pollingview, [s, scenarioname, gamedata, regions[leftlimit], 0])
    c.Rectangle(s,70,120,s.screen_width/(1200/1060), s.screen_height/(700/50), '#003366', region if region=="National" else [i.fullname for i in gamedata.scenario.regions if region==i.name][0])
    c.Button(s,1140,120,s.screen_width/(1200/50), s.screen_height/(700/50), '>', pollingview, [s, scenarioname, gamedata, regions[rightlimit], 0])

    pollcount=len(gamedata.polling.polls)

    if region=='National':
        for count, i in enumerate(reversed([j for j in gamedata.polling.polls])):
            if page*pollsperpage<=count<(page+1)*pollsperpage:
                c.Button(s,10,180+count%pollsperpage*60,s.screen_width/(1200/350), s.screen_height/(700/50), str(i.date.strftime('%Y-%m-%d')), pollview, [s, scenarioname, gamedata, i, region], '#003366')
                for partycount, j in enumerate(i.totalpartyresults):
                    if partycount<5:
                        c.Button(s,370+partycount*110,180+count%pollsperpage*60,s.screen_width/(1200/100), s.screen_height/(700/50), str(j.seats), partyview, [s, scenarioname, gamedata, j.party.fullname], "#003366")
    else:
        for count, i in enumerate(reversed([j for j in gamedata.polling.polls])):
            if page*pollsperpage<=count<(page+1)*pollsperpage:
                c.Button(s,10,180+count%pollsperpage*60,s.screen_width/(1200/350), s.screen_height/(700/50), str(i.date.strftime('%Y-%m-%d')), pollview, [s, scenarioname, gamedata, i, region], '#003366')
                for partycount, j in enumerate([k for k in i.partyregionresults if k.region.name==region]):
                    if partycount<5:
                        c.Button(s,370+partycount*110,180+count%pollsperpage*60,s.screen_width/(1200/100), s.screen_height/(700/50), str(j.seats), partyview, [s, scenarioname, gamedata, j.party.fullname], "#003366")


    c.Rectangle(s,990,240,s.screen_width/(1200/200), s.screen_height/(700/250), '#003366')
    c.Button(s, 1000, s.screen_width/(1200/250), s.screen_width/(1200/180), s.screen_height/(700/50), 'General', regionview, [s, scenarioname, gamedata, region])
    c.Button(s, 1000, s.screen_width/(1200/310), s.screen_width/(1200/180), s.screen_height/(700/50), 'Issues', issueview, [s, scenarioname, gamedata])
    c.Button(s, 1000, s.screen_width/(1200/370), s.screen_width/(1200/180), s.screen_height/(700/50), 'Influence', escape, [s, scenarioname, gamedata])
    c.Button(s, 1000, s.screen_width/(1200/430), s.screen_width/(1200/180), s.screen_height/(700/50), 'Polling', pollingview, [s, scenarioname, gamedata, region, 0])

    if page!=0:
        c.Button(s,400,600,s.screen_width/(1200/50), s.screen_height/(700/50), '<', pollingview, [s, scenarioname, gamedata, region, page-1])
    if pollcount>pollsperpage:
        c.Rectangle(s,460,600,s.screen_width/(1200/50), s.screen_height/(700/50), '#003366', str(page+1))
    if pollcount>(page+1)*pollsperpage:
        c.Button(s,520,600,s.screen_width/(1200/50), s.screen_height/(700/50), '>', pollingview, [s, scenarioname, gamedata, region, page+1])

def pollview(s, scenarioname, gamedata, poll, region='National', page=0):
    if s.windowhistory[-1][0]!=pollview:
        s.windowhistory.append([pollview, [s, scenarioname, gamedata, poll, region, page]])
    s.objects.clear()
    partiesperpage=5
    regions=['National'] + [i.name for i in gamedata.scenario.regions]
    c.Rectangle(s,0,680,s.screen_width,s.screen_height, '#003366')
    c.Rectangle(s,0,0,s.screen_width,s.screen_height-(s.screen_height/(700/600)), '#003366')
    c.Rectangle(s,350,0,500,s.screen_height-(s.screen_height/(700/600)), '#003366', "Poll Information")
    c.Rectangle(s,950,0,300,s.screen_height-(s.screen_height/(700/600)), '#003366', str(gamedata.scenario.main.currentdate.date()))
    button_size_x, button_size_y = s.screen_width/(1200/200), s.screen_height/(700/80)
    c.Button(s,10, s.screen_width/(1200/10), button_size_x, button_size_y, 'Back', pollingview, [s, scenarioname, gamedata, region])
    leftlimit=regions.index(region)-1
    if leftlimit<0:
        leftlimit=len(regions)-1
    rightlimit=regions.index(region)+1
    if rightlimit>len(regions)-1:
        rightlimit=0
    c.Button(s,10,120,s.screen_width/(1200/50), s.screen_height/(700/50), '<', pollview, [s, scenarioname, gamedata, poll, regions[leftlimit]])
    c.Rectangle(s,70,120,s.screen_width/(1200/1060), s.screen_height/(700/50), '#003366', region if region=="National" else [i.fullname for i in gamedata.scenario.regions if region==i.name][0])
    c.Button(s,1140,120,s.screen_width/(1200/50), s.screen_height/(700/50), '>', pollview, [s, scenarioname, gamedata, poll, regions[rightlimit]])
    if region=='National':
        partycount=len([j for j in poll.totalpartyresults if j.votes>0 or j.seats>0])
        for count, i in enumerate([j for j in poll.totalpartyresults if j.votes>0 or j.seats>0]):
            if page*partiesperpage<=count<(page+1)*partiesperpage:
                c.Button(s,10,180+count%partiesperpage*60,s.screen_width/(1200/350), s.screen_height/(700/50), str(i.party.fullname), partyview, [s, scenarioname, gamedata, i.party.fullname], "#003366")
                c.Rectangle(s,370,180+count%partiesperpage*60,s.screen_width/(1200/100), s.screen_height/(700/50), '#003366', str(round(i.percentage,1)) + "%")
                c.Rectangle(s,480,180+count%partiesperpage*60,s.screen_width/(1200/100), s.screen_height/(700/50), '#003366', str(i.seats))
                c.Rectangle(s,590,180+count%partiesperpage*60,s.screen_width/(1200/100), s.screen_height/(700/50), '#003366', str(i.seats-next((x for x in gamedata.polling.aggregated.totalpartyresults if x.party == i.party), None).seats))
                c.Rectangle(s,700,180+count%partiesperpage*60,s.screen_width/(1200/100), s.screen_height/(700/50), '#003366', str(round(i.percentage-next((x for x in gamedata.polling.aggregated.totalpartyresults if x.party == i.party), None).percentage,1)) + "%")
    else:
        partycount=len([j for j in poll.partyregionresults if j.region.name==region and (j.votes>0 or j.seats>0)])
        for count, i in enumerate([j for j in poll.partyregionresults if j.region.name==region and (j.votes>0 or j.seats>0)]):
            if page*partiesperpage<=count<(page+1)*partiesperpage:
                c.Button(s,10,180+count%partiesperpage*60,s.screen_width/(1200/350), s.screen_height/(700/50), str(i.party.fullname), partyview, [s, scenarioname, gamedata, i.party.fullname], "#003366")
                c.Rectangle(s,370,180+count%partiesperpage%partycount*60,s.screen_width/(1200/100), s.screen_height/(700/50), '#003366', str(round(i.percentage,1)) + "%")
                c.Rectangle(s,480,180+count%partiesperpage%partycount*60,s.screen_width/(1200/100), s.screen_height/(700/50), '#003366', str(i.seats))
                c.Rectangle(s,590,180+count%partiesperpage*60,s.screen_width/(1200/100), s.screen_height/(700/50), '#003366', str(i.seats-next((x for x in gamedata.polling.aggregated.partyregionresults if x.party == i.party and x.region==i.region), None).seats))
                c.Rectangle(s,700,180+count%partiesperpage*60,s.screen_width/(1200/100), s.screen_height/(700/50), '#003366', str(round(i.percentage-next((x for x in gamedata.polling.aggregated.partyregionresults if x.party == i.party and x.region==i.region), None).percentage,1)) + "%")

    c.Rectangle(s,990,240,s.screen_width/(1200/200), s.screen_height/(700/250), '#003366')
    c.Button(s,1000, s.screen_width/(1200/250), s.screen_width/(1200/180), s.screen_height/(700/50), 'General', regionview, [s, scenarioname, gamedata, region])
    c.Button(s,1000, s.screen_width/(1200/310), s.screen_width/(1200/180), s.screen_height/(700/50), 'Issues', issueview, [s, scenarioname, gamedata, None, region])
    c.Button(s,1000, s.screen_width/(1200/370), s.screen_width/(1200/180), s.screen_height/(700/50), 'Influence', escape, [s, scenarioname, gamedata])
    c.Button(s,1000, s.screen_width/(1200/430), s.screen_width/(1200/180), s.screen_height/(700/50), 'Polling', pollingview, [s, scenarioname, gamedata, region])

    cg.partysharechart(s, 10, 480, 960, 50, gamedata, region, 'votes')
    cg.partysharechart(s, 10, 540, 960, 50, gamedata, region, 'seats')
    
    if page!=0:
        c.Button(s,400,600,s.screen_width/(1200/50), s.screen_height/(700/50), '<', pollview, [s, scenarioname, gamedata, poll, region, page-1])
    if partycount>partiesperpage:
        c.Rectangle(s,460,600,s.screen_width/(1200/50), s.screen_height/(700/50), '#003366', str(page+1))
    if partycount>(page+1)*partiesperpage:
        c.Button(s,520,600,s.screen_width/(1200/50), s.screen_height/(700/50), '>', pollview, [s, scenarioname, gamedata, poll, region, page+1])

def eventview(s, scenarioname, gamedata, currentevent=None):
    s.windowhistory.append([eventview, [s, scenarioname, gamedata, currentevent]])
    s.objects.clear()
    c.Rectangle(s,0,680,s.screen_width,s.screen_height, '#003366')
    c.Rectangle(s,0,0,s.screen_width,s.screen_height-(s.screen_height/(700/600)), '#003366')
    c.Rectangle(s,350,0,500,s.screen_height-(s.screen_height/(700/600)), '#003366', "Events' View")
    c.Rectangle(s,950,0,300,s.screen_height-(s.screen_height/(700/600)), '#003366', str(gamedata.scenario.main.currentdate.date()))
    button_size_x, button_size_y = s.screen_width/(1200/200), s.screen_height/(700/80)
    c.Button(s, 10, s.screen_width/(1200/10), button_size_x, button_size_y, 'Back', scenariomain, [s, scenarioname, gamedata, False])

    c.Rectangle(s, 10, 110, s.screen_width/(1200/190), s.screen_width/(1200/565), '#003366')
    if not gamedata.scenario.news:
        c.Rectangle(s, 15, 115, s.screen_width/(1200/180), s.screen_width/(1200/80), '#250045', "No events so far")
    else:
        for count, i in enumerate(reversed(gamedata.scenario.news)):
            c.Button(s, 15, 115+count*90, s.screen_width/(1200/180), s.screen_width/(1200/80), i.event.name, eventview, [s, scenarioname, gamedata, i.event])

    if currentevent==None:
        pass
    else:
        c.MultipleLineText(s, 210, 110, 580, 565, '#003366', currentevent.description, fontsize=30)

def electionscreen(s, scenarioname, gamedata):
    s.windowhistory.append([electionscreen, [s, scenarioname, gamedata]])
    s.objects.clear()
    c.Rectangle(s,0,680,s.screen_width,s.screen_height, '#003366')
    c.Rectangle(s,0,0,s.screen_width,s.screen_height-(s.screen_height/(700/600)), '#003366')
    c.Rectangle(s,350,0,500,s.screen_height-(s.screen_height/(700/600)), '#003366', "Election Day")
    c.Rectangle(s,950,0,300,s.screen_height-(s.screen_height/(700/600)), '#003366', str(gamedata.scenario.base.electiondate.date()))
    button_size_x, button_size_y = s.screen_width/(1200/200), s.screen_height/(700/80)
    c.Button(s, 10, s.screen_width/(1200/10), button_size_x, button_size_y, 'Back', scenariomain, [s, scenarioname, gamedata, False])

    ResultHandler.getelection(gamedata, 5)

def nextturn(s, scenarioname, gamedata):
    def processturn(s, scenarioname, gamedata):
        s.calculating=True
        gamedata.results=ResultHandler.getresults(gamedata.scenario)
        gamedata.polling=ResultHandler.getpolling(gamedata, gamedata.polling, 5)
        s.calculating=False
        s.windowhistory[-1][0](*s.windowhistory[-1][1])
        #scenariomain(scenarioname, gamedata, recalculate=False)

    if not s.calculating:
        if gamedata.scenario.base.enddate>gamedata.scenario.main.currentdate:
            gamedata.scenario.main.newturn()
            TriggerHandler.main(gamedata.scenario)
            if gamedata.scenario.main.currentdate<=gamedata.scenario.base.electiondate<gamedata.scenario.main.currentdate+gamedata.scenario.main.turnlength:
                print(gamedata.scenario.main.currentdate.date(), "ELECTION DAY")
            else:
                print(gamedata.scenario.main.currentdate.date())

        c.LoadingScreenImage(s, 225,90,5,(255,255,255))

        threading.Thread(target=processturn,
                             args=[s, scenarioname,gamedata],
                             daemon=True).start()


def escape(s, scenarioname, gamedata):
    s.objects.clear()
    button_size_x, button_size_y = s.screen_width/(1200/400), s.screen_height/(700/90)
    c.ImageButton(s, s.screen_width/2-(button_size_x/2), s.screen_width/(1200/300), button_size_x, button_size_y, 'resources/gfx/Button.png', 'Return to the game', scenariomain, [s, scenarioname, gamedata, False])
    c.ImageButton(s, s.screen_width/2-(button_size_x/2), s.screen_width/(1200/400), button_size_x, button_size_y, 'resources/gfx/Button.png', 'Main menu', mainmenu, [s])
    c.ImageButton(s, s.screen_width/2-(button_size_x/2), s.screen_width/(1200/500), button_size_x, button_size_y, 'resources/gfx/Button.png', 'Quit', quit)

def options(s):
    s.objects.clear()
    c.Button(s, s.screen_width/2-200, 130, 400, 100, 'Go back', mainmenu, [s])

def quit():
    pygame.quit()
    sys.exit()