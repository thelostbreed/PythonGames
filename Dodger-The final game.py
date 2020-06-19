import pygame, random, sys
from pygame import font
from pygame.locals import *

WINDOWWIDTH = 600
WINDOWHEIGHT = 600
TEXTCOLOR = (255, 255, 255)
BACKGROUNDCOLOR = (0, 0, 0)
FPS = 40
BADIEMINSIZE = 10
BADIEMAXSIZE = 40
BADIEMINSPEED = 1
BADIEMAXSPEED = 8
ADDNEWBADDIERATE = 5
PLAYERMOVERATE = 5


# function to terminate the program
def terminate():
    pygame.quit()
    sys.exit()


# function when player press a key
def waitForPlayerToPressKey():
    while True:  # while game is playing
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()  # call to terminate function
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()
                return


# function when player collides
# 2 args playerRect is the image area of the player and baddies are the boys
# to which player collides , the baddie parameter is the list of "baddie" dictionary data structure.
def playerHasHitTheBaddie(playerRect, baddies):
    for b in baddies:
        if playerRect.colliderect(b['rect']):  # if player collides with the one of the baddies
            return True
    return False


# drawing text on the window
def drawText(text, font, surface, x, y):
    # render method will create a Surface object that has the text rendered in a specific font on it
    textObj = font.render(text, 1, TEXTCOLOR)
    # to know the size and location of the surface object, you can get this info from get.rect() Surface method
    # textRect has the copy of width and height information from the Surface object
    textRect = textObj.get_rect()
    # line 54 changes the location of the Rect object by setting up a new tuple with topleft attribute
    textRect.topleft = (x, y)
    # blit() the rendered text on the surface object
    surface.blit(textObj, textRect)


# set up pygame, the window and the mouse cursor
pygame.init()
mainClock = pygame.time.Clock()
# only 1 argument will be passed in display.set_mode
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption("Dodger Game")
# cursor will not visible
pygame.mouse.set_visible(False)

# set up fonts
font = pygame.font.Font(None, 48)

# set up sounds
gameOverSound = pygame.mixer.Sound('gameover.wav') # mixer.Sound plays the sound for a short time
pygame.mixer.music.load('background.mid') # mixer.music.load plays the sound forever

# setup images
playerImage = pygame.image.load('girl.jpg')
playerRect = playerImage.get_rect()
baddieImage = pygame.image.load('boy.png')

