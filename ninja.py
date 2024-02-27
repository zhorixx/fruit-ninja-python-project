import pygame
import os
import random
import sqlite3

player_lives = 3
score = 0
fruits = ['melon', 'orange', 'pomegranate', 'guava', 'bomb']
topscore = 0
rounddd = 0
stats = input('Введите ваш никнейм:')

background = pygame.image.load('back.jpg')
ninjago = [pygame.image.load('images/run1.png'),
               pygame.image.load('images/run2.png'),
               pygame.image.load('images/run3.png'),
               pygame.image.load('images/run4.png'),
               pygame.image.load('images/run5.png'),
               ]
Table = True
WIDTH = 800
HEIGHT = 600
FPS = 11
pygame.init()
pygame.display.set_caption('Fruit Ninja on Python')
pygame.mixer.music.load('sounds/misuc.mp3')
pygame.mixer.music.play(-1)
s = pygame.mixer.Sound('sounds/noj.wav')
vz = pygame.mixer.Sound('sounds/vzriv.wav')
gameDisplay = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


font = pygame.font.Font(os.path.join(os.getcwd(), 'comic.ttf'), 42)
score_text = font.render('Points : ' + str(score), True, (255, 255, 255))
lives_icon = pygame.image.load('images/white_lives.png')


def randomka(fruit):
    fruit_path = "images/" + fruit + ".png"
    data[fruit] = {
        'img': pygame.image.load(fruit_path),
        'x': random.randint(100, 500),
        'y': 800,
        'speed_x': random.randint(-10, 10),

        'speed_y': random.randint(-80, -60),
        'throw': False,

        't': 0,
        'hit': False,
    }

    if random.random() >= 0.75:
        data[fruit]['throw'] = True
    else:
        data[fruit]['throw'] = False


data = {}
for fruit in fruits:
    randomka(fruit)


def poisk(x, y):
    gameDisplay.blit(pygame.image.load("images/red_lives.png"), (x, y))


font_name = pygame.font.match_font('comic.ttf')


def textowod(display, text, size, x, y):
    font = pygame.font.Font('comic.ttf', size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    gameDisplay.blit(text_surface, text_rect)


def zhizni(display, x, y, lives, image):
    for i in range(lives):
        img = pygame.image.load(image)
        img_rect = img.get_rect()
        img_rect.x = int(x + 35 * i)
        img_rect.y = y
        display.blit(img, img_rect)

countt = 0
def menu():
    global countt
    gameDisplay.blit(background, (0, 0))
    textowod(gameDisplay, "Fruit Ninja on Python!", 50, WIDTH / 2, HEIGHT / 4 )

    if not game_over:
        textowod(gameDisplay, "Points : " + str(score), 50, WIDTH / 2, HEIGHT / 2 - 50)
        textowod(gameDisplay, "Top Score : " + str(topscore), 50, WIDTH / 2, HEIGHT / 2 + 50)
    textowod(gameDisplay, "Press a key to begin!", 50, WIDTH / 2, HEIGHT * 3 / 4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                s.play()
                waiting = False


first_round = True
game_over = True
game_running = True
while game_running:
    if game_over:
        if first_round:
            menu()
            first_round = False
        game_over = False
        player_lives = 3
        zhizni(gameDisplay, 690, 5, player_lives, 'images/red_lives.png')
        score = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False

    gameDisplay.blit(background, (0, 0))
    gameDisplay.blit(ninjago[countt], (675, 20))
    if countt != 4:
        countt += 1
    else:
        countt = 0
    gameDisplay.blit(score_text, (0, 0))
    zhizni(gameDisplay, 690, 5, player_lives, 'images/red_lives.png')

    for key, value in data.items():
        if value['throw']:
            value['x'] += value['speed_x']
            value['y'] += value['speed_y']
            value['speed_y'] += (1 * value['t'])
            value['t'] += 1

            if value['y'] <= 800:
                gameDisplay.blit(value['img'],
                                 (value['x'], value['y']))

            else:
                randomka(key)

            current_position = pygame.mouse.get_pos()

            if not value['hit'] and current_position[0] > value['x'] and current_position[0] < value['x'] + 60 \
                    and current_position[1] > value['y'] and current_position[1] < value['y'] + 60:
                if key == 'bomb':
                    player_lives -= 1
                    if player_lives == 0:

                        poisk(690, 15)
                    elif player_lives == 1:
                        poisk(725, 15)
                    elif player_lives == 2:
                        poisk(760, 15)
                    if player_lives == 0:
                        if score > topscore:
                            topscore = score
                        rounddd += 1
                        with sqlite3.connect('game.db') as db:
                            cursor = db.cursor()
                            if Table:
                                db.execute(f"""
                                        CREATE TABLE {stats} (
                                            round    INTEGER,
                                            score    INTEGER,
                                            topscore INTEGER
    
                                );
                                    """)
                            bebra = f""" INSERT INTO {stats} (round, score, topscore) VALUES({rounddd}, {score}, {topscore})"""
                            cursor.execute(bebra)
                        Table = False
                        menu()
                        FPS += 5
                        game_over = True

                    half_fruit_path = "images/explosion.png"
                else:
                    half_fruit_path = "images/" + "half_" + key + ".png"

                value['img'] = pygame.image.load(half_fruit_path)
                value['speed_x'] += 10
                if key == 'bomb':
                    vz.play()
                if key != 'bomb':
                    score += 1
                    s.play()
                score_text = font.render('Points : ' + str(score), True, (255, 255, 255))
                value['hit'] = True
        else:
            randomka(key)

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
