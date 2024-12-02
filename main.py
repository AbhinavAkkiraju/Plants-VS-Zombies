from cmu_graphics import *
from pathlib import Path
import random
from level_objects import Lawnmower, PlantCard, Sun
from plant_objects import postPlant, Sunflower, Peashooter, DoublePeashooter, Iceshooter
from zombie_objects import RegZombie, ConeZombie, BucketZombie
from get_grid_coor import getClosestGridCoor
import time
import pygame

script_dir = Path(__file__).resolve().parent
media_dir = script_dir / "media"
plants_dir = media_dir / "plants"

pygame.mixer.init()

def onAppStart(app):
    # Setting screen size to 1920x1080 (default)
    app.width = 1920
    app.height = 1080

    # Loading screen
    app.url_loading_background = str(media_dir / "loading_screen.png") # https://www.spriters-resource.com/mobile/plantsvszombies/sheet/206074/
    app.url_title = str(media_dir / "title_header.png") # https://www.amazon.com/Plants-vs-Zombies-1-Lawnmageddon/dp/1616551925 
    app.url_loading = str(media_dir / "loading_bar.png") # https://www.alamy.com/stock-photo-plants-vs-zombies-pc-game-loading-screen-38615868.html 
    app.background_music = pygame.mixer.Sound(str(media_dir / "music.mp3")) # https://www.youtube.com/watch?v=7EPqbS_ErgE&list=PL-Ha54QFPaSs5omBkutsbVXUhP6Fexutp
    app.background_music.play(-1)
    app.isLoadingScreen = True
    app.click_sound = pygame.mixer.Sound(str(media_dir / "click_sound.mp3")) # https://www.youtube.com/watch?v=i0DON3AjhW4&pp=ygULY2xpY2sgc291bmQ%3D

    # Selector screen 
    app.isHomeScreen = False
    app.url_home_background = str(media_dir / "selector_screen.png") # Screenshot from my iPhone - Plants VS Zombies 1 Application

    # Help and options screen
    app.isHelpOptionsScreen = False
    app.url_help_box = str(media_dir / "help_options_screen.png") # Screenshot from my iPhone - Plants VS Zombies 1 Application
    app.coverUnwantedColor = rgb(26,28,41)
    app.lineColor = rgb(139, 159, 169)
    app.outsideDragger = rgb(137, 138, 182)
    app.insideDragger = rgb(76, 78, 93)
    app.slider1OuterCoor = [[1000, 320], [1003, 321], [1017, 354], [1009, 365], [993, 366], [984, 356]]
    app.slider1InnerCoor = [[1000, 333], [1006, 341], [1002, 359], [993, 356]]
    app.slider2OuterCoor = [[998, 378], [1004, 378], [1018, 410], [1009, 422], [993, 423], [983, 409], [986, 403]]
    app.slider2InnerCoor = [[1000, 390], [1005, 397], [1008, 410], [998, 416], [993, 413]]

    # Level selector screen
    app.isLevelSelectorScreen = False
    app.level_selector_screen_background = str(media_dir / "level_selector_screen.png") # Screenshot from my iPhone - Plants VS Zombies 1 Application

    # Level 1 (grass level)
    app.isGrassLevel = False
    app.grass_level_background = str(media_dir / "front_yard_grass.png") # https://www.reddit.com/r/PlantsVSZombies/comments/vqqhjs/i_made_pvz_evening_enjoy/
    app.lawnmowers = {"lawnmower1":[], "lawnmower2":[], "lawnmower3":[], "lawnmower4":[], "lawnmower5":[]}
    app.topbar = {'plant1':[], 'plant2':[], 'plant3':[], 'plant4':[], 'plant5':[], 'plant6':[]}
    app.sun = str(media_dir / "sun.png") # https://heroism.fandom.com/wiki/Sun_(Plants_vs._Zombies)
    app.sun_count = 50
    app.plants_top_bar = str(media_dir / "plants_top_bar.png") # https://plantsvszombies.fandom.com/wiki/Ice_Level
    app.shovel = str(media_dir / "shovel.png") # https://plantsvszombies.fandom.com/wiki/Ice_Level
    app.grid = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0]]
    app.card_selected = None
    app.gridX = app.gridY = 0
    app.suns = []
    app.sunFallSpeed = 3
    app.sunSpawnTimer = 0
    app.zombieSpeed = 1
    app.zombiesKilled = 0
    app.zombieSpawnTimer = 0
    app.totalZombies = 50
    app.totalRegZombies = 30
    app.totalConeZombies = 10
    app.totalBucketZombies = 10
    app.zombies = []
    app.sunflowers = []
    app.lanesOccupied = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0}
    app.possibleZombies = []
    app.shovel_activated = False

    # Animation for grass level to move from left to right for plant select screen
    app.stepsPerSecond = 100
    app.grassX = 0

    # Plant select screen
    app.isPlantSelectScreen = False
    app.plant_select_background = str(media_dir / "plant_select_screen.png") # https://www.solitairelaboratory.com/solitairearcade/zombies/plantsvszombiesguide.html
    app.selected_plants = []
    app.curr_plant = None
    app.moved_plant = False
    app.delete_plant = str(media_dir / 'trash.png') # https://pvzcc.fandom.com/wiki/Stealthy_Imp_(PvZ2)
    app.selected_delete_card = None
    app.grassLevelStarted = False
    app.animationDone = False
    app.countdown = False
    app.number = 4
    app.progress = 0
    app.countdownDone = False
    app.levelWon = False

    # Plants
    # All of these are screenshots from this image: https://tvtropes.org/pmwiki/pmwiki.php/Characters/PlantsVsZombiesPlants
    app.pea_shooter_card = str(plants_dir / "pea_shooter.png")
    app.sunflower_card = str(plants_dir / "sunflower.png")
    app.walnut_card = str(plants_dir / "walnut.png")
    app.double_pea_shooter_card = str(plants_dir / "double_pea_shooter.png")
    app.ice_shooter_card = str(plants_dir / "ice_shooter.png")
    app.tallnut_card = str(plants_dir / "tallnut.png")
    app.double_sunflower_card = str(plants_dir / "double_sunflower.png")
    app.all_plants = [app.pea_shooter_card, app.sunflower_card, app.walnut_card, app.double_pea_shooter_card, app.ice_shooter_card, app.tallnut_card, app.double_sunflower_card]

