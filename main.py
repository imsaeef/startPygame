import pygame
import os
pygame.font.init()
pygame.mixer.init()

#set window size
WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

#set title of the window
pygame.display.set_caption("myFirst Game!")

#------ variables ---------

#color
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
#border control
BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join("Assets", "Grenade+1.mp3"))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join("Assets", "Gun+Silencer.mp3"))

HEALTH_FONT = pygame.font.SysFont("comicsans", 40)
WINNER_FONT = pygame.font.SysFont("comicsans", 100)

#control speed
FPS = 60

#velocity
VEL = 5
BULLETS_VEL = 7
MAX_BULLETS = 10

SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

#---------------------------

#import img
YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join("Assets", "spaceship_yellow.png"))
#rotate yellow spaceship for 90 degree
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)
#import img
RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join("Assets", "spaceship_red.png"))
#rotate red spaceship for 270 degree
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)

SPACE = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "space.png")), (WIDTH, HEIGHT))

# draw window
def drawWindow(red, yellow, redBullets, yellowBullets, redHealth, yellowHealth):
    #set window color
    # WIN.fill(WHITE)
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)

    redHealthText = HEALTH_FONT.render("Health: " + str(redHealth), 1, WHITE)
    yellowHealthText = HEALTH_FONT.render("Health: " + str(yellowHealth), 1, WHITE)
    WIN.blit(redHealthText, (WIDTH - redHealthText.get_width() - 10, 10))
    WIN.blit(yellowHealthText, (10, 10))

    #yellow spaceship
    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    #red spaceship
    WIN.blit(RED_SPACESHIP, (red.x, red.y))

    for bullet in redBullets:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in yellowBullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    pygame.display.update()

#yellow object movement
def yellowHandleMovement(keysPressed, yellow):
    #moving yello
    if keysPressed[pygame.K_a] and yellow.x - VEL > 0: #left
        yellow.x -= VEL
    if keysPressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x + 15: #right
        yellow.x += VEL
    if keysPressed[pygame.K_w] and yellow.y - VEL > 0: #up
        yellow.y -= VEL
    if keysPressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT - 15:  #down
        yellow.y += VEL


#red object movement
def redHandleMovement(keysPressed, red):
    #moving red
    if keysPressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width: #left
        red.x -= VEL
    if keysPressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH + 15: #right
        red.x += VEL
    if keysPressed[pygame.K_UP] and red.y - VEL > 0: #up
        red.y -= VEL
    if keysPressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT - 15: #down
        red.y += VEL

# handle bullets left and right
def handleBullets(yellowBullets, redBullets, yellow, red):

    #red bullets
    for bullet in yellowBullets:
        bullet.x += BULLETS_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellowBullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellowBullets.remove(bullet)

    #yellow bullets
    for bullet in redBullets:
        bullet.x -= BULLETS_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            redBullets.remove(bullet)
        elif bullet.x < 0:
            redBullets.remove(bullet)

def drawWinner(text):
    drawText = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(drawText, (WIDTH/2 - drawText.get_width()/2, HEIGHT/2 - drawText.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)


#start game function
def main():
    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    redBullets = []
    yellowBullets = []

    #health
    redHealth = 10
    yellowHealth = 10

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellowBullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)
                    yellowBullets.append(bullet)
                    #sound
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_RCTRL and len(redBullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x, red.y + red.height//2 - 2, 10, 5)
                    redBullets.append(bullet)
                    #sound
                    BULLET_FIRE_SOUND.play()
        

            if event.type == RED_HIT:
                redHealth -= 1
                #sound
                BULLET_HIT_SOUND.play()


            if event.type == YELLOW_HIT:
                yellowHealth -= 1
                #sound
                BULLET_HIT_SOUND.play()

        winnerText = ""
        if redHealth <= 0:
            winnerText = "Yellow wins!"

        if yellowHealth <= 0:
            winnerText = "Red wins!"

        if winnerText != "":
            drawWinner(winnerText)
            break

        keysPressed = pygame.key.get_pressed()
        yellowHandleMovement(keysPressed, yellow)
        redHandleMovement(keysPressed, red)


        handleBullets(yellowBullets, redBullets, yellow, red)
        drawWindow(red, yellow, redBullets, yellowBullets, redHealth, yellowHealth)

    main()


if __name__=="__main__":
    main()