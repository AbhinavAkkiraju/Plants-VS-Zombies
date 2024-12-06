from cmu_graphics import *
from pathlib import Path
import random
from level_objects import Lawnmower, PlantCard, Sun
from plant_objects import postPlant, Sunflower, Peashooter, DoublePeashooter, Iceshooter
from level_one_variables import level_one_variables
from get_grid_coor import getClosestGridCoor, getClosestSelectGridCoor, getSelectedCard
from on_app_start import onAppStart
import time

onAppStart(app)

def redrawAll(app):
    if app.isLoadingScreen:
        drawImage(app.url_loading_background, 0, 0, width = app.width, height = app.height)
        drawImage(app.url_title, app.title_left_space, app.title_top_space, width = app.title_width, height = app.title_height)
        drawImage(app.url_loading, app.loading_left_space, app.loading_top_space, width = app.loading_width, height = app.loading_height)
    
    elif app.isHomeScreen:
        drawImage(app.url_home_background, 0, 0, width = app.width, height = app.height)
    
    elif app.isLevelSelectorScreen:
        drawImage(app.level_selector_screen_background, 0, 0, width = app.width, height = app.height)
        # drawLabel('BYOL', 1223, 337, size = 20, font = 'grenze', fill = 'white')
    
    if app.isLevelOne:
        drawImage(app.grass_background, 0 - app.grassX, 0, width = app.background_width, height = app.height)
        if app.isPlantSelectScreen:
            drawImage(app.plant_select_background, 0, app.select_left, width = app.select_width, height = app.height)
            drawRect(app.select_cover_left, app.select_cover_top, app.select_cover_width, app.select_cover_height, fill = app.select_cover_color)

            left = 27
            top = 122
            for plant in app.all_plants:
                if left == (27 + (53*7)):
                    top += 66
                    left = 27
                drawImage(plant, left, top, width = 47, height = 59)
                left += 53

            top = 17
            width = 50
            height = 61
            for i, plant in enumerate(app.selected_plants):
                left = 89 + (57 * i)           
                drawImage(plant, left, top, width = width, height = height)
            
            drawCircle(app.circle_x, app.circle_y, app.circle_radius, fill = app.circle_fill, border = app.circle_border)
            drawImage(app.delete_plant, app.trash_x, app.trash_y, width = app.trash_width, height = app.trash_height)

        if app.countdown:
            drawLabel(app.number, app.width/2, app.height/2, size=100)

        if app.levelWon:
            drawLabel("YOU WIN!", app.width/2, app.height/2, size=100)

        if app.levelStarted and app.animationDone:
            for i in range(1, 6):
                app.lawnmowers[i-1] = Lawnmower(i)
            drawImage(app.plants_top_bar, 0, 0, width = 400, height = 70)
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
    if app.isLevelOne and not app.levelStarted:
        if app.grassX < app.background_width - app.width - 20:
            app.grassX += 20
        else:
            app.isPlantSelectScreen = True
    
    if app.levelStarted and not app.animationDone:
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
                if zombie.isSlowed: 
                    zombie.x -= (app.zombieSpeed/1.5)
                else: 
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

    # User clicks on 'click to start' button
    if app.isLoadingScreen and 350 <= mouseX <= 600 and 445 <= mouseY <= 490:
        app.isLoadingScreen = False
        app.isHomeScreen = True

    # User clicks on "play" button
    elif app.isHomeScreen and ((525 <= mouseX <= 635 and 105 <= mouseY <= 210)
                            or (470 <= mouseX <= 700 and 175 <= mouseY <= 215)):
        app.isLevelSelectorScreen = True
        app.isHomeScreen = False

    # User clicks on back button in level selector screen
    elif app.isLevelSelectorScreen and 55 <= mouseX <= 95 and 15 <= mouseY <= 60:
        app.isLevelSelectorScreen = False
        app.isHomeScreen = True

    # User clicks on level 1
    elif app.isLevelSelectorScreen and 240 <= mouseX <= 280 and 240 <= mouseY <= 270:
        app.isLevelSelectorScreen = False
        level_one_variables(app)
        app.isLevelOne = True

    elif app.isPlantSelectScreen:
        # User selects card
        if 27 <= mouseX <= 440 and 123 <= mouseY <= 435:
            selected_x, selected_y = getClosestSelectGridCoor(mouseX, mouseY)
            app.curr_plant = app.select_grid[selected_x][selected_y]
            app.moved_plant = False
        
        # User places selected plant in row
        if app.curr_plant and app.select_cover_left <= mouseX <= app.select_cover_left + app.select_cover_width and app.select_cover_top <= mouseY <= app.select_cover_top + app.select_cover_height:
            num_plants = len(app.selected_plants)
            if app.curr_plant not in app.selected_plants and num_plants < 6:
                app.moved_plant = True
                app.selected_plants.append(app.curr_plant)    

        # User clicks on already selected card
        if 87 <= mouseX <= 427 and 18 <= mouseY <= 79:
            if len(app.selected_plants) == 0: pass
            else:
                index = getSelectedCard(mouseX)
                app.selected_delete_card = app.selected_plants[index]

        # User trashes the selected card
        if 472 <= mouseX <= 544 and 18 <= mouseY <= 83 and app.selected_delete_card != None:
            app.selected_plants.remove(app.selected_delete_card)
            app.selected_delete_card = None

        # User selects 'let's rock' button
        if 160 <= mouseX <= 310 and 483 <= mouseY <= 515:
            app.levelStarted = True
            app.isPlantSelectScreen = False

    # User clicks on one of the plant cards on the top of the screen
    elif app.levelStarted and 10 <= mouseY <= 90 and 133 <= mouseX <= 675:
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
    elif app.levelStarted and 710 <= mouseX <= 810 and 10 <= mouseY <= 100:
        app.shovel_activated = True

    # User attempts to place the plant on the lawn
    # If they do not have enough sun, the card is unselected
    # Otherwise, the plant is placed and the user loses the sun cost for that plant
    elif app.levelStarted and 160 <= mouseX <= 1445 and 110 <= mouseY <= 780 and app.card_selected:
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
    elif app.levelStarted and 160 <= mouseX <= 1445 and 110 <= mouseY <= 780 and app.shovel_activated:
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

def main():
    runApp()

main()