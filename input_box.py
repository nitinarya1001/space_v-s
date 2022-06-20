import sys

import pygame


def enter_name_pass(screen, player_input, player_num, pl_pa, log_reg, SPACE, GAME_TITLE):
    font = pygame.font.Font(None, 32)
    clock = pygame.time.Clock()
    input_box = pygame.Rect(player_input, (140, 32))
    color = pygame.Color('#ffffff')
    text = ''
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return text
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode

        screen.blit(SPACE, (0, 0))
        screen.blit(GAME_TITLE, (0, 0))
        # Render the current text.
        txt_surface = font.render(text, True, color)
        player_entry = font.render(
            f"Enter the {pl_pa} of player {player_num}", True, color)
        pl_log_reg = font.render(f"Player {player_num} {log_reg}", True, color)
        # Resize the box if the text is too long.
        width = max(200, txt_surface.get_width()+10)
        input_box.w = width
        # Blit the text.
        screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
        screen.blit(player_entry, (input_box.x-50, input_box.y+40))
        if log_reg == "Register":
            screen.blit(pl_log_reg, (input_box.x+10, input_box.y-40))
        else:
            screen.blit(pl_log_reg, (input_box.x+20, input_box.y-40))
        # Blit the input_box rect.
        pygame.draw.rect(screen, color, input_box, 2)
        pygame.display.flip()
        pygame.display.update()
        clock.tick(60)
