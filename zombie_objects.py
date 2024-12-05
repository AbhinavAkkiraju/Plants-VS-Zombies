from cmu_graphics import *
from pathlib import Path
import random

script_dir = Path(__file__).resolve().parent
media_dir = script_dir / "media"
zombies_dir = media_dir / "zombie_gifs"

class Zombie:
    def __init__(self, health, image_path):
        self.lane = random.randint(0, 4)
        self.x = 1450
        self.health = health
        self.damage = 6
        self.y = 0
        self.width = 150
        self.isSlowed = False
        self.notEating = True
        self.isDead = False
        self.height = 130
        match self.lane:
            case 0:
                self.y = 214
            case 1:
                self.y = 338
            case 2:
                self.y = 487
            case 3:
                self.y = 611
            case 4:
                self.y = 747
        self.image = str(image_path)

    def draw(self):
        drawImage(self.image, self.x, self.y - 100, width = self.width, height = self.height)
    
    def takeDamage(self, damage):
        self.health -= damage
        self.isSlowed = True
        if self.health <= 0:
            self.isDead = True

class RegZombie(Zombie):
    def __init__(self):
        super().__init__(200, zombies_dir / "zombie.png") # https://characters.fandom.com/wiki/Zombie_(Plants_Vs_Zombies)

class ConeZombie(Zombie):
    def __init__(self):
        super().__init__(640, zombies_dir / "cone_zombie.gif") # https://plantsvszombies.fandom.com/wiki/Conehead_Zombie/Gallery

class BucketZombie(Zombie):
    def __init__(self):
        super().__init__(1300, zombies_dir / "bucket_zombie.png") # https://plantsvszombies.fandom.com/wiki/Buckethead_Zombie/Gallery