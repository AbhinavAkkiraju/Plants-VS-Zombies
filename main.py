from cmu_graphics import *
from pathlib import Path
import pygame

script_dir = Path(__file__).resolve().parent
media_dir = script_dir / "media"

pygame.mixer.init()

def onAppStart(app):
    # Setting screen size to 1920x1080 (default)
    app.width = 1920
    app.height = 1080

    # Loading screen
    app.url_loading_background = str(media_dir / "loading_screen.png")
    app.url_title = str(media_dir / "title_header.png")
    app.url_loading = str(media_dir / "loading_bar.png")
    app.background_music = pygame.mixer.Sound(str(media_dir / "music.mp3"))
    app.background_music.play(-1)
    app.isLoadingScreen = True
    app.click_sound = pygame.mixer.Sound(str(media_dir / "click_sound.mp3"))

    # Selector screen 
    app.isHomeScreen = False
    app.url_home_background = str(media_dir / "selector_screen.png")

    # Help and options screen
    app.isHelpOptionsScreen = False
    app.url_help_box = str(media_dir / "help_options_screen.png")
    app.coverUnwantedColor = rgb(26,28,41)
    app.lineColor = rgb(139, 159, 169)
    app.outsideDragger = rgb(137, 138, 182)
    app.insideDragger = rgb(76, 78, 93)
    app.slider1OuterCoor = [[1000, 320], [1003, 321], [1017, 354], [1009, 365], [993, 366], [984, 356]]
    app.slider1InnerCoor = [[1000, 333], [1006, 341], [1002, 359], [993, 356]]
    app.slider2OuterCoor = [[998, 378], [1004, 378], [1018, 410], [1009, 422], [993, 423], [983, 409], [986, 403]]
    app.slider2InnerCoor = [[1000, 390], [1005, 397], [1008, 410], [998, 416], [993, 413]]

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

def onMousePress(app, mouseX, mouseY):
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
    
    # print(mouseX, mouseY)

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