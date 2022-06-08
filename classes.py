#roundHalfUp Code from     # https://docs.python.org/3/library/decimal.html#rounding-modes

import random
import math
import decimal
def roundHalfUp(d):
    rounding = decimal.ROUND_HALF_UP
    # See other rounding options here:
    return int(decimal.Decimal(d).to_integral_value(rounding=rounding))

def almostEqual(d1, d2, epsilon=10**-3):
    return (abs(d2 - d1) < epsilon)

def almostEqualTuple(t1, t2, epsilon = 10**-7):
    return (abs(int(t2[0]) - int(t1[0])) < epsilon) and (abs(int(t2[1]) - int(t1[1])) < epsilon)


class Tiles(object):

    land = {'wood':'saddlebrown', 'clay':'tomato3', 'stone':'snow4', \
    'wheat':'goldenrod', 'sheep':'green3', 'desert':'khaki'}
    store = set()
    allapex = set()
    allsides = set()

    def __init__(self, cpoint, land, number):
        self.cpoint = cpoint
        self.land = land
        self.color = Tiles.land[self.land]
        self.number = number
        self.apex = []
        self.side = []
        Tiles.store.add(self)

    def __hash__(self):
        return hash((self.cpoint))

    def __eq__(self, other):
        return (isinstance(other, Tiles) and \
        self.cpoint == other.cpoint and self.land == other.land and self.number == other.number)

    def __repr__(self):
        cx, cy = self.cpoint
        return("%d, %d, %s, %d" %(cx, cy, self.land, self.number))

    def assignApex(self, hexSize):
        apexList = []
        cx, cy = self.cpoint
        for i in range(6):
            angle = ((math.pi)*i)/3
            px = cx-hexSize*math.cos(angle)
            py = cy-hexSize*math.sin(angle)
            apexList.append((px,py))
        self.apex = apexList
        for apex in self.apex:
            Tiles.allapex.add(apex)

    def assignSides(self):
        sideList = []
        for i in range(len(self.apex)):
            pathx = (self.apex[i][0] + self.apex[i-1][0])/2
            pathy = (self.apex[i][1] + self.apex[i-1][1])/2
            sideList.append(Road(self.apex[i], self.apex[i-1], pathx, pathy, None))
        self.side = sideList
        for side in self.side:
            Tiles.allsides.add(side)

    def getcpoint(self):
        return self.cpoint

    def getApex(self):
        return self.apex

    def getSide(self):
        return self.side

    def getNumber(self):
        return self.number

    def getLand(self):
        return self.land

    def draw(self, canvas, data):
        canvas.create_polygon(self.apex, fill = self.color, outline = 'black')
        canvas.create_text(self.cpoint, text = self.land + '\n' + str(self.number))


class Settlements(object):
    red = set()
    blue = set()
    white = set()
    orange = set()
    every = set()

    def __init__(self, apex, player, size=1):
        self.apex = apex
        self.player = player
        self.size = size


    def create(self):
        player = self.player
        Settlements.every.add(self)
        if player == 'red':
            Settlements.red.add(self)
        elif player == 'blue':
            Settlements.blue.add(self)
        elif player == 'white':
            Settlements.white.add(self)
        elif player == 'orange':
            Settlements.orange.add(self)

    def __hash__(self):
        return hash((self.apex, self.player))

    def __repr__(self):
        apexx,apexy = self.apex
        return "set(%d, %d)" %(apexx, apexy)

    def __eq__(self, other):
        return (isinstance(other, Settlements) and self.apex == other.apex and self.player == other.player)

    def getApex(self):
        return self.apex

    def getSize(self):
        return self.size

    def getPlayer(self):
        return self.player

    def upgrade(self):
        self.size = 2

    def draw(self, canvas):
        cx, cy = self.apex
        if self.size == 1:
            points = [(cx-10, cy), (cx-10, cy+10), (cx+10, cy+10), (cx+10, cy), (cx, cy-10)]
            canvas.create_polygon(points, fill = self.player, outline = 'black')
        elif self.size == 2: 
            points = [(cx-3, cy), (cx-10, cy), (cx-10, cy+10), (cx+10, cy+10), (cx+10, cy-7), (cx+5, cy-10), (cx-3, cy-7)]
            canvas.create_polygon(points, fill = self.player, outline = 'black')

