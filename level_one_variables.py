from cmu_graphics import *
from zombie_objects import RegZombie, ConeZombie, BucketZombie

def level_one_variables(app):
    app.isLevelOne = True
    app.sunFallSpeed = 3
    app.sunSpawnTimer = 0
    app.zombieSpeed = 1
    app.totalZombies = 10
    app.possibleZombies = []
    for _ in range(6):
        app.possibleZombies.append(RegZombie())
    for _ in range(2):
        app.possibleZombies.append(ConeZombie())
    for _ in range(2):
        app.possibleZombies.append(BucketZombie())