###Socket Base Code from https://kdchin.gitbooks.io/sockets-module-manual/ by kdchin
###Tkinter Run code from 15112 course website: http://www.cs.cmu.edu/~112/notes/notes-animations-part2.html


import socket
import threading
from queue import Queue

HOST = "" # put your IP address here if playing on multiple computers
PORT = 50068

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.connect((HOST,PORT))
print("connected to server")

def handleServerMsg(server, serverMsg):
  server.setblocking(1)
  msg = ""
  command = ""
  while True:
    msg += server.recv(10).decode("UTF-8")
    command = msg.split("\n")
    while (len(command) > 1):
      readyMsg = command[0]
      msg = "\n".join(command[1:])
      serverMsg.put(readyMsg)
      command = msg.split("\n")

# events-example0.py from 15-112 website
# Barebones timer, mouse, and keyboard events
from tkinter import *
from classes import *
from board import *
from pieces import *
from mech import *
import random
from playsound import playsound
import time
####################################
# customize these functions
####################################

def init(data):

    #board calculations
    #list
    data.cpoints = locateHexagons(data)
    data.robber = Robber()
    #lists
    data.lands, data.numbers = shuffleBoard(data)

    #assignedname
    data.me = None

    #set of Tile Class
    for i in range(len(data.cpoints)):
        Tiles(data.cpoints[i], data.lands[i], data.numbers[i])

    data.hexSize = data.width/10
    for tile in Tiles.store:
        #set of sids and apexes
        tile.assignApex(data.hexSize)
        tile.assignSides()

    #states of game
    data.waiting = True
    data.ready = False
    data.start = False
    data.setup1 = False
    data.setup2 = False
    data.isBuild = False
    data.buildRoad = False
    data.buildCity = False
    data.buildSett = False
    data.finished = None
    data.isTrade = False
    data.isOffered = False


    data.sett1 = True
    data.sett2 = True
    data.road1 = True
    data.road2 = True
    data.rolled = False

    data.turn = 0
    data.names = ["red", "blue", "white", "orange"]

    data.dice0 = Dice(1)
    data.dice1 = Dice(2)


    #trade mechs
    data.tradePlayer = None
    data.resourceToGive = None
    data.resourceToGet = None
    data.resOffered = None
    data.resAsked = None
    data.playerOffer = None
    data.tradeSent = False

    data.leaders = {'red':0, 'blue':0, 'white':0, 'orange':0}

    #private info
    data.resources = []
    startingHand(data)

    data.timer = 0

def mousePressed(event, data):
    msg = ''

    if not data.start and data.ready:
        msg += startGame(event,data)

    elif data.isOffered:
        msg += replyOffer(event, data)

    elif data.names[data.turn] == data.me:

        if data.start:
            msg += callNextTurn(event, data)
            if data.rolled:
                msg += rollDice(event, data)

            if data.setup1:
                if data.sett1:
                    msg += starterSettlement(event, data)
                if data.road1:
                    msg += starterRoad(event, data)

            elif data.setup2:
                if data.sett2:
                    msg += starterSettlement(event, data)
                if data.road2:
                    msg += starterRoad(event, data)

            elif not data.setup1 and not data.setup2:
                if data.buildCity:
                    msg += buildCity(event, data)
                elif data.buildSett:
                    msg += buildSettlement(event, data)
                elif data.buildRoad:
                    msg += buildRoad(event, data)
                toggleBuild(event,data)
                msg += toggleTrade(event,data)

    if (msg != ""):
        print ("sending: ", msg,)
        data.server.send(msg.encode())
    

def keyPressed(event, data):
    msg = ''

    if event.keysym == 's':
        data.start = True
        data.setup1 = True
        msg += 'started setup1\n'

    if data.start:
        if event.keysym == 'z':
            data.setup1 = False
            data.setup2 = True
            msg += 'started setup2\n'

        if event.keysym == 'x':
            data.setup2 = False
            data.ready = False
            data.waiting = False
            data.rolled = True
            msg += 'started game\n'

        if event.keysym == 'Left':
            msg += nextTurn(data,-1)

        if event.keysym == 'Right':
            msg += nextTurn(data,1)

    if (msg != ""):
        print ("sending: ", msg,)
        data.server.send(msg.encode())



def timerFired(data):
    data.timer += 1

    msg = ''

    if data.timer%50 == 0:
        msg += getScore(data)

    for key in data.leaders:
        if data.leaders[key] == 10:
            data.start = False
            data.finished = key

    if data.tradeSent>1:
        if data.timer%80 == 0:
            data.tradeSent = False

    if (msg != ""):
        print ("sending: ", msg,)
        data.server.send(msg.encode())
