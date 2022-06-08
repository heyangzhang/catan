from classes import *
import math

def locateHexagons(data):
    cpoints = []
    hexSize = data.width/10
    centerBisect = hexSize * math.sin(math.pi/3)
    centerx = data.width/2
    centery = centerx
    circleRad1 = centerBisect*2
    circleRad2 = hexSize*3
    circleRad3 = centerBisect*4
    boardCircle = [circleRad1, circleRad2, circleRad3]
    cpoints.append((centerx, centerx))
    for i in range(6):
        angle = (math.pi/6)+(math.pi*i)/3
        cpointx = centerx + boardCircle[0]*math.cos(angle)
        cpointy = centery + boardCircle[0]*math.sin(angle)
        cpoints.append((cpointx, cpointy))
    for i in range(6):
        angle = math.pi*i/3
        cpointx = centerx + boardCircle[1]*math.cos(angle)
        cpointy = centery + boardCircle[1]*math.sin(angle)
        cpoints.append((cpointx, cpointy))
    for i in range(6):
        angle = (math.pi/6)+(math.pi*i)/3
        cpointx = centerx + boardCircle[2]*math.cos(angle)
        cpointy = centery + boardCircle[2]*math.sin(angle)
        cpoints.append((cpointx, cpointy))
    return cpoints

def shuffleBoard(data):
#returns a tuple of lists of randomized lands and nums
    lands = ['wood'] * 4 + ['wheat'] * 4 + ['sheep'] * 4 \
    + ['clay'] * 3 + ['stone'] * 3
    numbers = [11, 12, 9, 4, 6, 5, 10, 3, 11, 4, 8, 8, 10, 9, 3, 5, 2, 6]
    random.shuffle(lands)
    random.shuffle(numbers)
    randIndex = random.randint(0,17)
    lands.insert(randIndex, 'desert')
    numbers.insert(randIndex, 7)
    data.robber.move(data.cpoints[randIndex])
    return (lands, numbers)

def drawBoard(canvas, data):
    canvas.create_rectangle(0,0, data.width, data.width, fill = 'steelblue1')
    for tile in Tiles.store:
        tile.draw(canvas, data)
    canvas.create_rectangle(0, data.width, data.width, data.height, fill = 'lightcyan')
    canvas.create_rectangle(data.width-50, data.width, data.width, data.height, fill = 'thistle1')
    canvas.create_rectangle(0, data.width, 80, data.height, fill = 'thistle1')


def drawStartNext(canvas, data):
    canvas.create_rectangle(5,data.width+5, 75, data.width+45, fill = 'white')
    if not data.start:
        canvas.create_text(40, data.width+(25), text = 'START')
    elif data.start: 
        canvas.create_text(40, data.width+(25), text = 'NEXT\nTURN')

def drawRoll(canvas, data):
    canvas.create_rectangle(5, data.width+50, 75, data.width+90, fill = 'white')
    canvas.create_text(40, data.width+70, text ='ROLL')

def drawBuild(canvas, data):
    canvas.create_rectangle(20,25,data.width-20,225, fill ='gray')
    canvas.create_rectangle(25,30, data.width-25,80, fill = 'white')
    canvas.create_text(data.width/2, 55, text = 'Build Settlement')
    canvas.create_rectangle(25,100, data.width-25, 150, fill = 'white')
    canvas.create_text(data.width/2, 125, text = 'Build Road')
    canvas.create_rectangle(25, 170, data.width-25, 220, fill = 'white')
    canvas.create_text(data.width/2, 195, text = 'Build City')

def drawBuildToggle(canvas, data):
    canvas.create_oval(data.width-55,data.width-80,data.width-5, data.width-30, fill='white', outline = 'black')
    if data.isBuild:
        canvas.create_text(data.width-30,data.width-55, text='Back')
    if not data.isBuild:
        canvas.create_text(data.width-30, data.width-55, text='Build')

def drawOffer(canvas, data):
    canvas.create_rectangle(20,125,data.width-20,275, fill ='gray')
    canvas.create_text(data.width/2, 180, text = '%s offered you a Trade!\ntheir %s for your %s\nyou must reject a trade you cannot complete!'%(data.playerOffer, data.resOffered, data.resAsked))
    canvas.create_rectangle(data.width/3-50, 210, data.width/3+50, 260, fill ='green')
    canvas.create_text(data.width/3, 235, text='accept')
    canvas.create_rectangle(data.width*(2/3)-50, 210, data.width*(2/3)+50, 260, fill ='red')
    canvas.create_text(data.width*(2/3), 235, text='reject')

