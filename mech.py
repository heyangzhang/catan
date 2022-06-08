from classes import *
from pieces import *

def almostEqualTuple(t1, t2, epsilon = 10**-7):
    return (abs(t2[0] - t1[0]) < epsilon) and (abs(t2[1] - t1[1]) < epsilon)

def nextTurn(data, direction = 1, player = None):
    data.turn = (direction+data.turn)%4
    data.rolled = True
    if player == 'orange':
        if data.setup2:
            print('a')
            data.setup2 = False
            data.ready = False
            data.waiting = False
            data.rolled = True
        if data.setup1:
            print('b')
            data.setup1 = False
            data.setup2 = True
    return 'nextTurn %s\n' %direction

def callNextTurn(event, data):
    if 5<event.x <75 and data.width+5<event.y<data.width+45:
        return nextTurn(data, 1, data.me)
    return ''

def startGame(event, data):
    if 5<event.x <75 and data.width+5<event.y<data.width+45:
        data.start = True
        data.setup1 = True
        return 'started setup1\n'
    return ''

def rollDice(event, data):
    if 5<event.x <75 and data.width+50<event.y<data.width+90:
        data.dice0.roll(data.me)
        data.dice1.roll(data.me)
        getResource(data)
        data.rolled = False
        return 'rolled %d %d\n' %(data.dice0.getNumber(), data.dice1.getNumber())
    return ''

def getResource(data):
    for tile in Tiles.store:
        if tile.getNumber() == (data.dice0.getNumber() + data.dice1.getNumber()):
            print('pass1')
            for apex in tile.getApex():
                for sett in Settlements.every:
                    if almostEqualTuple(sett.getApex(), apex):
                        print('pass2')
                        if sett.getPlayer() == data.me:
                            print('pass3')
                            for resource in data.resources:
                                if resource.returnItem() == tile.getLand():
                                    print('pass4')
                                    resource.getItem(sett.getSize())

def toggleBuild(event, data):
    if data.width-55<event.x<data.width-5 and data.width-80<event.y<data.width-30:
        data.isBuild = not data.isBuild
    if data.isBuild:
        if 10<event.x<data.width-10 and 30<event.y<80:
            data.buildSett = True
            data.isBuild = False
        if 10<event.x<data.width-10 and 100<event.y<150:
            data.buildRoad = True
            data.isBuild = False
        if 10<event.x<data.width-10 and 170<event.y<220:
            data.buildCity = True
            data.isBuild = False

def toggleTrade(event, data):
    msg = ''
    players = ["red", "blue", "white", "orange"]
    resources = ['wood','sheep','clay','wheat']
    players.remove(data.me)
    if data.width-55<event.x<data.width-5 and 30<event.y<80:
        data.isTrade = not data.isTrade
        if not data.isTrade:
            data.tradePlayer = None
            data.resourceToGive = None
            data.resourceToGet = None
        print(data.isTrade)
    if data.isTrade:
        player = ''
        give = ''
        get = ''
        players = ["red", "blue", "white", "orange"]
        resources = ['wood','sheep','clay','wheat', 'stone']
        players.remove(data.me)
        for i in range(3):
            if (data.width/2)-62+(i*50)<event.x<(data.width/2)-62+(i*50)+25 and 150<event.y<175:
                data.tradePlayer = i
                print('hello1')
        for i in range(5):
            if (data.width/2)-138+(i*60)<event.x<(data.width/2)-138+(i*60)+50 and 210<event.y<260:
                data.resourceToGive = i
                print('hello2')
        for i in range(5):
            if (data.width/2)-138+(i*60)<event.x<(data.width/2)-138+(i*60)+50 and 295<event.y<345:
                data.resourceToGet = i
                get += resources[data.resourceToGet]
                print('hello3')
        if data.width-100<event.x<data.width-50 and 360<event.y<385:
            if data.tradePlayer != None and data.resourceToGive != None and data.resourceToGet != None:
                if players[data.tradePlayer] != '' and resources[data.resourceToGive] != '' and resources[data.resourceToGet] != '':
                    print('hello5')
                    data.tradeSent = True
                    data.resOffered = resources[data.resourceToGive]
                    data.resAsked = resources[data.resourceToGet]
                    if enoughResource({data.resOffered:1}, data):
                        msg += 'trade %s %s %s\n' %(players[data.tradePlayer], data.resOffered, data.resAsked)
                    else:
                        data.tradeSent = False
    return msg

def tradeMech(data, give, recieve):
    lstGive = [give]
    lstGet = [recieve]
    spendResources(lstGive, data)
    recResources(lstGet, data)

def replyOffer(event,data):
    msg = ''
    if data.width/3-50 < event.x < data.width/3+50 and 210<event.y<260 and enoughResource({data.resAsked:1}, data):
        msg += 'tradeReply %s yes\n' %(data.playerOffer)
        tradeMech(data, data.resAsked, data.resOffered)
        data.isOffered = False
        data.resOffered = None
        data.resAsked = None
        data.playerOffer = None
    if data.width*(2/3)-50 < event.x<data.width*(2/3)+50 and 210<event.y<260:
        msg += 'tradeReply %s no\n' %(data.playerOffer)
        data.isOffered = False
        data.resOffered = None
        data.resAsked = None
        data.playerOffer = None
    return msg

def getScore(data):
    score = 0
    for sett in Settlements.every:
        if sett.getPlayer() == data.me:
            score += sett.getSize()

    data.leaders[data.me] = score
    return 'score %d\n' %score