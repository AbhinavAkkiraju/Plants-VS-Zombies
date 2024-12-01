from cmu_graphics import *
from pathlib import Path
import os

script_dir = Path(__file__).resolve().parent
media_dir = script_dir / "media"
plants_dir = media_dir / "plants_gifs"

class Peashooter:
    def __init__(self, row, col):
        self.x = 160 + 145 * col
        self.y = 90 + 134 * row
        self.image = str(plants_dir / "peashooter.gif")
        self.cost = 100
    
    def draw(self):
        drawImage(self.image, self.x, self.y, width = 120, height = 120)

def postPlant(plant, x, y):
    if os.path.basename(plant) == os.path.basename(str(plants_dir / "pea_shooter.png")):
        return Peashooter(x, y)

