from cmu_graphics import *
from pathlib import Path
import random
from level_objects import Sun
import os

script_dir = Path(__file__).resolve().parent
media_dir = script_dir / "media"
plants_dir = media_dir / "plants_gifs"

class Plant:
    def __init__(self, row, col, image_path, cost, health):
        self.x = 160 + 145 * col
        self.y = 90 + 134 * row
        self.image = str(image_path)
        self.cost = cost
        self.isDead = False
        self.health = health
    
    def draw(self):
        drawImage(self.image, self.x, self.y, width = 120, height = 120)
    
    def takeDamage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.isDead = True

class Peashooter(Plant):
    def __init__(self, row, col):
        super().__init__(row, col, plants_dir / "peashooter.gif", cost = 100, health = 300)
        self.peaX = 220 + 145 * col
        self.peaXCopy = self.peaX
        self.damage = 20
        self.peaTimer = 0
        self.peaTime = 50
        self.fill = None
        self.border = None
    
    def draw(self):
        super().draw()
        drawCircle(self.peaXCopy, self.y + 60, 10, fill=self.fill, border=self.border)
        
    def update(self, zombies):
        self.fill = rgb(187,215,100)
        self.border = 'black'
        self.peaTimer += 1
        self.peaXCopy += 50
        for zombie in zombies:
            if self.peaXCopy > zombie.x+(zombie.width/2):
                zombie.takeDamage(self.damage)
                self.peaXCopy = self.peaX
        if self.peaXCopy > 1920:
            self.peaXCopy = self.peaX
        
    def reset(self):
        self.fill = None
        self.border = None
        self.peaXCopy = self.peaX
        self.peaTimer = 0
        
class Sunflower(Plant):
    def __init__(self, row, col):
        super().__init__(row, col, plants_dir / "sunflower.gif", cost = 50, health = 300)
        self.sun = str(media_dir / "sun.png")
        self.sunProductionTimer = 0
        self.sunProductionThreshold = random.randint(100, 200)
    
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

