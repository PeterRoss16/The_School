import math

import pygame

from functions_general import text_plate, display_text


def interface_display(interface_mode, fonts, surface, images, noise, counter, person_list, genes_database, persons_database):

    helper_screen = pygame.Surface((1920, 1080), pygame.SRCALPHA)

    if interface_mode == 'genetics':
        color_palette = [
            '',
            '#7F0000',
            '#7F6A00',
            '#5B7F00',
            '#007F0E',
            '#007F7F',
            '#004A7F',
        ]
        text_plate(surface, images, 600, 20, 720, 1002, '#003500', '#8ED7FF', 150, noise)
        line_v = pygame.Surface((2, 950))
        line_h = pygame.Surface((200, 2))
        plate = pygame.Surface((98, 48))
        helper_plate = pygame.Surface((300, 40), pygame.SRCALPHA)
        helper_plate.fill('black')
        helper_plate.set_alpha(200)
        line_v.fill('#8ED7FF')
        line_h.fill('#8ED7FF')
        surface.blit(line_v, (750, 50))
        surface.blit(line_h, (750, 50))
        surface.blit(line_v, (850, 50))
        surface.blit(line_v, (950, 50))

        cell_h = 60
        for ch in genes_database:
            if ch[-1:] == '0':
                marker = ch[:-1]
                # surface.blit(fonts['text_30'].render('[' + marker + ']', True, 'white'), (770, cell_h))
                for num in range(len(persons_database[person_list]['genes'])):
                    g = persons_database[person_list]['genes'][num]
                    g2 = persons_database[person_list]['genes2'][num]
                    biggest = 1
                    if genes_database[g[:4]]['dominant'] < genes_database[g2[:4]]['dominant']:
                        biggest = 2
                    elif genes_database[g[:4]]['dominant'] == genes_database[g2[:4]]['dominant']:
                        biggest = 3
                    if g[:3] == marker:
                        gene_text1 = 0
                        gene_text2 = 0
                        if g[-1:] == '+' or g[:1] == 'D':
                            gene_text1 = 1
                            plate.fill(color_palette[genes_database[g[:4]]['dominant']])
                            plate.set_alpha(255)
                            surface.blit(plate, (751, cell_h - 9))
                            display_text('[' + g[:4] + ']', 300, surface, fonts['text_30'], 30, 770, cell_h, 'white')
                            # Всплывающая подсказка
                            if pygame.Rect(751, cell_h - 9, 98, 48).collidepoint(pygame.mouse.get_pos()):
                                helper_screen.blit(helper_plate, (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1] - 40))
                                display_text(genes_database[g[:4]]['name'], 300, helper_screen, fonts['text_20'], 20, pygame.mouse.get_pos()[0] + 20, pygame.mouse.get_pos()[1] - 30, 'white')

                            if biggest == 2:
                                plate.fill('black')
                                plate.set_alpha(150)
                                surface.blit(plate, (751, cell_h - 9))
                        else:
                            plate.fill('black')
                            plate.set_alpha(255)
                            surface.blit(plate, (751, cell_h - 9))
                            surface.blit(fonts['text_30'].render('???', True, 'black'), (775 + 1, cell_h + 1))
                            surface.blit(fonts['text_30'].render('???', True, 'white'), (775, cell_h))
                        if g2[-1:] == '+' or g2[:1] == 'D':
                            gene_text2 = 1
                            plate.fill(color_palette[genes_database[g2[:4]]['dominant']])
                            plate.set_alpha(255)
                            surface.blit(plate, (851, cell_h - 9))
                            display_text('[' + g2[:4] + ']', 300, surface, fonts['text_30'], 30, 870, cell_h, 'white')
                            # Всплывающая подсказка
                            if pygame.Rect(851, cell_h - 9, 98, 48).collidepoint(pygame.mouse.get_pos()):
                                helper_screen.blit(helper_plate, (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1] - 40))
                                display_text(genes_database[g2[:4]]['name'], 300, helper_screen, fonts['text_20'], 20, pygame.mouse.get_pos()[0] + 20, pygame.mouse.get_pos()[1] - 30, 'white')

                            if biggest == 1:
                                plate.fill('black')
                                plate.set_alpha(150)
                                surface.blit(plate, (851, cell_h - 9))
                        else:
                            plate.fill('black')
                            plate.set_alpha(255)
                            surface.blit(plate, (851, cell_h - 9))
                            surface.blit(fonts['text_30'].render('???', True, 'black'), (875 + 1, cell_h + 1))
                            surface.blit(fonts['text_30'].render('???', True, 'white'), (875, cell_h))

                        if (biggest == 1 or biggest == 3) and gene_text1 == 1:
                            display_text(genes_database[g[:4]]['name'], 300, surface, fonts['text_20'], 20, 980, cell_h + 5, 'white')
                        elif biggest == 2 and gene_text2 == 1:
                            display_text(genes_database[g2[:4]]['name'], 300, surface, fonts['text_20'], 20, 980, cell_h + 5, 'white')

                cell_h += 50

        for dna in range(75, 1025, 50):
            surface.blit(line_h, (750, dna + 25))
            x_shift = 30 * math.sin(math.pi * dna + ((counter / 10) + dna))
            x1 = 660 + int(x_shift)
            x2 = 660 - int(x_shift)
            pygame.draw.circle(surface, '#8ED7FF', (x1, dna), 10, 4)
            pygame.draw.circle(surface, '#8ED7FF', (x2, dna), 10, 4)
            xx1 = min(x1, x2) + 10
            xx2 = max(x1, x2) - 10
            if xx2 - xx1 > 0:
                line = pygame.Surface((xx2 - xx1, 6))
                line.fill('#8ED7FF')
                surface.blit(line, (xx1, dna - 3))

    surface.blit(helper_screen, (0, 0))

    return