import pgzrun
import pygame

# Window instellen
screen_width = 600
screen_height = 350

# Achtergrond instellen
background = pygame.image.load("images/achtergrond.jpeg")
background = pygame.transform.scale(background, (screen_width, screen_height))


def draw():
    screen.clear()
    screen.blit(background, (0, 0))


def update():
    pass


def game_over():
    pass


pgzrun.go()