class Road(object):
    allroads = set()
    def __init__(self, pointa, pointb, sidex, sidey, player=None):
        self.pointa = pointa
        self.pointb = pointb
        self.sidex = roundHalfUp(sidex)
        self.sidey = roundHalfUp(sidey)
        self.player = player
        Road.allroads.add(self)

    def __repr__(self):
        return "Road(%d %d)" %(self.sidex, self.sidey)

    def __hash__(self):
        return hash((roundHalfUp(self.sidex), roundHalfUp(self.sidey)))

    def __eq__(self, other):
        return isinstance(other, Road) and almostEqualTuple((self.sidex, self.sidey),(other.sidex, other.sidey))

    def getCenter(self):
        return self.sidex, self.sidey

    def getPlayer(self):
        return self.player

    def getPoints(self):
        return (self.pointa, self.pointb)

    def addPlayer(self, player):
        self.player = player

    def draw(self, canvas):
        r = 4
        if self.player == None:
            canvas.create_oval(self.sidex-r, self.sidey-r, self.sidex+r, self.sidey+r, fill = 'white')
        else:
            canvas.create_line(self.pointa, self.pointb, fill=self.player, width = 10)
    
class Dice(object):
    def __init__(self, num, color = 'white', max = 6):
        self.max = max
        self.value = 6
        self.num = num
        self.color = color

    def roll(self, color):
        self.value = random.randint(1, self.max)
        self.color = color
        return self.getNumber()

    def setNum(self, num, color):
        self.value = num
        self.color = color

    def getNumber(self):
        return self.value

    def send(self):
        return 'rolled %d %d\n' %(self.num, self.value)

    def drawDot(self, canvas, x, y):
        canvas.create_oval(x-2, y-2, x+2, y+2, fill = 'black')

    def draw(self, canvas, x, y):
        size = 14
        canvas.create_rectangle(x-size, y-size, x+size, y+size, fill = self.color, outline = 'black')
        if self.value == 1:
            self.drawDot(canvas, x, y)
        elif self.value == 2:
            self.drawDot(canvas, x-6, y-6)
            self.drawDot(canvas, x+6, y+6)
        elif self.value == 3:
            self.drawDot(canvas, x-6, y-6)
            self.drawDot(canvas, x, y)
            self.drawDot(canvas, x+6, y+6)
        elif self.value == 4:
            self.drawDot(canvas, x-6, y-6)
            self.drawDot(canvas, x-6, y+6)
            self.drawDot(canvas, x+6, y-6)
            self.drawDot(canvas, x+6, y+6)
        elif self.value == 5:
            self.drawDot(canvas, x-6, y-6)
            self.drawDot(canvas, x, y)
            self.drawDot(canvas, x-6, y+6)
            self.drawDot(canvas, x+6, y-6)
            self.drawDot(canvas, x+6, y+6)
        elif self.value == 6:
            self.drawDot(canvas, x-6, y-6)
            self.drawDot(canvas, x-6, y)
            self.drawDot(canvas, x+6, y)
            self.drawDot(canvas, x-6, y+6)
            self.drawDot(canvas, x+6, y-6)
            self.drawDot(canvas, x+6, y+6)

class Robber(object):
    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y

    def move(self, cpoint):
        self.x, self.y = cpoint

    def draw(self, canvas):
        cx, cy = self.x, self.y - 10
        r = 15
        canvas.create_oval(cx-r, cy-r, cx +r, cy + r, fill = 'gray', outline = '')
        points = [(self.x-7, self.y-7), (self.x-15, self.y+20), (self.x+15, self.y+20), (self.x+7, self.y-7)]
        canvas.create_polygon(points, fill = 'gray', outline = '')


class Resources(object):
    color = {'wood':'saddlebrown', 'clay':'tomato3', 'stone':'snow4', \
    'wheat':'goldenrod', 'sheep':'green3', 'desert':'khaki'}

    def __init__(self, item, amount = 0):
        self.item = item
        self.amount = amount
        self.color = Resources.color[item]

    def getItem(self, count):
        self.amount += count

    def spendItem(self, cost):
        self.amount -= cost

    def returnAmount(self):
        return self.amount

    def returnItem(self):
        return self.item

    def draw(self, canvas, x, y):
        size = 20
        canvas.create_rectangle(x-size, y-size, x+size, y+size, fill = self.color)
        canvas.create_text(x, y, text=self.item)
        canvas.create_text(x+size+12, y, text='x %d' %self.amount)

