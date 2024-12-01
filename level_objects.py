from cmu_graphics import *
from pathlib import Path
import random

script_dir = Path(__file__).resolve().parent
media_dir = script_dir / "media"

class Lawnmower:
    def __init__(self, lane):
        self.lane = lane
        self.width = self.height = 100
        self.image_path = str(media_dir / "lawn_mower.png")
        self.activated = False
        self.x = self.y = 0
        match lane:
            case 1:
                self.x = 50
                self.y = 105
            case 2:
                self.x = 50
                self.y = 241
            case 3:
                self.x = 50
                self.y = 371
            case 4:
                self.x = 40
                self.y = 508
            case 5:
                self.x = 30
                self.y = 643
        drawImage(self.image_path, self.x, self.y, width = self.width, height = self.height)
    
class PlantCard:
    def __init__(self, number, plant):
        self.x = 0
        self.y = 10
        self.width = 75
        self.height = 80
        match number:
            case 1:
                self.x = 133
            case 2:
                self.x = 226
            case 3:
                self.x = 321
            case 4:
                self.x = 414
            case 5:
                self.x = 506
            case 6:
                self.x = 600
        drawImage(plant, self.x, self.y, width = self.width, height = self.height)

class Sun:
    def __init__(self):
        self.x = random.randint(20, 1900)
        self.y = 0
        self.radius = 30
        self.height = 75
        self.width = 75
        self.image = str(media_dir / "sun.png")

    def draw(self):
        drawImage(self.image, self.x - self.radius, self.y - self.radius, height = self.height, width = self.width)