def redrawAll(app):
    if app.isLoadingScreen: # Drawing the loading screen
        drawImage(app.url_loading_background, 0, 0, width = app.width, height = app.height)
        drawImage(app.url_title, 280, 20, width = 1000, height = 190)
        drawImage(app.url_loading, 590, 650, width = 400, height = 120)
    
    elif app.isHomeScreen: # Drawing the level selector screen
        drawImage(app.url_home_background, 0, 0, width = app.width, height = app.height)

        if app.isHelpOptionsScreen:
            drawImage(app.url_help_box, 400, 170, width = 800, height = 500)
            drawRect(550, 430, 600, 100, fill = app.coverUnwantedColor)
            drawRect(854, 305, 300, 130, fill = app.coverUnwantedColor)
            drawLine(870, 345, 1128, 345, fill = app.lineColor, lineWidth = 3.5)
            drawLine(870, 400, 1128, 400, fill = app.lineColor, lineWidth = 3.5)
            drawPolygon(*[coord for point in app.slider1OuterCoor for coord in point], fill = app.outsideDragger)
            drawPolygon(*[coord for point in app.slider1InnerCoor for coord in point], fill = app.insideDragger)
            drawPolygon(*[coord for point in app.slider2OuterCoor for coord in point], fill = app.outsideDragger)
            drawPolygon(*[coord for point in app.slider2InnerCoor for coord in point], fill = app.insideDragger)
    
    if app.isLevelSelectorScreen:
        drawImage(app.level_selector_screen_background, 0, 0, width = app.width, height = app.height)
        drawLabel('BYOL', 1223, 337, size = 20, font = 'grenze', fill = 'white')
    
    if app.isGrassLevel:
        drawImage(app.grass_level_background, 0 - app.grassX, 0, width = 2500, height = app.height)
        if app.isPlantSelectScreen:
            drawImage(app.plant_select_background, 0, -20, width = 1300, height = app.height)
            drawRect(134, 20, 576, 93, fill = rgb(99,47,23))
            
            left = 45
            top = 180
            for plant in app.all_plants:
                if left == (45 + (85*7)):
                    top += 100
                    left = 45
                drawImage(plant, left, top, width = 75, height = 85)
                left += 85

            top = 22
            width = 78
            height = 93
            for i, plant in enumerate(app.selected_plants):
                left = 145 + (95 * i)           
                drawImage(plant, left, top, width = width, height = height)
            
            drawCircle(794, 66, 55, fill = rgb(146,147,143), border = rgb(74,73,75))
            drawImage(app.delete_plant, 757, 30, width = 85, height = 85)
        if app.countdown:
            drawLabel(app.number, app.width/2, app.height/2, size=100)

        if app.levelWon:
            drawLabel("YOU WIN!", app.width/2, app.height/2, size=100)

        if app.grassLevelStarted and app.animationDone:
            for i in range(1, 6):
                app.lawnmowers[i-1] = Lawnmower(i)
            drawImage(app.plants_top_bar, 0, 0, width = 700, height = 100)
            for i, plant in enumerate(app.selected_plants):
                app.topbar[i] = PlantCard(i+1, plant)
            drawRect(15, 70, 85, 30, fill=rgb(233,239,186))
            drawLabel(str(app.sun_count), 60, 85, bold = True, size = 24)
            drawImage(app.shovel, 710, 5, width = 100, height = 90)
            for row in range(5):
                for col in range(9):
                    if not isinstance(app.grid[row][col], int):
                        app.grid[row][col].draw()
            for sun in app.suns:
                sun.draw()
            for zombie in app.zombies:
                zombie.draw()
            drawRect(870, 25, 330, 45, fill = rgb(71,88,113), border = "black", borderWidth = 3)
            drawRect(875, 30, 320, 35, fill = rgb(34,33,51))
            if app.progress > 0:
                drawRect(875, 30, app.progress*320, 35, fill = rgb(173,214,19))

