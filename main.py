import random
import time
import sqlite3

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

# Soundeffect collision instellen
pygame.mixer.init()
collision_sound = pygame.mixer.Sound("sounds/collision.wav")

# Soundeffect gameover instellen
pygame.mixer.init()
gameover_sound = pygame.mixer.Sound("sounds/gameover.wav")

# Achtergrondmuziek laden
pygame.mixer.music.load("sounds/achtergrondmuziek.wav")
# Muziek laten herhalen
pygame.mixer.music.play(-1)
# Volume achtergrondmuziek instellen
pygame.mixer.music.set_volume(0.5)

def resize_image(image_file, width, height):
    resized_image_file = f"resized_{image_file}"
    image = pygame.image.load(f"images/{image_file}")
    image = pygame.transform.scale(image, (width, height))
    pygame.image.save(image, f"images/{resized_image_file}")
    return resized_image_file

class SpaceGame:
    def __init__(self):
        # SQLite database instellen
        self.conn = sqlite3.connect('highscore.db')
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE IF NOT EXISTS highscore (score REAL)''')
        self.conn.commit()

        # Achtergrond instellen
        self.background = pygame.image.load("images/achtergrond.jpeg")
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))

        # Ruimteschip instellen
        self.spaceship = Actor(resize_image("ruimteschip.png", 139, 50))
        self.spaceship.pos = WIDTH // 3, HEIGHT // 2

        # Obstakels instellen
        self.obstacle_images = [
            resize_image(img, 80, 80)
            for img in ["meteor.png", "ufo.png", "satellite.png"]
        ]
        self.obstacle = Actor(random.choice(self.obstacle_images))
        self.obstacle.pos = WIDTH, HEIGHT // 2

        # Timer en booleans
        self.start_time = time.time()
        self.obstacle_is_created = False
        self.game_is_over = False
        self.game_over_time = 0
        self.game_speed = START_GAME_SPEED
        self.collisions = 0
        self.high_score = self.get_high_score()
        self.current_score = 0

    def get_high_score(self):
        self.c.execute('SELECT MAX(score) FROM highscore')
        result = self.c.fetchone()
        return result[0] if result[0] is not None else 0

    def save_high_score(self, score):
        self.c.execute('INSERT INTO highscore (score) VALUES (?)', (score,))
        self.conn.commit()

    def draw(self):
        screen.clear()
        screen.blit(self.background, (0, 0))

        if self.game_is_over:
            screen.draw.text("GAME OVER",
                             center=(WIDTH // 2, HEIGHT // 2),
                             fontsize=80,
                             color="red")
            screen.draw.text(f"High Score: {self.high_score}",
                             center=(WIDTH // 2, HEIGHT // 2 + 80),
                             fontsize=40,
                             color="yellow")
            screen.draw.text(f"Your Score: {self.current_score}",
                             center=(WIDTH // 2, HEIGHT // 2 + 130),
                             fontsize=40,
                             color="white")
        else:
            screen.draw.text(f"speed: {self.game_speed}, collisions: {self.collisions}",
                             center=(WIDTH // 2, HEIGHT - 40),
                             fontsize=40,
                             color="red")
            self.spaceship.draw()
            if self.obstacle_is_created:
                self.obstacle.draw()

    def update(self):
        if self.game_is_over:
            if time.time() - self.game_over_time > GAME_OVER_TIME:
                exit()
            return

        # Start de eerste meteor na een vertraging
        if not self.obstacle_is_created and time.time() - self.start_time > DELAY_METEOR:
            self.obstacle_is_created = True
            self.obstacle.pos = WIDTH + MARGIN_METEOR, random.randint(0, HEIGHT)

        if keyboard.up and self.spaceship.y > MARGIN:
            self.spaceship.y -= 5
        if keyboard.down and self.spaceship.y < HEIGHT - MARGIN:
            self.spaceship.y += 5
        if self.obstacle.x < 0:
            self.new_obstacle()

        self.game_speed = round(START_GAME_SPEED + (time.time() - self.start_time) / 12, 1)
        self.obstacle.x -= self.game_speed

        # Update current score
        self.current_score = self.game_speed

        # Check for collisions
        if self.obstacle_is_created and self.check_collision(self.spaceship, self.obstacle):
            pygame.mixer.Sound.play(collision_sound)
            self.new_obstacle()
            self.collisions += 1

        # Bij 3 collisions "Game Over" weergeven
        if self.collisions >= 3:
            pygame.mixer.Sound.play(gameover_sound)
            if self.game_speed > self.high_score:
                self.save_high_score(self.game_speed)
                self.high_score = self.game_speed
            self.game_over()

    def new_obstacle(self):
        self.obstacle.image = random.choice(self.obstacle_images)
        self.obstacle.x = WIDTH + MARGIN_METEOR
        self.obstacle.y = random.randint(0, HEIGHT)

    def check_collision(self, actor1, actor2):
        return actor1.colliderect(actor2)

    def game_over(self):
        print("Game Over")
        self.game_is_over = True
        self.game_over_time = time.time()

# Instantie van de game class aanmaken
game = SpaceGame()

def draw():
    game.draw()

def update():
    game.update()

pgzrun.go()

# Verbinding met SQLite-database afsluiten
import atexit
atexit.register(lambda: game.conn.close())
