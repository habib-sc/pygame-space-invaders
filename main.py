import pygame
import random
import math
from pygame import mixer

# initialize pygame
pygame.init()

# create screen
screen = pygame.display.set_mode((800, 600))

# background
background = pygame.image.load("img/bg-image.png")

# background music
# mixer.music.load("bg-audio.mp3")
# mixer.music.play(-1)

# title & icon
pygame.display.set_caption("Space Invader")
icon = pygame.image.load("img/fav-icon.png")
pygame.display.set_icon(icon)

# player
playerImage = pygame.image.load("img/battleship.png")
playerX = 370
playerY = 480
playerChangeX = 0

# enemy
enemyImage = []
enemyX = []
enemyY = []
enemyChangeX = []
enemyChangeY = []
totalEnemy = 5
for e in range(totalEnemy):
    enemyImage.append(pygame.image.load("img/alienship.png"))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 120))
    enemyChangeX.append(2.5)
    enemyChangeY.append(30)

# bullet
# bulletState(ready) -- Can't see the bullet on the screen.
# bulletState(fire) -- Bullet is moving
bulletImage = pygame.image.load("img/bullet.png")
bulletX = 0
bulletY = 480
bulletChangeX = 0
bulletChangeY = 20
bulletState = "ready"

# score
scoreValue = 0
font = pygame.font.Font('freesansbold.ttf', 34)
textX = 5
textY = 5

# game over text
gameOverFont = pygame.font.Font('freesansbold.ttf', 64)

# guide
guideFont = pygame.font.Font('freesansbold.ttf', 16)
guideX = 290
guideY = 8

# player function
def player(x, y):
    screen.blit(playerImage, (round(x), round(y)))


# enemy function
def enemy(x, y, e):
    screen.blit(enemyImage[e], (round(x), round(y)))


# bullet function
def fireBullet(x, y):
    global bulletState
    bulletState = "fire"
    screen.blit(bulletImage, (round(x + 16), round(y + 10)))


# collusion of bullet & enemy
def gameCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# score function
def gameScore(x, y):
    score = font.render(f"Score: {str(scoreValue)}", True, (255, 255, 255))
    screen.blit(score, (x, y))


# game over function
def gameOver():
    gameOverText = gameOverFont.render(f"Game is Over", True, (255, 255, 255))
    screen.blit(gameOverText, (200, 250))


# guid function
def guide(x, y):
    guideText = guideFont.render("Press Right & Left Arrow for movement, Space key for shoot", True, (255, 255, 255))
    screen.blit(guideText, (x, y))

# game loop
game_run = True
while game_run:

    # screen background -- RGB
    screen.fill((0, 0, 0))

    # background
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_run = False

        # checking keystroke ... pressed or not and if pressed then what is it -- right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerChangeX = -3.5
            if event.key == pygame.K_RIGHT:
                playerChangeX = 3.5
            if event.key == pygame.K_SPACE:
                if bulletState == "ready":
                    bulletSound = mixer.Sound("audio/bullet.wav")
                    bulletSound.play()
                    bulletX = playerX
                    fireBullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerChangeX = 0

    # Checking boundary for battleship
    playerX += playerChangeX

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # enemy movement
    for e in range(totalEnemy):

        if enemyY[e] >=  400:
            for sc in range(totalEnemy):
                enemyY[sc] = 2000
            gameOver()
            break

        enemyX[e] += enemyChangeX[e]
        if enemyX[e] <= 0:
            enemyChangeX[e] = 2.5
            enemyY[e] += enemyChangeY[e]
        elif enemyX[e] >= 736:
            enemyChangeX[e] = -2.5
            enemyY[e] += enemyChangeY[e]

        # collision
        collision = gameCollision(enemyX[e], enemyY[e], bulletX, bulletY)
        if collision:
            explosionSound = mixer.Sound("audio/explosion.wav")
            explosionSound.play()
            bulletY = 480
            bulletState = "ready"
            scoreValue += 15
            enemyX[e] = random.randint(0, 736)
            enemyY[e] = random.randint(50, 120)

        enemy(enemyX[e], enemyY[e], e)

    # bullet fire
    if bulletY <= 0:
        bulletY = 480
        bulletState = "ready"

    if bulletState == "fire":
        fireBullet(bulletX, bulletY)
        bulletY -= bulletChangeY


    player(playerX, playerY)
    gameScore(textX, textY)
    guide(guideX, guideY)
    pygame.display.update()
