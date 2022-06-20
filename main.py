import os
import sys

import pygame
from pygame.locals import *
from pygame.mixer import fadeout

from button import button
from data import *
from input_box import enter_name_pass
from warning import error_warn

pygame.init()
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space v/s")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
clock = pygame.time.Clock()
BORDER = pygame.Rect(WIDTH//2 - 5, 40, 10, HEIGHT)
BORDER_ = pygame.Rect(0, 40, WIDTH, 10)

BULLET_HIT_SOUND = pygame.mixer.Sound(
    'Assets/Grenade+1.mp3')
BULLET_FIRE_SOUND = pygame.mixer.Sound(
    'Assets/Gun+Silencer.mp3')
INTRO_MUSIC = pygame.mixer.Sound(
    'Assets/intromusic.mp3')

HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)
font = pygame.font.SysFont('comicsans', 35)

FPS = 60
VEL = 5
BULLET_VEL = 7
MAX_BULLETS = 3
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40
GAME_TITLE = pygame.image.load(
    os.path.join('Assets', 'SpacevswelcomeScreen.png'))
YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2
YELLOW_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets', 'spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)
RED_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)

SPACE = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT))

player_input = ((WIDTH/2)-120, HEIGHT//1.6)


def WelcomeScreen():

    WIN.blit(SPACE, (0, 0))
    WIN.blit(GAME_TITLE, (0, 0))
    INTRO_MUSIC.play(loops=-1)
    button_text_exit = 'Exit'
    button_text_newgame = "New Game"
    path = button(WIN, WIDTH, HEIGHT, button_text_newgame,
                  button_text_exit, K_ESCAPE)
    if path is True:
        log_reg()
    elif path is False:
        battle_drop()
        pygame.quit()
        sys.exit()


def log_reg():
    WIN.blit(SPACE, (0, 0))
    WIN.blit(GAME_TITLE, (0, 0))
    button_text_register = 'Register'
    button_text_login = "Log in"
    choice = button(WIN, WIDTH, HEIGHT,  button_text_login,
                    button_text_register, K_SPACE)
    if choice is True:
        input_name_login()
    elif choice is False:
        input_name_reg()


def input_name_login():  # we are logging in
    button_text_register = 'Register'
    button_text_login = " Try again?"
    while True:  # so less comments :) is it biting???
        clock.tick(FPS)
        WIN.blit(SPACE, (0, 0))
        WIN.blit(GAME_TITLE, (0, 0))
        PLAYER1 = enter_name_pass(
            WIN, player_input, 1, "username", "Login", SPACE, GAME_TITLE)
        PLAYER1_PASS = enter_name_pass(
            WIN, player_input, 1, "password", "Login", SPACE, GAME_TITLE)
        if data_check(PLAYER1, PLAYER1_PASS, "login") == False:
            WIN.blit(SPACE, (0, 0))
            WIN.blit(GAME_TITLE, (0, 0))
            error_warn("Wrong username or password", WIDTH, HEIGHT, WIN)
            choice = button(WIN, WIDTH, HEIGHT, button_text_login,
                            button_text_register, K_SPACE)
            if choice is True:
                continue
            elif choice is False:
                pp = input_name_redir_reg(1)
                PLAYER1 = pp[0]
                PLAYER1_PASS = pp[1]
                PLAYER_1 = pp[2]
                break
        else:
            PLAYER_1 = font.render(PLAYER1, True, WHITE)
            break

    while True:
        clock.tick(FPS)
        WIN.blit(SPACE, (0, 0))
        WIN.blit(GAME_TITLE, (0, 0))
        PLAYER2 = enter_name_pass(
            WIN, player_input, 2, "username", "Login", SPACE, GAME_TITLE)
        PLAYER2_PASS = enter_name_pass(
            WIN, player_input, 2, "password", "Login", SPACE, GAME_TITLE)
        if data_check(PLAYER2, PLAYER2_PASS, "login") == False:
            WIN.blit(SPACE, (0, 0))
            WIN.blit(GAME_TITLE, (0, 0))
            error_warn("Wrong username or password", WIDTH, HEIGHT, WIN)
            choice = button(WIN, WIDTH, HEIGHT, button_text_login,
                            button_text_register, K_SPACE)
            if choice is True:
                continue
            elif choice is False:
                pp = input_name_redir_reg(2)
                PLAYER2 = pp[0]
                PLAYER2_PASS = pp[1]
                PLAYER_2 = pp[2]
                break
        else:
            PLAYER_2 = font.render(PLAYER2, True, WHITE)
            break
    scores = game_scores_retriev(PLAYER1, PLAYER2)
    fadeout(1000)
    main(PLAYER_1, PLAYER1, PLAYER_2, PLAYER2, scores)


def input_name_reg():  # we are registering
    while True:  # so less comments :) is it biting???
        clock.tick(FPS)
        WIN.blit(SPACE, (0, 0))
        WIN.blit(GAME_TITLE, (0, 0))
        PLAYER1 = enter_name_pass(
            WIN, player_input, 1, "username", "Register", SPACE, GAME_TITLE)
        PLAYER1_PASS = enter_name_pass(
            WIN, player_input, 1, "password", "Register", SPACE, GAME_TITLE)
        if data_check(PLAYER1, PLAYER1_PASS, "reg") == True:
            error_warn(
                "Username Already exists! try something else...", WIDTH, HEIGHT, WIN)
            pygame.time.delay(1000)
            continue
        else:
            data_saving(PLAYER1, PLAYER1_PASS)
            PLAYER_1 = font.render(PLAYER1, True, WHITE)
            break

    while True:  # so less comments :) is it biting???
        clock.tick(FPS)
        WIN.blit(SPACE, (0, 0))
        WIN.blit(GAME_TITLE, (0, 0))
        PLAYER2 = enter_name_pass(
            WIN, player_input, 2, "username", "Register", SPACE, GAME_TITLE)
        PLAYER2_PASS = enter_name_pass(
            WIN, player_input, 2, "password", "Register", SPACE, GAME_TITLE)
        if data_check(PLAYER2, PLAYER2_PASS, "reg") == True:
            error_warn(
                "Username Already exists! try something else...", WIDTH, HEIGHT, WIN)
            pygame.time.delay(1000)
            continue
        else:
            data_saving(PLAYER2, PLAYER2_PASS)
            PLAYER_2 = font.render(PLAYER2, True, WHITE)
            break
    scores = game_scores_retriev(PLAYER1, PLAYER2)
    fadeout(1000)
    main(PLAYER_1, PLAYER1, PLAYER_2, PLAYER2, scores)


def input_name_redir_reg(num):  # we are registering if login fails
    while True:  # so less comments :) is it biting???
        clock.tick(FPS)
        WIN.blit(SPACE, (0, 0))
        WIN.blit(GAME_TITLE, (0, 0))
        PLAYER = enter_name_pass(
            WIN, player_input, num, "username", "Register", SPACE, GAME_TITLE)
        PLAYER_PASS = enter_name_pass(
            WIN, player_input, num, "password", "Register", SPACE, GAME_TITLE)
        if data_check(PLAYER, PLAYER_PASS, "reg") == True:
            error_warn(
                "Username Already exists! try something else...", WIDTH, HEIGHT, WIN)
            pygame.time.delay(1000)
            continue
        else:
            data_saving(PLAYER, PLAYER_PASS)
            PLAYER_ = font.render(PLAYER, True, WHITE)
            return PLAYER, PLAYER_PASS, PLAYER_


def draw_window(red, yellow, red_bullets, yellow_bullets, red_health,
                yellow_health, PLAYER1, PLAYER2, scores):
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)
    pygame.draw.rect(WIN, BLACK, BORDER_)
    PLAYER__1 = HEALTH_FONT.render(PLAYER1 + "'s", 1, WHITE)
    PLAYER__2 = HEALTH_FONT.render(PLAYER2 + "'s", 1, WHITE)
    red_health_text = HEALTH_FONT.render(
        "health: " + str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render(
        "health: " + str(yellow_health), 1, WHITE)
    WIN.blit(PLAYER__1, (10, 10))
    WIN.blit(PLAYER__2, (WIDTH - red_health_text.get_width() -
             PLAYER__2.get_width() - 15, 10))
    WIN.blit(yellow_health_text, (PLAYER__1.get_width() + 15, 10))
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    #WIN.blit(PLAYER_1, (yellow.x-PLAYER_1.get_width()/yellow.x, yellow.y+SPACESHIP_HEIGHT+10))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))
    #WIN.blit(PLAYER_2, (red.x+ PLAYER_2.get_width()/red.x, red.y+SPACESHIP_HEIGHT+10))
    score = HEALTH_FONT.render(f"{scores[0]} - {scores[1]}", True, WHITE)
    WIN.blit(score, (WIDTH/2 - score.get_width()/2, 10))

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    pygame.display.update()


def yellow_handle_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0:  # LEFT
        yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width - 3 < BORDER.x:     # RIGHT
        yellow.x += VEL
    if keys_pressed[pygame.K_w] and yellow.y - VEL > BORDER_.y + 5:  # UP
        yellow.y -= VEL
    if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT - 15:  # DOWN
        yellow.y += VEL


def red_handle_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - VEL - 10 > BORDER.x + BORDER.width:  # LEFT
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width - 13 < WIDTH:  # RIGHT
        red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y - VEL > BORDER_.y + 5:  # UP
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT - 15:  # DOWN
        red.y += VEL


def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)