def onStep(app):
    if app.isGrassLevel and not app.grassLevelStarted:
        if app.grassX < 2500 - app.width - 20:
            app.grassX += 20
        else:
            app.isPlantSelectScreen = True
    
    if app.grassLevelStarted and not app.animationDone:
        if app.grassX > 300:
            app.grassX -= 20
        else:
            app.countdown = True
    
    # Countdown to start level
    if app.countdown:
        time.sleep(1)
        if app.number > 0:
            app.number -= 1
        else:
            app.countdown = False
            app.animationDone = True
    
    # Sun randomly spawning in and falling down the screen
    if app.animationDone:
        app.sunSpawnTimer += 10
        if app.sunSpawnTimer > random.randint(750, 1250):
            newSun = Sun()
            app.suns.append(newSun)
            app.sunSpawnTimer = 0
        for sun in app.suns:
            if sun.producedFromFlower == False:
                sun.y += app.sunFallSpeed
                if sun.y > app.height:
                    app.suns.remove(sun)
        
        # Zombies randomly spawning in map and moving while not eating plants
        app.zombieSpawnTimer += 10
        if app.zombieSpawnTimer > random.randint(1500, 2250) and len(app.possibleZombies) > 1:
            choice = random.randint(0, len(app.possibleZombies) - 1)
            newZombie = app.possibleZombies[choice]
            app.possibleZombies.pop(choice)
            app.lanesOccupied[newZombie.lane] += 1
            app.zombies.append(newZombie)
            app.zombieSpawnTimer = 0
        elif app.zombieSpawnTimer > random.randint(1500, 2250) and len(app.possibleZombies) == 1:
            newZombie = app.possibleZombies[0]
            app.possibleZombies.pop(0)
            app.lanesOccupied[newZombie.lane] += 1
            app.zombies.append(newZombie)
            app.zombieSpawnTimer = 0
        for zombie in app.zombies:
            if zombie.notEating: 
                zombie.x -= app.zombieSpeed
            if zombie.x < (app.lawnmowers[zombie.lane].x + 20) or zombie.isDead:
                app.zombies.remove(zombie)
                app.totalZombies -= 1
                app.zombiesKilled += 1
                app.lanesOccupied[zombie.lane] -= 1
                app.progress = app.zombiesKilled / (app.zombiesKilled + app.totalZombies)
        
        # Sunflowers will randomly spawn sun if alive or die if they lose all their health
        for sunflower in app.sunflowers[:]:
            if sunflower.isDead:
                app.sunflowers.remove(sunflower)
            elif not app.levelWon:
                newSun = sunflower.update()
                if newSun:
                    app.suns.append(newSun)
        
        # Win condition
        if app.totalZombies == 0:
            app.levelWon = True
        
        # Plants will start to attack zombies whenever a zombie falls in their lane
        for row in range(5):
            for col in range(9):
                if not isinstance(app.grid[row][col], int) and ((isinstance(app.grid[row][col], Peashooter)) or (isinstance(app.grid[row][col], Iceshooter)) or (isinstance(app.grid[row][col], DoublePeashooter))) and app.lanesOccupied[row] >= 1:
                    app.grid[row][col].update(app.zombies)
                if not isinstance(app.grid[row][col], int) and ((isinstance(app.grid[row][col], Peashooter)) or (isinstance(app.grid[row][col], Iceshooter)) or (isinstance(app.grid[row][col], DoublePeashooter))) and app.lanesOccupied[row] == 0:
                    app.grid[row][col].reset()
                if not isinstance(app.grid[row][col], int) and app.grid[row][col].isDead:
                    app.grid[row][col] = 0

        # Checking if zombie has run into a plant
        # If it does, it will start to eat the plant
        for zombie in app.zombies:
            if 160 <= zombie.x<= 1445:
                x, y = getClosestGridCoor(zombie.x, zombie.y)
                if app.grid[x][y] != 0 and (zombie.x - (zombie.width/2) + 40) <= app.grid[x][y].x:
                    zombie.notEating = False
                    app.grid[x][y].takeDamage(zombie.damage)
                else:
                    zombie.notEating = True

