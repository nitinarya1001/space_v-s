import sys

import pygame
from pygame.constants import K_RETURN

pygame.font.init()

pygame.init()
clock = pygame.time.Clock()
fps = 60
WHITE = [255, 255, 255]
font = pygame.font.SysFont('comicsans', 35)


def button(WIN, WIDTH, HEIGHT, button_text_1, button_text_2, key_):
    button_y_pos = HEIGHT//1.6
    button_size = (200, 60)
    buttontextrender_1 = font.render(button_text_1, True, WHITE)
    buttontextrender_2 = font.render(button_text_2, True, WHITE)

    button_1 = pygame.Rect((WIDTH//4.5, button_y_pos),
                           button_size)  # button1 rect
    button_2 = pygame.Rect((WIDTH//1.9, button_y_pos),
                           button_size)  # button2 rect

    button_text_pos_1 = (button_1.centerx - (buttontextrender_1.get_width()/2),
                         button_1.centery - (buttontextrender_1.get_height()/2))
    button_text_pos_2 = (button_2.centerx - (buttontextrender_2.get_width()/2),
                         button_2.centery - (buttontextrender_2.get_height()/2))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == K_RETURN:
                    return True
                if event.key == key_:
                    return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos  # gets mouse position

                # checks if mouse position is over the button

                if button_1.collidepoint(mouse_pos):
                    # prints current location of mouse
                    return True
                if button_2.collidepoint(mouse_pos):
                    # prints current location of mouse
                    return False
        pygame.draw.rect(WIN, '#175734', button_1)  # draw new gamebutton
        WIN.blit(buttontextrender_1, (button_text_pos_1))
        pygame.draw.rect(WIN, '#8a1919',
                         button_2)  # draw exit button
        WIN.blit(buttontextrender_2, button_text_pos_2)
        pygame.display.update()
        clock.tick(fps)
