import math

import pygame

from functions_general import text_plate, display_text


def interface_display(interface_mode, fonts, surface, images, noise, counter, person_list, genes_database, persons_database):

    if interface_mode == 'genetics':
        color_palette = [
            '#7F0000',
            '#7F3300',
            '#7F6A00',
            '#5B7F00',
            '#267F00',
            '#007F0E',
            '#007F46',
            '#007F7F',
            '#004A7F',
            '#00137F',
        ]
        text_plate(surface, images, 600, 20, 720, 1002, '#003500', '#8ED7FF', 150, noise)
        line_v = pygame.Surface((2, 950))
        line_h = pygame.Surface((200, 2))
        plate = pygame.Surface((98, 48))
        line_v.fill('#8ED7FF')
        line_h.fill('#8ED7FF')
        surface.blit(line_v, (750, 50))
        surface.blit(line_h, (750, 50))
        surface.blit(line_v, (850, 50))
        surface.blit(line_v, (950, 50))

        cell_h = 60
        for ch in genes_database:
            if ch[-1:] == '0':
                plate.fill('#4800FF')
                surface.blit(plate, (751, cell_h - 9))
                marker = ch[:-1]
                surface.blit(fonts['text_30'].render('[' + marker + ']', True, 'white'), (770, cell_h))
                for g in persons_database[person_list]['genes']:
                    if g[:3] == marker:
                        if g[-1:] == '+' or g[:1] == 'D':
                            plate.fill(color_palette[genes_database[g[:4]]['dominant']])
                            surface.blit(plate, (851, cell_h - 9))
                            surface.blit(fonts['text_30'].render('вар. ' + g[3:4], True, 'black'), (870 + 1, cell_h + 1))
                            surface.blit(fonts['text_30'].render('вар. ' + g[3:4], True, 'white'), (870, cell_h))
                            display_text(genes_database[g[:4]]['name'], 300, surface, fonts['text_20'], 20, 980, cell_h + 5, 'white')
                        else:
                            plate.fill('black')
                            surface.blit(plate, (851, cell_h - 9))
                            surface.blit(fonts['text_30'].render('???', True, 'black'), (875 + 1, cell_h + 1))
                            surface.blit(fonts['text_30'].render('???', True, 'white'), (875, cell_h))
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

    return