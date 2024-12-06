from cmu_graphics import *
from zombie_objects import RegZombie, ConeZombie, BucketZombie

def set_level_one(app):
    app.sunFallSpeed = 3
    app.sunSpawnTimer = 0
    app.zombieSpeed = 1.5
    app.totalZombies = 15
    app.possibleZombies = []
    for _ in range(9):
        app.possibleZombies.append(RegZombie())
    for _ in range(3):
        app.possibleZombies.append(ConeZombie())
    for _ in range(3):
        app.possibleZombies.append(BucketZombie())

def set_level_two(app):
    app.sunFallSpeed = 3
    app.sunSpawnTimer = 0
    app.zombieSpeed = 1.5
    app.totalZombies = 25
    app.possibleZombies = []
    for _ in range(12):
        app.possibleZombies.append(RegZombie())
    for _ in range(6):
        app.possibleZombies.append(ConeZombie())
    for _ in range(7):
        app.possibleZombies.append(BucketZombie())

def set_level_three(app):
    app.sunFallSpeed = 3
    app.sunSpawnTimer = 0
    app.zombieSpeed = 2
    app.totalZombies = 30
    app.possibleZombies = []
    for _ in range(6):
        app.possibleZombies.append(RegZombie())
    for _ in range(12):
        app.possibleZombies.append(ConeZombie())
    for _ in range(12):
        app.possibleZombies.append(BucketZombie())

def set_level_byol(app):
    app.sunFallSpeed = 3
    app.sunSpawnTimer = 0
    app.zombieSpeed = 1.5
    app.totalRegZombies = 0
    app.totalConeZombies = 0
    app.totalBucketZombies = 0
