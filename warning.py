import pygame

font = pygame.font.SysFont('comicsans', 35)


def error_warn(warn, WIDTH, HEIGHT, WIN):

    while True:
        warnin = font.render(warn, True, '#ffffff')
        WIN.blit(warnin, (WIDTH/2 - warnin.get_width()/2, HEIGHT//1.2))
        pygame.display.update()
        break
    return