##################################################
    # communications with server
    while (serverMsg.qsize() > 0):
      msg = serverMsg.get(False)
      try:
        print("received: ", msg, "\n")
        msg = msg.split()
        command = msg[0]
        print(msg)

        if (command == "myIDis"):
            data.me = msg[1]
            if msg[1] == 'orange':
                data.waiting = False
                data.ready = True

        
        if (command == "newPlayer"):
            if data.me == 'red':
                newmsg = "Board "
                for land in data.lands:
                    newmsg += (land+' ')
                for number in data.numbers:
                    newmsg += (str(number)+' ')
                newmsg += '\n'
                if (newmsg != ""):
                    print ("sending: ", newmsg,)
                    data.server.send(newmsg.encode())
            if msg[1] == 'orange':
                data.waiting = False
                data.ready = True

        if (command == 'Board'):
            data.lands = []
            data.numbers = []
            Tiles.store = set()
            for i in range(2, 21):
                data.lands.append(msg[i])
            for i in range(21, 40):
                data.numbers.append(int(msg[i]))
            for i in range(len(data.cpoints)):
                Tiles(data.cpoints[i], data.lands[i], data.numbers[i])
            for tile in Tiles.store:
                tile.assignApex(data.hexSize)
                tile.assignSides()
            #moveRobber(data)

        if (command == 'started'):
            if msg[2] == 'setup1':
                print('check')
                data.start = True
                data.setup1 = True
            elif msg[2] == 'setup2':
                data.start = True
                data.setup1 = False
                data.setup2 = True
            elif msg[2] == 'game':
                data.start = True
                data.setup1 = False
                data.setup2 = False
                data.rolled = True

        if (command == 'rolled'):
            data.dice0.setNum(int(msg[2]), msg[1])
            data.dice1.setNum(int(msg[3]), msg[1])
            getResource(data)

        if (command == 'nextTurn'):
            nextTurn(data, int(msg[2]))
            if msg[1] == 'orange':
                if data.setup2:
                    print('c')
                    data.setup2 = False
                    data.ready = False
                    data.waiting = False
                    data.rolled = True
                if data.setup1:
                    print('d')
                    data.setup1 = False
                    data.setup2 = True


        if (command == "newSettle"):
            player = msg[1]
            apex = (int(msg[2]), int(msg[3]))
            Settlements(apex, player).create()

        if (command == "newCity"):
            player = msg[1]
            apex = (int(msg[2]), int(msg[3]))
            for sett in Settlements.every:
                if sett == Settlements(apex, player):
                    sett.upgrade()

        if (command == 'newRoad'):
            for road in Road.allroads:
                x = int(road.getCenter()[0])
                y = int(road.getCenter()[1])
                if (x,y) == (int(msg[2]), int(msg[3])):
                    road.addPlayer(msg[1])

        if (command == 'trade'):
            if msg[2] == data.me:
                data.isOffered = True
                data.resOffered = msg[3]
                data.resAsked = msg[4]
                data.playerOffer = msg[1]

        if (command ==  'tradeReply'):
            if msg[2] == data.me:
                if bool(msg[3]):
                    data.tradeSent = 2
                    tradeMech(data, data.resOffered, data.resAsked)
                else: data.tradeSent = 3
                data.isOffered = False
                data.resOffered = None
                data.resAsked = None
                data.playerOffer = None
                data.isTrade = False
                data.tradePlayer = None
                data.resourceToGive = None
                data.resourceToGet = None


        if (command == 'score'):
            data.leaders[msg[1]] = int(msg[2])

      except:
        print("failed")
      serverMsg.task_done()
################################################


def redrawAll(canvas, data):
    drawBoard(canvas, data) #from board.py
    drawColorSymb(canvas, data)
    drawDice(canvas, data)
    drawResources(canvas, data)
    drawStartNext(canvas, data)
    drawRoll(canvas, data)
    drawBuildToggle(canvas,data)
    drawTradeToggle(canvas, data)

    #data.robber.draw(canvas)

    for sett in Settlements.every:
        sett.draw(canvas)

    for road in Road.allroads:
        road.draw(canvas)

    if data.isBuild:
        drawBuild(canvas,data)

    if data.isTrade:
        drawTrade(canvas, data)

    if data.isOffered:
        drawOffer(canvas, data)

    if data.waiting:
        drawWaiting(canvas, data)

    if data.ready:
        drawReady(canvas, data)

    if data.setup1 or data.setup2:
        drawSetup(canvas, data)

    if data.finished != None:
        canvas.create_rectangle(0,0,data.width, data.width)
        drawLeader(canvas,data)

####################################
# use the run function as-is
####################################

def run(width, height, serverMsg=None, server=None):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        redrawAll(canvas, data)
        canvas.update()

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.server = server
    data.serverMsg = serverMsg
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    init(data)
    # create the root and the canvas
    root = Tk()
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

serverMsg = Queue(100)
threading.Thread(target = handleServerMsg, args = (server, serverMsg)).start()

run(400, 500, serverMsg, server)
