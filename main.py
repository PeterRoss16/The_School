import ctypes
import random
import sys

import pygame

from functions_interface import interface_display
from functions_general import controls, display_text, text_plate, shifter, create_button
from functions_generators import person_generator, person_data, person_ava
from genes_database import genes_database
from persons_database import persons_database
from planet_database import planet_database

# Инициализация загружаемых настроек
user32 = ctypes.windll.user32
user32.SetProcessDPIAware()
scr_res_x = 1920

pygame.init()
screen = pygame.display.set_mode((1920, 1080))
surface = pygame.Surface((1920, 1080))
clock = pygame.time.Clock()

fonts = {
    'text_30': pygame.font.Font('fonts/HIbiny Light.ttf', 30),
    'text_20': pygame.font.Font('fonts/HIbiny Light.ttf', 20),
}
lorem_ipsum = ' Lorem ipsum dolor sit amet, consectetur adipiscing elit. @ Mauris vulputate lacus sit amet enim volutpat, ut suscipit arcu interdum. @ Pellentesque congue ligula sit amet diam dignissim suscipit. Vestibulum semper leo eget ex laoreet posuere. Suspendisse nibh dui, ultrices in imperdiet eget, tristique eget dolor.'

planet_info = 'Планета 1 @ @ Гравитация: 1,6 G @ Атмосфера: пригодна для дыхания'

images = {
    'left_corner': pygame.image.load("images/ui/left_corner.png").convert_alpha(),
    'right_corner': pygame.image.load("images/ui/right_corner.png").convert_alpha(),
    'window_1': pygame.image.load("images/bg/window_1.png").convert_alpha(),
    'planet_green_bg': pygame.image.load("images/bg/planet_green_bg.png").convert_alpha(),
    'planet_green': pygame.image.load("images/bg/planet_green.png").convert_alpha(),
    'planet_desert': pygame.image.load("images/bg/planet_desert.png").convert_alpha(),
    'planet_ice': pygame.image.load("images/bg/planet_ice.png").convert_alpha(),
}

game_state = {
    'current_planet': 'Эден',
    'money': 1000,
    'teachers': [],
    'students': [],
    'agents': [],
}

# Инициализация
alpha = 200
counter = 0
noise = 0
ava = ''
interface_mode = ''

persons_database = person_generator(persons_database, 'Иден', 0,0,0,1)
persons_database = person_generator(persons_database, 'Иден', random.randint(1,4), random.randint(12,35))
persons_database = person_generator(persons_database, 'Иден', random.randint(1,4), random.randint(12,35))
persons_database = person_generator(persons_database, 'Иден', random.randint(1,4), random.randint(12,35))
persons_database = person_generator(persons_database, 'Иден', random.randint(1,4), random.randint(12,35))
persons_database = person_generator(persons_database, 'Иден', random.randint(1,4), random.randint(12,35))
persons_database = person_generator(persons_database, 'Саламанка', random.randint(1,4), random.randint(12,35))
persons_database = person_generator(persons_database, 'Саламанка', random.randint(1,4), random.randint(12,35))
persons_database = person_generator(persons_database, 'Саламанка', random.randint(1,4), random.randint(12,35))
persons_database = person_generator(persons_database, 'Саламанка', random.randint(1,4), random.randint(12,35))
persons_database = person_generator(persons_database, 'Саламанка', random.randint(1,4), random.randint(12,35))
persons_database = person_generator(persons_database, 'Саламанка', random.randint(1,4), random.randint(12,35))
persons_database = person_generator(persons_database, 'Иден', random.randint(0,4), random.randint(18,90), '', '', 1)
persons_database = person_generator(persons_database, 'Иден', random.randint(0,4), random.randint(18,90), '', '', random.randint(1,2))
persons_database = person_generator(persons_database, 'Саламанка', random.randint(0,4), random.randint(18,90), '', '', 1)
persons_database = person_generator(persons_database, 'Саламанка', 0, random.randint(18,90), '', '', random.randint(1,2))
person_list = 0
person_list_max = len(persons_database) - 1
person_list_min = 0

while True:

    clock.tick(60)
    fps = int(clock.get_fps())
    control_click, mouse_wheel = controls()
    counter += 1
    if counter > 60:
        counter = 0
    noise = int(counter/10)
    if mouse_wheel < 0:
        person_list += 1
        ava = ''
    elif mouse_wheel > 0:
        person_list -= 1
        ava = ''
    if person_list < person_list_min:
        person_list = person_list_max
    elif person_list > person_list_max:
        person_list = person_list_min

    person_info = person_data(person_list, persons_database)
    if ava == '':
        ava = person_ava(person_list, persons_database, images)

    # Фон
    surface.blit(images['planet_green_bg'], (0, - 100))
    surface.blit(images['window_1'], (0, 0))

    # # Графическое окно
    # text_plate(surface, 50, 50, 426, 326, '#073C99', '#8ED7FF', alpha)
    # surface.blit(images['planet_green'], (63, 63))
    text_plate(surface, images, 30, 50, 320, 620, '#03193F', '#8ED7FF', alpha, noise)
    if ava != '':
        surface.blit(ava, (40, 60))

    # Информационное окно
    text_plate(surface, images, 30, 700, 506, 300, '#03193F', '#8ED7FF', alpha, noise)
    display_text(person_info, 486, surface, fonts['text_20'], 20, 50, 730, 'white')

    # # Текстовое окно
    # text_plate(surface, 500, 50, 600, 950, '#E0CFB1', '#9B764D', alpha)
    # display_text(person_info, 550, surface, fonts['text_20'], 30, 530, 80, 'black')
    #
    # # Текстовое окно2
    # text_plate(surface, 1124, 50, 1000, 800, 'white', 'grey', alpha)
    # display_text(planet_text, 550, surface, fonts['text_20'], 30, 1154, 80, 'black')

    # Кнопка
    interface_mode = create_button('Генетика', interface_mode, 'genetics', 355, 50, 180, 60, fonts['text_30'], surface, control_click, color='#03193F', color_line='#8ED7FF', alpha=150)
    interface_mode = create_button('Качества', interface_mode, 'traits', 355, 115, 180, 60, fonts['text_30'], surface, control_click, color='#03193F', color_line='#8ED7FF', alpha=150)
    interface_mode = create_button('Отношения', interface_mode, 'relations', 355, 180, 180, 60, fonts['text_30'], surface, control_click, color='#03193F', color_line='#8ED7FF', alpha=150)
    interface_mode = create_button('Знания', interface_mode, 'knowledge', 355, 245, 180, 60, fonts['text_30'], surface, control_click, color='#03193F', color_line='#8ED7FF', alpha=150)
    interface_mode = create_button('Импланты', interface_mode, 'implants', 355, 310, 180, 60, fonts['text_30'], surface, control_click, color='#03193F', color_line='#8ED7FF', alpha=150)

    interface_display(interface_mode, fonts, surface, images, noise, counter, person_list, genes_database, persons_database)

    surface.blit(fonts['text_20'].render('FPS:' + str(fps), True, 'white'), (10, 1050))
    screen.blit(surface, (0, 0))
    pygame.display.flip()