def draw_winner(text, PLAYER_1, PLAYER1, PLAYER_2, PLAYER2, winner, scores):
    WIN.blit(SPACE, (0, 0))
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width() /
                         2, HEIGHT/2 - draw_text.get_height()/2))
    game_scores_saving(PLAYER1, PLAYER2, winner)
    pygame.display.update()
    pygame.time.delay(3000)
    continue_game(PLAYER_1, PLAYER1, PLAYER_2, PLAYER2)


def continue_game(PLAYER_1, PLAYER1, PLAYER_2, PLAYER2):
    WIN.blit(SPACE, (0, 0))
    playagain = font.render("Wanna play again?", True, WHITE)
    enter_yes = "Yes(ENTER)"
    esc_no = "No(ESC)"
    WIN.blit(playagain, (WIDTH/2 - playagain.get_width()/2, HEIGHT/2))
    choice = button(WIN, WIDTH, HEIGHT, enter_yes,
                    esc_no, K_ESCAPE)
    while True:
        for event in pygame.event.get():
            clock.tick(FPS)
            if event.type == QUIT:
                battle_drop()
                pygame.quit()
                sys.exit()
            if choice == True:
                scores = game_scores_retriev(PLAYER1, PLAYER2)
                main(PLAYER_1, PLAYER1, PLAYER_2, PLAYER2, scores)
            if choice == False:
                battle_drop()
                WelcomeScreen()
        pygame.display.update()


def main(PLAYER_1, PLAYER1, PLAYER_2, PLAYER2, scores):
    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    red_bullets = []
    yellow_bullets = []

    red_health = 10
    yellow_health = 10

    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == QUIT:
                battle_drop()
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        red.x, red.y + red.height//2 - 2, 10, 5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()

            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()

        winner_text = ""
        if red_health <= 0:
            winner_text = f"{PLAYER1} Wins!"
            winner = PLAYER1
        if yellow_health <= 0:
            winner_text = f"{PLAYER2} Wins!"
            winner = PLAYER2
        if winner_text != "":
            draw_winner(winner_text, PLAYER_1, PLAYER1,
                        PLAYER_2, PLAYER2, winner, scores)

        keys_pressed = pygame.key.get_pressed()
        yellow_handle_movement(keys_pressed, yellow)
        red_handle_movement(keys_pressed, red)

        handle_bullets(yellow_bullets, red_bullets, yellow, red)

        draw_window(red, yellow, red_bullets, yellow_bullets,
                    red_health, yellow_health, PLAYER1, PLAYER2, scores)
    #continue_game(PLAYER_1, PLAYER1, PLAYER_2, PLAYER2, scores)


if __name__ == "__main__":
    WelcomeScreen()
