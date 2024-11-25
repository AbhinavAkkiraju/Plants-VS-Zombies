from cmu_graphics import *

def onAppStart(app):
    # Setting screen size to 1920x1080 (default)
    app.width = 1920
    app.height = 1080

    # Loading screen
    app.url_loading_background = r"C:\Users\abhin\OneDrive\Documents\GitHub\Plants-VS-Zombies\media\loading_screen.png"
    app.url_title = r"C:\Users\abhin\OneDrive\Documents\GitHub\Plants-VS-Zombies\media\title_header.png"
    app.url_loading = r"C:\Users\abhin\OneDrive\Documents\GitHub\Plants-VS-Zombies\media\loading_bar.png"
    app.sound = Sound(r"C:\Users\abhin\OneDrive\Documents\GitHub\Plants-VS-Zombies\media\music.mp3")
    app.sound.play(loop = True)
    app.isLoadingScreen = True

    # Selector screen 
    app.isHomeScreen = False
    app.url_home_background = r"C:\Users\abhin\OneDrive\Documents\GitHub\Plants-VS-Zombies\media\selector_screen.png"

    # Help and options screen
    app.isHelpOptionsScreen = False
    # app.url_help_box = urllib.requires.pathname2url("C:\Users\abhin\OneDrive\Documents\GitHub\Plants-VS-Zombies\media\help_options_screen.png")
    app.url_help_box = r"C:\Users\abhin\OneDrive\Documents\GitHub\Plants-VS-Zombies\media\help_options_screen.png"
    app.coverUnwantedColor = rgb(26,28,41)

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

def onMousePress(app, mouseX, mouseY):

    # User clicks on 'start playing' button
    if app.isLoadingScreen and 590 <= mouseX <= 990 and 650 <= mouseY <= 770:
        app.isLoadingScreen = False
        app.isHomeScreen = True
    
    # User clicks on 'help and options' button
    elif app.isHomeScreen and 80 <= mouseX <= 160 and 630 <= mouseY <= 775:
        app.isHelpOptionsScreen = True
    
    elif app.isHelpOptionsScreen and 690 <= mouseX <= 910 and 600 <= mouseY <= 645:
        app.isHelpOptionsScreen = False
    
    print(mouseX, mouseY)

def main():
    runApp()

main()