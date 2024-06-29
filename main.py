import pgzrun
import pygame

# Window instellen
WIDTH = 600
HEIGHT = 350
MARGIN = 10

# Achtergrond instellen
background = pygame.image.load("images/achtergrond.jpeg")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# Ruimteschip instellen
spaceship_image = pygame.image.load("images/ruimteschip.png")
spaceship_image = pygame.transform.scale(spaceship_image, (80, 80))
spaceship_image = pygame.transform.rotate(spaceship_image, -45)
temp_file = "images/ruimteschip_rotated.png"
pygame.image.save(spaceship_image, temp_file)

spaceship = Actor("ruimteschip_rotated")
spaceship.pos = WIDTH // 2, HEIGHT // 2


def draw():
    screen.clear()
    screen.blit(background, (0, 0))
    spaceship.draw()


def update():
    if keyboard.up and spaceship.y > MARGIN:
        spaceship.y -= 5
    if keyboard.down and spaceship.y < HEIGHT - MARGIN:
        spaceship.y += 5


def game_over():
    pass


pgzrun.go()
