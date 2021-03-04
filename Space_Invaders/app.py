import pygame
import random
import math
from pygame import mixer

# work to using all modules
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600))
# adding an game icon
icon = pygame.image.load("spaceship.png")
pygame.display.set_icon(icon)

running = True

# title and icon
pygame.display.set_caption("Space Invaders")

# player
playerImage = pygame.image.load("rocket.png")
# resize image
playerImage = pygame.transform.scale(playerImage, (50, 50))

playerX = 370
playerY = 480
playerX_change = 0

# background
backgroundImage = pygame.image.load("background.jpg")
backgroundImage = pygame.transform.scale(backgroundImage, (800, 600))

# adding background sound
mixer.music.load("back_music.mp3")
mixer.music.play(-1)

# bullet
bulletImage = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 1
# cant see it..but it keep ready
bullet_state = "ready"

enemyImage = []
enemyX = []
enemyY = [random.randint(50, 150)]
# invader position update
enemyX_change =[]
enemyY_change =[]

num_of_enemies = 6

for i in range(num_of_enemies):

    # enemy
    enemyImage.append(pygame.image.load("enemy.png"))
    # resize image
    # enemyImage = pygame.transform.scale(enemyImage, (50, 50))

    enemyX.append(random.randint(0, 800))
    enemyY.append(random.randint(50, 150))
    # invader position update
    enemyX_change.append(0.3)
    enemyY_change.append(10)


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImage, (x + 16, y + 10))


def isCollision(x, y, x1, y1):
    distance = (math.sqrt(math.pow(x - x1, 2)) + (math.pow(y - y1, 2)))
    if distance < 27:
        return True
    else:
        return False


# score
score_value = 0
font = pygame.font.Font('freesansbold.ttf',32)

textX = 10
textY = 10

def score_show(x,y):
    global score_value
    score = font.render("Score : "+ str(score_value),True,(0,255,0))
    screen.blit(score, (x, y))

def game_over_text():
    global game_over
    game_over = font.render("GAME OVER",True,(0,255,0))
    screen.blit(game_over, (250, 250))


def player(x, y):
    # draw it on screen
    screen.blit(playerImage, (x, y))


def enemy(x, y, i2):
    # draw it on screen
    screen.blit(enemyImage[i], (x, y))


# game Loop
while running:

    # background color
    screen.fill((0, 0, 0))

    # load background image
    screen.blit(backgroundImage, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # controlling the player
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = - 0.6

            if event.key == pygame.K_RIGHT:
                playerX_change = 0.6

            if event.key == pygame.K_SPACE:
                # to make only fire one bullet per once
                if bullet_state is "ready":
                    bullet_sound = mixer.Sound("gun.mp3")
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, playerY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change

    # setting border to player
    if playerX <= 0:
        playerX = 0

    elif playerX >= 750:
        playerX = 750

    # set boundaries to enemy
    enemyX += enemyX_change

    for i in range(num_of_enemies):
        # game over
        if enemyY[i] > 600:
            for j in range(num_of_enemies):
                enemyY[j] = 2000

            # game_over_text()
            # break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.3
            # moving enemy down
            enemyY[i] += enemyY_change[i]

        elif enemyX[i] >= 750:
            enemyX_change[i] = -0.3
            enemyY[i] += enemyY_change[i]

        # collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            bulletY = 480
            bullet_state = "ready"
            # increase score
            score_value += 1
            # respawn enemy
            enemyX[i] = random.randint(0, 800)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change



    # calling methods
    player(playerX, playerY)
    # show your score
    score_show(textX,textY)

    pygame.display.update()
