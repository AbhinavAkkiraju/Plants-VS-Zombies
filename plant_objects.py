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
        self.width = self.height = 120
        self.image = str(image_path)
        self.cost = cost
        self.isDead = False
        self.health = health
    
    def draw(self):
        drawImage(self.image, self.x, self.y, width = self.width, height = self.height) # resize on app start
    
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
        self.peaActive = False
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

class Walnut(Plant):
    def __init__(self, row, col):
        super().__init__(row, col, plants_dir / "walnut.png", cost = 50, health = 4000)

class Tallnut(Plant):
    def __init__(self, row, col):
        super().__init__(row, col, plants_dir / "tallnut.png", cost = 125, health = 8000)

class DoubleSunflower(Plant):
    def __init__(self, row, col):
        super().__init__(row, col, plants_dir / "double_sunflower.png", cost = 125, health = 300)
        self.sun = str(media_dir / "sun.png")
        self.sunProductionTimer = 0
        self.sunProductionThreshold = random.randint(200, 300)
    
    def update(self):
        self.sunProductionTimer += 1
        if self.sunProductionTimer >= self.sunProductionThreshold:
            self.sunProductionTimer = 0
            self.sunProductionThreshold = random.randint(100, 200)
            return self.produceSun()
        return None

    def produceSun(self):
        return Sun(self.x + 50, self.y + 50, True)

class DoublePeashooter(Plant):
    def __init__(self, row, col):
        super().__init__(row, col, plants_dir / "double_peashooter.png", cost = 100, health = 300)
        self.peaX = 220 + 145 * col
        self.peaXCopy = self.peaX
        self.damage = 40
        self.peaTimer = 0
        self.peaTime = 50
        self.peaActive = False
        self.fill = None
        self.border = None
    
    def draw(self):
        super().draw()
        drawCircle(self.peaXCopy, self.y + 60, 10, fill=self.fill, border=self.border)
        drawCircle(self.peaXCopy + 20, self.y + 60, 10, fill = self.fill, border = self.border)
        
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

class Iceshooter(Plant):
    def __init__(self, row, col):
        super().__init__(row, col, plants_dir / "iceshooter.png", cost = 100, health = 300)
        self.peaX = 220 + 145 * col
        self.peaXCopy = self.peaX
        self.damage = 20
        self.peaTimer = 0
        self.peaTime = 50
        self.peaActive = False
        self.fill = None
        self.border = None
    
    def draw(self):
        super().draw()
        drawCircle(self.peaXCopy, self.y + 60, 10, fill=self.fill, border=self.border)
        
    def update(self, zombies):
        self.fill = rgb(80,217,255)
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

def postPlant(plant, x, y):
    if os.path.basename(plant) == os.path.basename(str(plants_dir / "pea_shooter.png")): # https://plantsvszombies.fandom.com/wiki/Peashooter
        return Peashooter(x, y)
    elif os.path.basename(plant) == os.path.basename(str(plants_dir / "sunflower.png")): # https://characters.fandom.com/wiki/Sunflower
        return Sunflower(x, y)
    elif os.path.basename(plant) == os.path.basename(str(plants_dir / "walnut.png")): # https://www.pngegg.com/en/png-ydrac
        return Walnut(x, y)
    elif os.path.basename(plant) == os.path.basename(str(plants_dir / "tallnut.png")): # https://plantsvszombies.fandom.com/wiki/Tall-nut
        return Tallnut(x, y)
    elif os.path.basename(plant) == os.path.basename(str(plants_dir / "double_pea_shooter.png")): # https://plantsvszombies.fandom.com/wiki/Repeater
        return DoublePeashooter(x, y)
    elif os.path.basename(plant) == os.path.basename(str(plants_dir / "double_sunflower.png")): # https://plantsvszombies.fandom.com/wiki/Twin_Sunflower
        return DoubleSunflower(x, y)
    elif os.path.basename(plant) == os.path.basename(str(plants_dir / "ice_shooter.png")): # https://www.pngegg.com/en/png-zsemg
        return Iceshooter(x, y)

