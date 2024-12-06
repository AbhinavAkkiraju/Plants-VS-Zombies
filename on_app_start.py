from cmu_graphics import *
from pathlib import Path

script_dir = Path(__file__).resolve().parent
media_dir = script_dir / "media"
screens_dir = media_dir / "screens"
sounds_dir = media_dir / "sounds"
plants_dir = media_dir / "plants"
level_objects_dir = media_dir / "level_objects"

def onAppStart(app):

    # Setting screen size to 960x540
    app.width = 960
    app.height = 540

    # Loading screen
    app.url_loading_background = str(screens_dir / "loading_screen.png") # https://www.spriters-resource.com/mobile/plantsvszombies/sheet/206074/
    app.url_title = str(screens_dir / "title_header.png") # https://www.amazon.com/Plants-vs-Zombies-1-Lawnmageddon/dp/1616551925 
    app.url_loading = str(screens_dir / "loading_bar.png") # https://www.alamy.com/stock-photo-plants-vs-zombies-pc-game-loading-screen-38615868.html 
    app.isLoadingScreen = True
    app.title_width = 500
    app.title_height = 115
    app.title_top_space = 15
    app.title_left_space = app.width/2 - app.title_width/2
    app.loading_width = 270
    app.loading_height = 80
    app.loading_top_space = 420
    app.loading_left_space = app.width/2 - app.loading_width/2

    # Selector screen 
    app.isHomeScreen = False
    app.url_home_background = str(screens_dir / "selector_screen.png") # Screenshot from my iPhone - Plants VS Zombies 1 Application

    # Level selector screen
    app.isLevelSelectorScreen = False
    app.level_selector_screen_background = str(screens_dir / "level_selector_screen.png") # Screenshot from my iPhone - Plants VS Zombies 1 Application

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

    # Level objects and variables
    app.isLevelOne = False
    app.levelStarted = False
    app.static_background = None
    app.grass_background = str(screens_dir / "front_yard_grass.png") # https://www.reddit.com/r/PlantsVSZombies/comments/vqqhjs/i_made_pvz_evening_enjoy/
    app.lawnmowers = {"lawnmower1":[], "lawnmower2":[], "lawnmower3":[], "lawnmower4":[], "lawnmower5":[]}
    app.topbar = {'plant1':[], 'plant2':[], 'plant3':[], 'plant4':[], 'plant5':[], 'plant6':[]}
    app.sun = str(level_objects_dir / "sun.png") # https://heroism.fandom.com/wiki/Sun_(Plants_vs._Zombies)
    app.sun_count = 50
    app.plants_top_bar = str(screens_dir / "plants_top_bar.png") # https://plantsvszombies.fandom.com/wiki/Ice_Level
    app.shovel = str(level_objects_dir / "shovel.png") # https://plantsvszombies.fandom.com/wiki/Ice_Level
    app.grid = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0]]
    app.select_grid = [[app.pea_shooter_card, app.sunflower_card, app.walnut_card, app.double_pea_shooter_card, app.ice_shooter_card, app.tallnut_card, app.double_sunflower_card, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0]]
    app.card_selected = None
    app.gridX = app.gridY = 0
    app.suns = []
    app.sunFallSpeed = 3
    app.sunSpawnTimer = 0
    app.zombieSpeed = 2.5
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
    app.background_drawn = False
    app.static_background = []

    # Animation for grass level to move from left to right for plant select screen
    app.stepsPerSecond = 60
    app.background_width = 2100
    app.grassX = 0

    # Plant select screen
    app.isPlantSelectScreen = False
    app.plant_select_background = str(screens_dir / "plant_select_screen.png") # https://www.solitairelaboratory.com/solitairearcade/zombies/plantsvszombiesguide.html
    app.selected_plants = []
    app.curr_plant = None
    app.moved_plant = False
    app.delete_plant = str(level_objects_dir / 'trash.png') # https://pvzcc.fandom.com/wiki/Stealthy_Imp_(PvZ2)
    app.selected_delete_card = None
    app.animationDone = False
    app.countdown = False
    app.number = 4
    app.progress = 0
    app.countdownDone = False
    app.levelWon = False
    app.starterCalled = False
    app.loadingScreenDrawn = False
    app.select_left = -10
    app.select_width = 800
    app.select_cover_left = 80
    app.select_cover_top = 15
    app.select_cover_width = 360
    app.select_cover_height = 63
    app.select_cover_color = rgb(99,47,23)
    app.circle_x = 510
    app.circle_y = 50
    app.circle_radius = 35
    app.circle_fill = rgb(146,147,143)
    app.circle_border = rgb(74,73,75)
    app.trash_x = 490
    app.trash_y = 28
    app.trash_width = 50
    app.trash_height = 50

    