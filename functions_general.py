import random
import sys
import pygame
from pygame.locals import MOUSEWHEEL


def controls():
    pressed = pygame.key.get_pressed()
    control_click = pygame.mouse.get_pressed()[0]
    mouse_wheel = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif pressed[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEWHEEL:
            mouse_wheel = event.y
    return control_click, mouse_wheel


def text_plate(surface, images, x, y, width, height, color='#E0CFB1', color_line='#9B764D', alpha=150, noise=0):
    plate = pygame.Surface((width, height))
    # plate_border = pygame.Surface((width - 6, height - 6))
    # plate_useful = pygame.Surface((width - 10, height - 10))
    plate_header = pygame.Surface((width - 40, 10))
    plate_line = pygame.Surface((width - 40, 2))
    plate_noise = pygame.Surface((width - 10, 2))
    plate.fill(color)
    # plate_border.fill(color_line)
    # plate_useful.fill(color)
    plate_header.fill(color)
    plate_line.fill(color_line)
    plate_noise.fill('black')
    # plate.blit(plate_border, (3, 3))
    # plate.blit(plate_useful, (5, 5))
    plate.set_alpha(alpha)
    plate_noise.set_alpha(alpha - 50)
    surface.blit(plate, (x, y))
    for n in range(y + 5, y + height - 10, 6):
        surface.blit(plate_noise, (x + 5, n + noise))
    surface.blit(plate_header, (x + 20, y - 10))
    surface.blit(plate_line, (x + 20, y - 10))
    surface.blit(plate_line, (x + 20, y - 6))
    surface.blit(plate_line, (x + 20, y - 2))
    surface.blit(images['left_corner'], (x, y - 10))
    surface.blit(images['right_corner'], (x + width - 20, y - 10))
    return


def display_text(input_text, width, surface, text_font, font_size, x, y, color, upper=0, strings=0, centered=False):
    input_text_ = input_text.split(' ')
    result_text = ['']
    j = 0
    for i in range(len(input_text_)):
        if text_font.size(result_text[j] + input_text_[i])[0] > width or input_text_[i] == '@':
            j += 1
            if input_text_[i][-1:] == '@':
                input_text_[i] = input_text_[i][:-1]
            result_text.append(input_text_[i] + ' ')
        else:
            result_text[j] += input_text_[i] + ' '
    i = 0
    for t in result_text:
        if t[:1] == ' ':
            t = t[1:]
        if centered:
            xx = width - text_font.size(t)[0]
            while xx > 0:
                t = ' ' + t
                xx -= 1
        surface.blit(text_font.render(t, True, 'black'), (x + 1, (y + 1 + i * font_size)))
        surface.blit(text_font.render(t, True, color), (x, (y + i * font_size)))
        i += 1
    return upper


def shifter(y, y_tgt, incr):
    if y_tgt > y:
        y += incr
        if y > y_tgt:
            y = y_tgt
    elif y_tgt < y:
        y -= incr
        if y < y_tgt:
            y = y_tgt
    return y


def create_button(button_text, mode, value, x, y, width, height, text_font, surface, control_click, color='#03193F', color_line='#8ED7FF', alpha=150):
    button = pygame.Surface((width, height))
    button_inside = pygame.Surface((width - 4, height - 4))
    button.set_alpha(alpha)
    button_inside.set_alpha(alpha)
    button_hbox = pygame.Rect(x, y, width, height)
    # button_hbox.width = button_hbox.width / scr_mult
    # button_hbox.height = button_hbox.height / scr_mult

    if control_click and button_hbox.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0] is False:
        if mode != value:
            mode = value
        else:
            mode = ''

    if mode != value:
        if button_hbox.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            button.fill(color)
            button_inside.fill('grey')
            surface.blit(button, (x, y + 2))
            surface.blit(button_inside, (x + 2, y + 4))
            txt_shift = int((width - text_font.size(button_text)[0])/2)
            vert_shift = int((height - text_font.size(button_text)[1])/2)
            surface.blit(text_font.render(button_text, True, 'black'), (x + txt_shift, y + vert_shift + 2))
        else:
            button.fill(color_line)
            button_inside.fill(color)
            surface.blit(button, (x, y))
            surface.blit(button_inside, (x + 2, y + 2))
            txt_shift = int((width - text_font.size(button_text)[0])/2)
            vert_shift = int((height - text_font.size(button_text)[1])/2)
            surface.blit(text_font.render(button_text, True, 'black'), (x + 1 + txt_shift, y + 1 + vert_shift))
            surface.blit(text_font.render(button_text, True, color_line), (x + txt_shift, y + vert_shift))
    else:
        if button_hbox.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            button.fill(color_line)
            button_inside.fill(color)
            surface.blit(button, (x, y))
            surface.blit(button_inside, (x + 2, y + 2))
            txt_shift = int((width - text_font.size(button_text)[0])/2)
            vert_shift = int((height - text_font.size(button_text)[1])/2)
            surface.blit(text_font.render(button_text, True, 'black'), (x + 1 + txt_shift, y + 1 + vert_shift))
            surface.blit(text_font.render(button_text, True, color_line), (x + txt_shift, y + vert_shift))
        else:
            button.fill(color)
            button_inside.fill('grey')
            surface.blit(button, (x, y + 2))
            surface.blit(button_inside, (x + 2, y + 4))
            txt_shift = int((width - text_font.size(button_text)[0])/2)
            vert_shift = int((height - text_font.size(button_text)[1])/2)
            surface.blit(text_font.render(button_text, True, 'black'), (x + txt_shift, y + vert_shift + 2))

    return mode

