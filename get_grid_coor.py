from cmu_graphics import *

def getClosestGridCoor(x, y):

    def getRow():
        if y <= 252:
            return 0
        elif y <= 380:
            return 1
        elif y <= 528:
            return 2
        elif y <= 637:
            return 3
        return 4

    if x >= 1294:
        return (getRow(), 8)
    elif x >= 1143:
        return (getRow(), 7)
    elif x >= 1019:
        return (getRow(), 6)
    elif x >= 862:
        return (getRow(), 5)
    elif x >= 723:
        return (getRow(), 4)
    elif x >= 581:
        return (getRow(), 3)
    elif x >= 429:
        return (getRow(), 2)
    elif x >= 293:
        return (getRow(), 1)
    elif x >= 154:
        return (getRow(), 0)