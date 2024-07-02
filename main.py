import random
import time

import pgzrun
import pygame

# Window instellen
WIDTH = 800
HEIGHT = 500
MARGIN = 10
MARGIN_METEOR = 20
DELAY_METEOR = 3
MARGIN_COLLISION = 15
GAME_OVER_TIME = 3
START_GAME_SPEED = 6

#Soundeffect collision instellen
pygame.mixer.init()
collision_sound = pygame.mixer.Sound("sounds/collision.wav")

#Soundeffect gameover instellen
pygame.mixer.init()
gameover_sound = pygame.mixer.Sound("sounds/gameover.wav")

#Achtergrondmuziek laden
pygame.mixer.music.load("sounds/achtergrondmuziek.wav")
#Muziek laten herhalen
pygame.mixer.music.play(-1) 
#Volume achtergrondmuziek instellen
pygame.mixer.music.set_volume(0.5)

def resize_image(image_file, width, height):
    resized_image_file = f"resized_{image_file}"
    image = pygame.image.load(f"images/{image_file}")
    image = pygame.transform.scale(image, (width, height))
    pygame.image.save(image, f"images/{resized_image_file}")
    return resized_image_file


# Achtergrond instellen
background = pygame.image.load("images/achtergrond.jpeg")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# Ruimteschip instellen
spaceship = Actor(resize_image("ruimteschip.png", 139, 50))
spaceship.pos = WIDTH // 3, HEIGHT // 2

# Obstakels instellen

obstacle_images = [
    resize_image(img, 80, 80)
    for img in ["meteor.png", "ufo.png", "satellite.png"]
]
obstacle = Actor(random.choice(obstacle_images))
obstacle.pos = WIDTH, HEIGHT // 2

# Timer en booleans
start_time = time.time()
obstacle_is_created = False
game_is_over = False
game_over_time = 0
game_speed = START_GAME_SPEED
collisions = 0


def draw():
    global obstacle_is_created, game_is_over, game_speed, collisions
    screen.clear()
    screen.blit(background, (0, 0))

    if game_is_over:
        screen.draw.text("GAME OVER",
                         center=(WIDTH // 2, HEIGHT // 2),
                         fontsize=80,
                         color="red")
    else:
        screen.draw.text(f"speed: {game_speed}, collisions: {collisions}",
                         center=(WIDTH // 2, HEIGHT - 40),
                         fontsize=40,
                         color="red")
        spaceship.draw()
        if obstacle_is_created:
            obstacle.draw()


def update():
    global obstacle_is_created, game_is_over, game_speed, collisions

    if game_is_over:
        if time.time() - game_over_time > GAME_OVER_TIME:
            exit()
        return

    # Start de eerste meteor na een vertraging
    if not obstacle_is_created and time.time() - start_time > DELAY_METEOR:
        obstacle_is_created = True
        obstacle.pos = WIDTH + MARGIN_METEOR, random.randint(0, HEIGHT)

    if keyboard.up and spaceship.y > MARGIN:
        spaceship.y -= 5
    if keyboard.down and spaceship.y < HEIGHT - MARGIN:
        spaceship.y += 5
    if obstacle.x < 0:
        new_obstacle()

    game_speed = round(START_GAME_SPEED + (time.time() - start_time) / 12, 1)
    obstacle.x -= game_speed

    # Check for collisions
    if obstacle_is_created and check_collision(spaceship, obstacle):
        pygame.mixer.Sound.play(collision_sound)
        new_obstacle()
        collisions += 1

    if collisions >= 3:
        pygame.mixer.Sound.play(gameover_sound)
        game_over()

def new_obstacle():
    global obstacle_images
    obstacle.image = random.choice(obstacle_images)
    obstacle.x = WIDTH + MARGIN_METEOR
    obstacle.y = random.randint(0, HEIGHT)


def check_collision(actor1, actor2):
    return actor1.colliderect(actor2)


def game_over():
    global game_is_over, game_over_time
    print("Game Over")
    game_is_over = True
    game_over_time = time.time()


pgzrun.go()
