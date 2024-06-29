import random
import time

import pgzrun
import pygame

# Window instellen
WIDTH = 600
HEIGHT = 350
MARGIN = 10
MARGIN_METEOR = 20
DELAY_METEOR = 3
MARGIN_COLLISION = 15
GAME_SPEED = 3

# Achtergrond instellen
background = pygame.image.load("images/achtergrond.jpeg")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# Ruimteschip instellen
spaceship_image = pygame.image.load("images/ruimteschip.png")
spaceship_image = pygame.transform.scale(spaceship_image, (139, 50))
temp_file = "images/ruimteschip_small.png"
pygame.image.save(spaceship_image, temp_file)

spaceship = Actor("ruimteschip_small")
spaceship.pos = WIDTH // 3, HEIGHT // 2

# Meteor instellen
meteor_image = pygame.image.load("images/meteor.png")
meteor_image = pygame.transform.scale(meteor_image, (80, 80))
temp_file = "images/meteor_small.png"
pygame.image.save(meteor_image, temp_file)

meteor = Actor("meteor_small")
meteor.pos = WIDTH, HEIGHT // 2

# Timer
start_time = time.time()
meteor_created = False


def draw():
    screen.clear()
    screen.blit(background, (0, 0))
    spaceship.draw()
    if meteor_created:
        meteor.draw()


def update():
    global meteor_created
    # Start de eerste meteor na een vertraging
    if not meteor_created and time.time() - start_time > DELAY_METEOR:
        meteor_created = True
        meteor.pos = WIDTH + MARGIN_METEOR, random.randint(0, HEIGHT)

    if keyboard.up and spaceship.y > MARGIN:
        spaceship.y -= 5
    if keyboard.down and spaceship.y < HEIGHT - MARGIN:
        spaceship.y += 5
    if meteor.x < 0:
        meteor.x = WIDTH + MARGIN_METEOR
        meteor.y = random.randint(0, HEIGHT)

    meteor.x -= GAME_SPEED

    # Check for collisions
    if meteor_created and check_collision(spaceship, meteor):
        game_over()


def check_collision(actor1, actor2):
    return actor1.colliderect(actor2)


def game_over():
    print("Game Over")
    print(f"meteor: {meteor.x},  {meteor.y}")
    print(f"spaceship: {spaceship.x},  {spaceship.y}")
    exit()  # Exit the game


pgzrun.go()
