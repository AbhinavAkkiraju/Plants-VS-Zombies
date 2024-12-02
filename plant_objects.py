from cmu_graphics import *
from pathlib import Path
import random
from level_objects import Sun
import os

script_dir = Path(__file__).resolve().parent
media_dir = script_dir / "media"
plants_dir = media_dir / "plants_gifs"

class Peashooter:
    def __init__(self, row, col):
        self.x = 160 + 145 * col
        self.y = 90 + 134 * row
        self.image = str(plants_dir / "peashooter.gif")
        self.peaX = 220 + 145 * col
        self.peaXCopy = self.peaX
        self.damage = 20
        self.peaTimer = 0
        self.peaTime = 5
        self.cost = 100
        self.fill = None
        self.border = None
        self.zombie_seen = False
    
    def draw(self):
        drawImage(self.image, self.x, self.y, width = 120, height = 120)
        drawCircle(self.peaXCopy, self.y + 50, 10, fill=self.fill, border=self.border)
        
    def update(self, zombies):
        self.peaXCopy += 50
        self.peaTimer += 1
        self.fill = rgb(187,215,100)
        self.border = 'black'
        for zombie in zombies:
            if self.peaXCopy > zombie.x+(zombie.width/2):
                zombie.takeDamage(self.damage)
                self.peaXCopy = self.peaX
        if self.peaXCopy > 1500:
            self.peaXCopy = self.peaX
        
class Sunflower:
    def __init__(self, row, col):
        self.x = 160 + 145 * col
        self.y = 90 + 134 * row
        self.image = str(plants_dir / "sunflower.gif")
        self.sun = str(media_dir / "sun.png")
        self.cost = 50
        self.sunProductionTimer = 0
        self.sunProductionThreshold = random.randint(100, 200)
    
    def draw(self):
        drawImage(self.image, self.x, self.y, width = 120, height = 120)
    
    def update(self):
        self.sunProductionTimer += 1
        if self.sunProductionTimer >= self.sunProductionThreshold:
            self.sunProductionTimer = 0
            self.sunProductionThreshold = random.randint(100, 200)
            return self.produceSun()
        return None

    def produceSun(self):
        return Sun(self.x + 50, self.y + 50, True)
    
def postPlant(plant, x, y):
    if os.path.basename(plant) == os.path.basename(str(plants_dir / "pea_shooter.png")):
        return Peashooter(x, y)
    elif os.path.basename(plant) == os.path.basename(str(plants_dir / "sunflower.png")):
        return Sunflower(x, y)