# show the start screen
# drawText function will pass five 5 arguments
drawText('Dodger', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
drawText('Press a key to start', font, windowSurface, (WINDOWWIDTH / 3) - 30, (WINDOWHEIGHT / 3) + 50)
pygame.display.update()
# waitForPlayerToPressKey() will pause the game until a key is pressed
waitForPlayerToPressKey()

# value of top score will start from 0 when the program starts
# whenever the player loses and has a score larger than current top score, the top score is replaces with larger score
topScore = 0
# this while loops will iterate whenever the game starts
while True:
    # set up start of the game
    baddies = [] # set baddies as an empty list, baddies variable is a list of dict objects with 3 keys :
                    # rect , speed , surface
    score = 0
    # the starting location of the player will be at the center and 50 pixel up from the bottom
    playerRect.topleft = (WINDOWWIDTH / 2, WINDOWHEIGHT - 50)
    moveLeft = moveRight = moveUp = moveDown = False
    reverseCheat = slowCheat = False
    baddieAddCounter = 0
    pygame.mixer.music.play(-1, 0.0)

    while True:  # game loop will run while the game part is playing
        score += 1
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

            if event.type == KEYDOWN:
                if event.key == ord('z'):
                    reverseCheat = True
                if event.key == ord('x'):
                    slowCheat = True
                if event.key == K_LEFT or event.key == ord('a'):
                    moveRight = False
                    moveLeft = True
                if event.key == K_RIGHT or event.key == ord('d'):
                    moveRight = True
                    moveLeft = False
                if event.key == K_UP or event.key == ord('w'):
                    moveDown = False
                    moveUp = True
                if event.key == K_DOWN or event.key == ord('s'):
                    moveDown = True
                    moveUp = False

            if event.type == KEYUP:
                if event.key == ord('z'):
                    reverseCheat = False
                    score = 0
                if event.key == ord('x'):
                    slowCheat = False
                    score = 0
                if event.key == K_ESCAPE:
                    terminate()

                if event.key == K_LEFT or event.key == ord('a'):
                    moveLeft = False
                if event.key == K_RIGHT or event.key == ord('d'):
                    moveRight = False
                if event.key == K_UP or event.key == ord('w'):
                    moveUp = False
                if event.key == K_DOWN or event.key == ord('s'):
                    moveDown = False

            if event.type == MOUSEMOTION:  # if the mouse moves , move the player where the cursor is
                # the position attrbute stores a tuple of x, y coordinates of where the mouse cursor moved in the window
                playerRect.centerx = event.pos[0]
                playerRect.centery = event.pos[1]
                # ip in move_ip stands for in_place
                # playerRect.move_ip(event.pos[0] - playerRect.centerx, event.pos[1] - playerRect.centery)

        # add new baddies at the top of the screen, if needed
        if not reverseCheat and not slowCheat:
            baddieAddCounter += 1
        if baddieAddCounter == ADDNEWBADDIERATE:
            baddieAddCounter = 0
            baddieSize = random.randint(BADIEMINSIZE, BADIEMAXSIZE)
            newBaddie = {'rect': pygame.Rect(random.randint(0, WINDOWWIDTH - baddieSize), 0 - baddieSize, baddieSize,
                                             baddieSize),
                         'speed': random.randint(BADIEMINSPEED, BADIEMAXSPEED),
                         'surface': pygame.transform.scale(baddieImage, (baddieSize, baddieSize)), }
            baddies.append(newBaddie)

        # move the player around
        # if the player's character is moving left and left edge of the player's character is greater than 0
        # (which is the left edge of the window), then playerRect should be move left
        if moveLeft and playerRect.left > 0:
            # you will always move the playerRect object by the number of pixel in PLAYERMOVERATE. To get the
            # negetive form of an integer , multiply it by -1
            # so move_ip(-1 * playermoverate ) will move the location of playerRect object to the left
            playerRect.move_ip(-1 * PLAYERMOVERATE, 0)
        if moveRight and playerRect.right < WINDOWWIDTH:
            playerRect.move_ip(PLAYERMOVERATE, 0)
        if moveUp and playerRect.top > 0:
            playerRect.move_ip(0, -1 * PLAYERMOVERATE)
        if moveDown and playerRect.bottom < WINDOWHEIGHT:
            playerRect.move_ip(0, PLAYERMOVERATE)

        # move the mouse cursor to match the player
        # it will set the mouse cursor at the player character position, so that the mouse and the player are always
        # at the same place.
        pygame.mouse.set_pos(playerRect.centerx, playerRect.centery)

        # move the baddies down
        for b in baddies:
            # if both the cheats are nto activated then bring baddie's location down to a number of pixels equal to
            # its speed, which is stored in 'speed' key
            if not reverseCheat and not slowCheat:
                b['rect'].move_ip(0, b['speed'])
            elif reverseCheat:
                b['rect'].move_ip(0, -5)
            elif slowCheat:
                b['rect'].move_ip(0, 1)

        # delete the baddies that have fallen past the bottom
        for b in baddies[:]:
            # b is the current baddie data structure from baddies[:] list
            # each baddie data structure in the list is a dict with the 'rect' key, which stores a Rect object
            # so b['rect'] is the rect object for the baddie
            # top attribute is the Y coordinate of the top edge of the rectangular area.

            if b['rect'].top > WINDOWHEIGHT: # so this will check if the top edge of the baddie if=s below the bottom
                                            # of the window
                baddies.remove(b)

        # draw the game world on the window
        windowSurface.fill(BACKGROUNDCOLOR)

        # draw the score and the top score
        drawText('Score : %s' % score, font, windowSurface, 10, 10)
        drawText('Top Score : %s' % topScore, font, windowSurface, 10, 40)

        # draw player's rectangle
        # playerImage is the surface Object that contains all colored pixels that make up the players character image
        # playerRect is the Rect object that stores the information about the size and loc of player's character
        windowSurface.blit(playerImage, playerRect)

        # draw each baddie
        for b in baddies:
            # the blit() method will create the char image on windowSurface at player's character
            windowSurface.blit(b['surface'], b['rect'])

        pygame.display.update()

        # check if any of thr baddie has hit the player
        if playerHasHitTheBaddie(playerRect, baddies):
            if score > topScore:
                topScore = score
            break

        mainClock.tick(FPS)

    pygame.mixer.music.stop()
    gameOverSound.play()

    drawText('Game Over', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
    drawText('Press a key to play again: ', font, windowSurface, (WINDOWWIDTH / 3) - 80, (WINDOWHEIGHT / 3) + 50)
    pygame.display.update()
    waitForPlayerToPressKey()

    gameOverSound.stop()