def onMousePress(app, mouseX, mouseY):

    num_selected = len(app.selected_plants)

    # User clicks on 'start playing' button
    if app.isLoadingScreen and 590 <= mouseX <= 990 and 650 <= mouseY <= 770:
        app.click_sound.play()
        app.isLoadingScreen = False
        app.isHomeScreen = True
    
    # User clicks on 'help and options' button
    elif app.isHomeScreen and 80 <= mouseX <= 160 and 630 <= mouseY <= 775:
        app.click_sound.play()
        app.isHelpOptionsScreen = True
    
    elif app.isHelpOptionsScreen and 690 <= mouseX <= 910 and 600 <= mouseY <= 645:
        app.click_sound.play()
        app.isHelpOptionsScreen = False

    # User clicks on "play" button
    elif app.isHomeScreen and not app.isHelpOptionsScreen and ((825 <= mouseX <= 990 and 155 <= mouseY <= 315)
                                                               or (740 <= mouseX <= 825 and 255 <= mouseY <= 335)
                                                               or (1000 <= mouseX <= 1090 and 235 <= mouseY <= 360)
                                                               or (785 <= mouseX <= 835 and 175 <= mouseY <= 255)
                                                               or (745 <= mouseX <= 795 and 230 <= mouseY <= 255)):
        app.click_sound.play()
        app.isLevelSelectorScreen = True
        app.isHomeScreen = False

    # User clicks on back button in level selector screen
    elif app.isLevelSelectorScreen and 85 <= mouseX <= 145 and 20 <= mouseY <= 85:
        app.click_sound.play()
        app.isLevelSelectorScreen = False
        app.isHomeScreen = True

    # User clicks on level 1 (grass level)
    elif app.isLevelSelectorScreen and 375 <= mouseX <= 440 and 375 <= mouseY <= 415:
        app.isLevelSelectorScreen = False
        app.isGrassLevel = True
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

    elif app.isPlantSelectScreen:
        # User clicks on pea shooter plant
        if 45 <= mouseX <= 120 and 180 <= mouseY <= 265:
            app.curr_plant = app.pea_shooter_card
            app.moved_plant = False

        # User clicks on sunflower plant
        elif 130 <= mouseX <= 205 and 180 <= mouseY <= 265:
            app.curr_plant = app.sunflower_card
            app.moved_plant = False
        
        # User clicks on walnut plant
        elif 215 <= mouseX <= 280 and 180 <= mouseY <= 265:
            app.curr_plant = app.walnut_card
            app.moved_plant = False

        # User clicks on double peashooter plant
        elif 300 <= mouseX <= 375 and 180 <= mouseY <= 265:
            app.curr_plant = app.double_pea_shooter_card
            app.moved_plant = False
        
        # User clicks on ice shooter plant
        elif 385 <= mouseX <= 460 and 180 <= mouseY <= 265:
            app.curr_plant = app.ice_shooter_card
            app.moved_plant = False
        
        # User clicks on tallnut plant
        elif 470 <= mouseX <= 545 and 180 <= mouseY <= 265:
            app.curr_plant = app.tallnut_card
            app.moved_plant = False
        
        # User clicks on double sunflower plant
        elif 555 <= mouseX <= 630 and 180 <= mouseY <= 265:
            app.curr_plant = app.double_sunflower_card
            app.moved_plant = False
        
        # User places selected plant in row
        elif app.curr_plant != None and 134 <= mouseX <= 711 and 20 <= mouseY <= 115:
            num_plants = len(app.selected_plants)
            if app.curr_plant not in app.selected_plants and num_plants < 6:
                app.moved_plant = True
                app.selected_plants.append(app.curr_plant)    

        # User clicks on first selected card
        if 145 <= mouseX <= 223 and 22 <=  mouseY <= 93 and num_selected >= 1:
            app.selected_delete_card = app.selected_plants[0]
        
        # User clicks on second selected card
        if 240 <= mouseX <= 318 and 22 <=  mouseY <= 93 and num_selected >= 2:
            app.selected_delete_card = app.selected_plants[1]

        # User clicks on third selected card
        if 335 <= mouseX <= 413 and 22 <=  mouseY <= 93 and num_selected >= 3:
            app.selected_delete_card = app.selected_plants[2]

        # User clicks on fourth selected card
        if 430 <= mouseX <= 508 and 22 <=  mouseY <= 93 and num_selected >= 4:
            app.selected_delete_card = app.selected_plants[3]

        # User clicks on fifth selected card
        if 525 <= mouseX <= 603 and 22 <=  mouseY <= 93 and num_selected >= 5:
            app.selected_delete_card = app.selected_plants[4]

        # User clicks on sixth selected card
        if 620 <= mouseX <= 698 and 22 <=  mouseY <= 93 and num_selected == 6:
            app.selected_delete_card = app.selected_plants[5]

        # User trashes card
        if 740 <= mouseX <= 845 and 15 <= mouseY <= 120 and app.selected_delete_card != None:
            app.selected_plants.remove(app.selected_delete_card)
            app.selected_delete_card = None

        # User selects 'let's rock' button
        if 260 <= mouseX <= 505 and 730 <= mouseY <= 780:
            app.grassLevelStarted = True
            app.isPlantSelectScreen = False

    # User clicks on one of the plant cards on the top of the screen
    elif app.grassLevelStarted and 10 <= mouseY <= 90 and 133 <= mouseX <= 675:
        if 133 <= mouseX <= 208:
            app.card_selected = app.selected_plants[0]
        elif 226 <= mouseX <= 301:
            app.card_selected = app.selected_plants[1]
        elif 321 <= mouseX <= 396:
            app.card_selected = app.selected_plants[2]
        elif 414 <= mouseX <= 489:
            app.card_selected = app.selected_plants[3]
        elif 506 <= mouseX <= 581:
            app.card_selected = app.selected_plants[4]
        else:
            app.card_selected = app.selected_plants[5]
    
    # User clicks on shovel
    elif app.grassLevelStarted and 710 <= mouseX <= 810 and 10 <= mouseY <= 100:
        app.shovel_activated = True

    # User attempts to place the plant on the lawn
    # If they do not have enough sun, the card is unselected
    # Otherwise, the plant is placed and the user loses the sun cost for that plant
    elif app.grassLevelStarted and 160 <= mouseX <= 1445 and 110 <= mouseY <= 780 and app.card_selected:
        app.gridX, app.gridY = getClosestGridCoor(mouseX, mouseY)
        if isinstance(app.grid[app.gridX][app.gridY], int):
            test = postPlant(app.card_selected, 0, 0)
            if test.cost <= app.sun_count:
                curr_plant = postPlant(app.card_selected, app.gridX, app.gridY)
                app.grid[app.gridX][app.gridY] = curr_plant
                if isinstance(curr_plant, Sunflower):
                    app.sunflowers.append(curr_plant)
                app.card_selected = None
                app.sun_count -= test.cost
        else:
            app.card_selected = None
    
    # User attempts to shovel plant away
    elif app.grassLevelStarted and 160 <= mouseX <= 1445 and 110 <= mouseY <= 780 and app.shovel_activated:
        app.gridX, app.gridY = getClosestGridCoor(mouseX, mouseY)
        if not isinstance(app.grid[app.gridX][app.gridY], int):
            curr_plant = app.grid[app.gridX][app.gridY]
            cost_curr_plant = curr_plant.cost
            app.grid[app.gridX][app.gridY] = 0
            if isinstance(curr_plant, Sunflower):
                app.sunflowers.remove(curr_plant)
            app.sun_count += cost_curr_plant
            app.shovel_activated = None
        else:
            app.shovel_activated = None

    # User clicks on sun and collects 25 sun points
    elif app.animationDone:
        for sun in app.suns:
            if (mouseX-sun.x)**2 + (mouseY-sun.y)**2 <= sun.radius**2:
                app.suns.remove(sun)
                app.sun_count += 25

    print(mouseX, mouseY)

