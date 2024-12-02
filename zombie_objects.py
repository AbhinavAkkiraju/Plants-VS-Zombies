from cmu_graphics import *
from pathlib import Path
import random

script_dir = Path(__file__).resolve().parent
media_dir = script_dir / "media"
zombies_dir = media_dir / "zombie_gifs"

class Zombie:
    def __init__(self):
        self.lane = random.randint(0, 4)
        self.x = 1450
        self.health = 200
        self.y = 0
        self.width = 150
        self.isDead = False
        self.height = 130
        match self.lane:
            case 0:
                self.y = 105
            case 1:
                self.y = 241
            case 2:
                self.y = 371
            case 3:
                self.y = 508
            case 4:
                self.y = 643
        self.image = str(zombies_dir / "zombie.gif")

    def draw(self):
        drawImage(self.image, self.x, self.y, width = self.width, height = self.height)
    
    def takeDamage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.isDead = True