def drawTrade(canvas, data):
    players = ["red", "blue", "white", "orange"]
    resources = ['wood','sheep','clay','wheat', 'stone']
    canvas.create_rectangle(20,125,data.width-20,390, fill ='gray')
    canvas.create_text(data.width/2, 140, text = 'Select Player')
    players.remove(data.me)
    for i in range(3):
        canvas.create_rectangle((data.width/2)-62+(i*50),150, (data.width/2)-62+(i*50)+25, 175, fill = players[i])
    canvas.create_text(data.width/2, 200, text='Select Resource to Give (that you have)')
    for i in range(5):
        canvas.create_rectangle((data.width/2)-138+(i*60),210, (data.width/2)-138+(i*60)+50, 260, fill = Tiles.land[resources[i]])
        canvas.create_text((data.width/2)-138+(i*60)+25,235, text=resources[i])
    canvas.create_text(data.width/2, 285, text='Select Resource to Recieve')
    for i in range(5):
        canvas.create_rectangle((data.width/2)-138+(i*60),295, (data.width/2)-138+(i*60)+50, 345, fill = Tiles.land[resources[i]])
        canvas.create_text((data.width/2)-138+(i*60)+25,320, text=resources[i])
    canvas.create_rectangle(data.width-100, 360, data.width-50, 385, fill='green')
    canvas.create_text(data.width-75, 372, text='send')

    if data.tradePlayer != None:
        i = data.tradePlayer
        canvas.create_rectangle((data.width/2)-62+(i*50),150, (data.width/2)-62+(i*50)+25, 175, fill = players[i], width = 5)
    if data.resourceToGive != None:
        i = data.resourceToGive
        canvas.create_rectangle((data.width/2)-138+(i*60),210, (data.width/2)-138+(i*60)+50, 260, fill = None, width = 5)
    if data.resourceToGet != None:
        i = data.resourceToGet
        canvas.create_rectangle((data.width/2)-138+(i*60),295, (data.width/2)-138+(i*60)+50, 345, fill = None, width = 5)

    if data.tradeSent == True:
        canvas.create_rectangle(20,125,data.width-20,390, fill ='gray')
        canvas.create_text(data.width/2, (390+125)/2, text='waiting...')
    if data.tradeSent == 2:
        canvas.create_rectangle(20,125,data.width-20,390, fill ='gray')
        canvas.create_text(data.width/2, (390+125)/2, text='Accepted')
    if data.tradeSent == 3:
        canvas.create_rectangle(20,125,data.width-20,390, fill ='gray')
        canvas.create_text(data.width/2, (390+125)/2, text='Rejected')


def drawTradeToggle(canvas, data):
    canvas.create_oval(data.width-55, 80, data.width-5, 30, fill = 'white', outline = 'black')
    if data.isTrade:
        canvas.create_text(data.width-30, 55, text='Back')
    if not data.isTrade:
        canvas.create_text(data.width-30, 55, text='Trade')

def drawWaiting(canvas, data):
    canvas.create_rectangle(80, data.width, data.width-50, data.height, fill ='white')
    canvas.create_text((data.width+30)/2, (data.width+data.height)/2, text = 'waiting for all \nfour players to join...')

def drawReady(canvas, data):
    canvas.create_rectangle(80, data.width, data.width-50, data.height, fill ='white')
    canvas.create_text((data.width+30)/2, (data.width+data.height)/2, text = 'ready to start')

def drawSetup(canvas, data):
    canvas.create_rectangle(80, data.width, data.width-50, data.height, fill ='white')
    canvas.create_text((data.width+30)/2, (data.width+data.height)/2, text = 'place a starting \nsettlement and road')

def drawColorSymb(canvas,data):
    color = data.me
    currColor = data.names[data.turn]
    colorindex = 0
    if color != None:
        colorindex = data.names.index(color)+1
    canvas.create_oval(5,5,25,25, fill=color, outline = 'black')
    canvas.create_text(65, 15, text='your color')
    canvas.create_oval(5,30,25,50, fill=currColor, outline = 'black')
    canvas.create_text(65, 40, text='curr color')
    canvas.create_text(15, 15, text = str(colorindex))

def drawLeader(canvas, data):
    canvas.create_rectangle(0,0,data.width, data.height, fill = 'white')
    canvas.create_text(data.width/2, data.height/2, text = 'GAME OVER!\n%s: %d\n%s: %d\n%s: %d\n%s: %d\n'\
     %('red', data.leaders['red'], 'blue', data.leaders['blue'], 'white', data.leaders['white'], 'orange', data.leaders['orange']))