# User adjusts volume
def onMouseDrag(app, mouseX, mouseY):
    if (app.slider1OuterCoor[5][0] <= mouseX <= app.slider1OuterCoor[2][0]) and (app.slider1OuterCoor[0][1] <= mouseY <= app.slider1OuterCoor[4][1]):
        if 870 <= mouseX <= 1128:
            change = mouseX - app.slider1InnerCoor[0][0]
            for i in range(0, 6):
                app.slider1OuterCoor[i][0] += change
            for i in range(0, 4):
                app.slider1InnerCoor[i][0] += change
            total_range = 1128 - 870
            percent_volume = (mouseX - 870) / total_range
            app.background_music.set_volume(percent_volume)
    
    elif (app.slider2OuterCoor[5][0] <= mouseX <= app.slider2OuterCoor[2][0]) and (app.slider2OuterCoor[0][1] <= mouseY <= app.slider2OuterCoor[4][1]):
        if 870 <= mouseX <= 1128:
            change = mouseX - app.slider2InnerCoor[0][0]
            for i in range(0, 7):
                app.slider2OuterCoor[i][0] += change
            for i in range(0, 5):
                app.slider2InnerCoor[i][0] += change
            total_range = 1128 - 870
            percent_volume = (mouseX - 870) / total_range
            app.click_sound.set_volume(percent_volume)

def main():
    runApp()

main()