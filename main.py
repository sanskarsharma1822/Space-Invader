import pygame
import random
import math
from pygame import mixer

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Space Invader")
icon = pygame.image.load("alien.png")
playerImage = pygame.image.load("spaceship.png")

bulletImage = pygame.image.load("bullet.png")

space = pygame.image.load("space.jpg")
pygame.display.set_icon(icon)
num_of_enemies = 5

playerX = 370
playerY = 480
player_change = 0
enemyImage = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
for i in range(num_of_enemies):
    enemyImage.append(pygame.image.load("kill.png"))
    enemyX.append(random.randint(32, 568))
    enemyY.append(random.randint(32, 150))
    enemyX_change.append(9)
    enemyY_change.append(40)

bulletX = 0
bulletY = 480
bulletY_change = 20
bullet_state = "ready"

score = 0
font = pygame.font.Font("freesansbold.ttf", 32)
scoreX = 10
scoreY = 10

over = pygame.font.Font('freesansbold.ttf' , 70)

mixer.music.load("background.wav")
mixer.music.play(-1)


def score_value(x, y):
    s = font.render("Score : " + str(score), True, (255, 255, 255))
    screen.blit(s, (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImage, (x + 16, y + 10))


def player(x, y):
    screen.blit(playerImage, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImage[i], (x, y))


def gameover():
    game_over=over.render(" GAME OVER ", True,(255,255,255))
    screen.blit(game_over,(180,200))


def collision(enemyX, enemyY, bulletX, bulletY):
    dis = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if dis < 27:
        return ('a')
    else:
        return ('b')


running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(space, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                player_change = 20
            if event.key == pygame.K_LEFT:
                player_change = -20
            if event.key == pygame.K_SPACE:

                if bullet_state is "ready":
                    laser = mixer.Sound('laser.wav')
                    laser.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                player_change = 0

    playerX += player_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736
    player(playerX, playerY)

    for i in range(num_of_enemies):
        enemyX[i] += enemyX_change[i]
        if enemyY[i] > 440:
            for x in range(num_of_enemies):
                enemyY[x] = 2000
            gameover()
            break

        if enemyX[i] <= 0:
            enemyX[i] = 0
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX[i] = 736
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]
        coll = collision(enemyX[i], enemyY[i], bulletX, bulletY)
        if coll == 'a':
            explosion = mixer.Sound('explosion.wav')
            explosion.play()
            bulletY = 480
            bullet_state = "ready"
            score += 1

            enemyX[i] = random.randint(32, 568)
            enemyY[i] = random.randint(32, 150)
        enemy(enemyX[i], enemyY[i], i)

        if bulletY <= 0:
            bulletY = 480
            bullet_state = "ready"
    score_value(scoreX, scoreY)

    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    pygame.display.update()
