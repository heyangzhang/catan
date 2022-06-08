from classes import *
import math

def almostEqual(d1, d2, epsilon=10**-7):
    return (abs(d2 - d1) < epsilon)

def almostEqualTuple(t1, t2, epsilon = 10**-7):
    return (abs(t2[0] - t1[0]) < epsilon) and (abs(t2[1] - t1[1]) < epsilon)

#settlements&cities
def buildSettlement(event, data):
    player = data.me
    for apex in Tiles.allapex:
        x, y = apex
        if abs(x - event.x) < 10 and abs(y - event.y) < 10\
        and isSettLegal(data, apex) and enoughResource({'wood':1, 'sheep':1, 'clay':1, 'wheat':1}, data):
            if Settlements(apex, player) not in Settlements.every: 
                Settlements(apex, player).create()   
                data.buildSett = False
                spendResources(['wood','sheep','clay','wheat'],data)
                return ("newSettle %d %d\n" %(x, y))
    return ''

def buildCity(event, data):
    player = data.me
    for sett in Settlements.every:
        x, y = sett.getApex()
        if abs(x - event.x) < 10 and abs(y - event.y) < 10:
            if sett.getPlayer() == data.me and enoughResource({'wheat':2, 'stone':3}, data):
                sett.upgrade()
                data.buildCity = False
                spendResources(['wheat','wheat','stone', 'stone','stone'],data)
                return ('newCity %d %d\n' %(x, y))
    return ''

def isSettLegal(data, apex):
    x, y = apex
    for sett in Settlements.every:
        x1, y1 = sett.getApex()
        d = math.sqrt((y1-y)**2 + (x1-x)**2)
        if d<=data.hexSize+5:
            return False

    for road in Road.allroads:
        if road.getPlayer() == data.me:
            if  almostEqualTuple((x,y),road.getPoints()[0]) or  almostEqualTuple((x,y),road.getPoints()[1]):
                return True
    return False

#roads
def buildRoad(event, data):
    for road in Road.allroads:
        x, y = road.getCenter()
        if abs(x - event.x) < 8 and abs(y - event.y) < 8\
        and isRoadLegal(data, x, y) and enoughResource({'wood':1, 'clay':1}, data):
            if road.getPlayer() == None:
                road.addPlayer(data.me)
                data.buildRoad = False
                spendResources(['wood','clay'],data)
                return ("newRoad %d %d\n"%(x,y))
    return ''

def isRoadLegal(data, x, y):
    for road in Road.allroads:
        if road.getCenter() == (x,y):
            pointa, pointb = road.getPoints()

    for road in Road.allroads:
        pointc, pointd = road.getPoints()
        if almostEqualTuple(pointc,pointa) or almostEqualTuple(pointc,pointb) or almostEqualTuple(pointd,pointa) or  almostEqualTuple(pointd,pointb):
            if road.getCenter() != (x,y):
                if road.getPlayer() == data.me:
                    return True

    return False

#starter
def starterRoad(event, data):
    for road in Road.allroads:
        (x, y) = road.getCenter()
        if abs(x - event.x) < 8 and abs(y - event.y) < 8\
        and starterRoadLegal(data, x, y):
            if road.getPlayer() == None:
                road.addPlayer(data.me)
                if data.road1:
                    data.road1 = False
                elif not data.road1:
                    data.road2 = False
                return ("newRoad %d %d\n"%(x,y))
    return ''

def starterRoadLegal(data, x, y):
    for road in Road.allroads:
        if road.getCenter() == (x,y):
            pointa, pointb = road.getPoints()

    for sett in Settlements.every:
        if sett.getPlayer() == data.me:
            if almostEqualTuple(sett.getApex(),pointa) or almostEqualTuple(sett.getApex(), pointb):
                return True

    return False

def starterSettlement(event, data):
    player = data.me
    for apex in Tiles.allapex:
        (x, y) = apex
        if abs(x - event.x) < 10 and abs(y - event.y) < 10\
        and starterSettLegal(data, x,y):
            if Settlements(apex, player) not in Settlements.every: 
                Settlements(apex, player).create()   
                if data.sett1:
                    data.sett1 = False
                elif not data.sett1:
                    data.sett2 = False
                return ("newSettle %d %d\n" %(x, y))
    return ''

def starterSettLegal(data, x, y):
    for sett in Settlements.every:
        x1, y1 = sett.getApex()
        d = math.sqrt((y1-y)**2 + (x1-x)**2)
        if d<=data.hexSize+5:
            return False
    return True


def roadCount():
    count = 0
    for road in Road.allroads:
        if road.getPlayer() != None:
            count += 1
    return count

#resource cards
def startingHand(data):
    lst = ['wood', 'clay', 'stone', 'wheat', 'sheep']
    for kind in lst:
        data.resources.append(Resources(kind))

def drawResources(canvas, data):
    a = 0
    dx = 70
    dy = 50
    x0 = 120
    y0 = data.width + 25
    coords = [(0,0), (1,0), (2,0), (0,1), (1,1)]
    for resource in data.resources:
        x, y = coords[a]
        resource.draw(canvas, x0 + x*dx, y0 + y*dy)
        a += 1

def spendResources(lst,data):
    for cost in lst:
        for resource in data.resources:
            if cost == resource.returnItem():
                resource.spendItem(1)

def recResources(lst, data):
    for cost in lst:
        for resource in data.resources:
            if cost == resource.returnItem():
                resource.getItem(1)



def enoughResource(reDict, data):
    for item in reDict:
        for resource in data.resources:
            if resource.returnItem() == item:
                if resource.returnAmount() < reDict[item]:
                    return False
    return True


#dice
def drawDice(canvas, data):
    data.dice0.draw(canvas, data.width-25, data.height-25)
    data.dice1.draw(canvas, data.width-25, data.height-70)


#Robber

