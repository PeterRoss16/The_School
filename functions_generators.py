import random

import pygame

from genes_database import genes_database
from knowledge_database import knowledge_database
from names_database import male_names_database, female_names_database, surnames_database, nobles_database
from planet_database import planet_database


def person_generator(persons_database, planet, caste=2, age=0, parent1='', parent2='', educated=0):
    new_person_index = max(list(persons_database)) + 1
    persons_database[new_person_index] = {}
    persons_database[new_person_index]['relations'] = {}
    persons_database[new_person_index]['spouses'] = []
    persons_database[new_person_index]['parents'] = []
    persons_database[new_person_index]['children'] = []
    persons_database[new_person_index]['concubines'] = []
    persons_database[new_person_index]['genes'] = []
    persons_database[new_person_index]['implants'] = []
    persons_database[new_person_index]['knowledge'] = []
    persons_database[new_person_index]['gender'] = random.randint(0, 1)
    persons_database[new_person_index]['home_planet'] = planet
    if persons_database[new_person_index]['gender'] == 0:
        persons_database[new_person_index]['name'] = male_names_database[planet][random.randint(0, len(male_names_database[planet]) - 1)]
    else:
        persons_database[new_person_index]['name'] = female_names_database[planet][random.randint(0, len(female_names_database[planet]) - 1)]
    persons_database[new_person_index]['call'] = ''
    if parent1 != '':
        if persons_database[new_person_index]['name'] == persons_database[parent1]['name']:
            persons_database[new_person_index]['call'] = 'II'
            if persons_database[parent1]['call'] == 'II':
                persons_database[new_person_index]['call'] = 'III'
            elif persons_database[parent1]['call'] == 'III':
                persons_database[new_person_index]['call'] = 'IV'
            elif persons_database[parent1]['call'] == 'IV':
                persons_database[new_person_index]['call'] = 'V'
        elif persons_database[new_person_index]['name'] == persons_database[parent2]['name']:
            persons_database[new_person_index]['call'] = 'II'
            if persons_database[parent2]['call'] == 'II':
                persons_database[new_person_index]['call'] = 'III'
            elif persons_database[parent2]['call'] == 'III':
                persons_database[new_person_index]['call'] = 'IV'
            elif persons_database[parent2]['call'] == 'IV':
                persons_database[new_person_index]['call'] = 'V'
        persons_database[new_person_index]['parents'].append(parent1)
        persons_database[new_person_index]['parents'].append(parent2)
        persons_database[parent1]['children'].append(new_person_index)
        persons_database[parent2]['children'].append(new_person_index)
        persons_database[new_person_index]['surname'] = persons_database[parent1]['surname']
        persons_database[new_person_index]['house'] = persons_database[parent1]['house']
        if persons_database[parent1]['title'] < 5 or persons_database[parent2]['title'] < 5:
            persons_database[new_person_index]['title'] = 4
        persons_database[new_person_index]['caste'] = min(persons_database[parent1]['caste'], persons_database[parent2]['caste'])

        # Генетика
        for ch1 in persons_database[parent1]['genes']:
            for ch2 in persons_database[parent2]['genes']:
                if ch1[:3] == ch2[:3]:
                    if genes_database[ch1[:4]]['dominant'] > genes_database[ch2[:4]]['dominant']:
                        persons_database[new_person_index]['genes'].append(ch1[:4])
                    elif genes_database[ch1[:4]]['dominant'] < genes_database[ch2[:4]]['dominant']:
                        persons_database[new_person_index]['genes'].append(ch2[:4])
                    else:
                        chance = random.randint(1, 2)
                        if chance == 1:
                            persons_database[new_person_index]['genes'].append(ch1[:4])
                        else:
                            persons_database[new_person_index]['genes'].append(ch2[:4])
        persons_database = random_mutations(persons_database, new_person_index, planet, 1, 3)

    else:
        if caste == 0:
            persons_database[new_person_index]['title'] = 4
            persons_database[new_person_index]['surname'] = nobles_database[planet][random.randint(0, len(nobles_database[planet]) - 1)]
        elif caste != 4:
            persons_database[new_person_index]['surname'] = surnames_database[planet][random.randint(0, len(surnames_database[planet]) - 1)]
            persons_database[new_person_index]['title'] = 5
        else:
            persons_database[new_person_index]['surname'] = ''
            persons_database[new_person_index]['title'] = 5
        persons_database[new_person_index]['house'] = ''
        persons_database[new_person_index]['caste'] = caste

        # Генетика
        gene_pool = []
        marker = ''
        for ch in genes_database:
            if ch[-1:] == '0':
                marker = ch[:-1]
                for ch2 in genes_database:
                    if ch2[:3] == marker:
                        for d in range(1, genes_database[ch2]['dominant'] + 1):
                            gene_pool.append(ch2)
                chance = random.randint(0,len(gene_pool) - 1)
                request = gene_pool[chance]
                if request not in planet_database[planet]['unfav_genes']:
                    persons_database[new_person_index]['genes'].append(request)
                    marker = ''
                    gene_pool = []
                else:
                    check = False
                    for f in planet_database[planet]['fav_genes']:
                        if f[:3] == marker:
                            persons_database[new_person_index]['genes'].append(f)
                            marker = ''
                            gene_pool = []
                            check = True
                            break
                    if not check:
                        chance = random.randint(0, len(gene_pool) - 1)
                        request = gene_pool[chance]
                        persons_database[new_person_index]['genes'].append(request)
                        marker = ''
                        gene_pool = []
        persons_database = random_mutations(persons_database, new_person_index, planet)

    persons_database[new_person_index]['health'] = random.randint(40, 100) - (persons_database[new_person_index]['caste'] * 10)
    if persons_database[new_person_index]['health'] < 20:
        persons_database[new_person_index]['health'] = 20
    persons_database[new_person_index]['state'] = 1
    persons_database[new_person_index]['age'] = age

    if educated != 0:
        knowledge_pool = []
        for k in knowledge_database:
            if knowledge_database[k]['rank'] <= educated:
                knowledge_pool.append(k)
        limit = educated
        while True:
            chance = random.randint(0, len(knowledge_pool) - 1)
            persons_database[new_person_index]['knowledge'].append(knowledge_pool[chance])
            del knowledge_pool[chance]
            limit -= 1
            if limit <= 0:
                break

    return persons_database


def random_mutations(persons_database, new_person_index, planet, x=2, y=4):
    count = random.randint(x, y)
    gene_pool = list(genes_database)
    for gene in gene_pool:
        limit = 10
        if gene in planet_database[planet]['fav_genes']:
            limit = 5
        elif gene in planet_database[planet]['unfav_genes']:
            limit = 20
        if genes_database[gene]['dominant'] == 1:
            limit += 10
        chance = random.randint(0, limit)
        for ch in genes_database[gene]['noncom']:
            if ch in persons_database[new_person_index]['genes']:
                chance = 10
        if chance == 0:
            for gene2 in persons_database[new_person_index]['genes']:
                if gene2[:3] == gene[:3]:
                    index = persons_database[new_person_index]['genes'].index(gene2)
                    persons_database[new_person_index]['genes'][index] = gene
            count -= 1
        if count <= 0:
            break
    return persons_database


def person_data(person_list, persons_database, person_info=''):
    subject = persons_database[person_list]
    if subject['gender'] == 0:
        if subject['title'] == 0:
            person_info = 'Император'
        elif subject['title'] == 1:
            person_info = 'Герцог'
        elif subject['title'] == 2:
            person_info = 'Граф'
        elif subject['title'] == 3:
            person_info = 'Барон'
        elif subject['title'] == 4:
            person_info = 'Сквайр'
        elif subject['title'] == 5:
            person_info = ''
    elif subject['gender'] == 1:
        if subject['title'] == 0:
            person_info = 'Императрица'
        elif subject['title'] == 1:
            person_info = 'Герцогиня'
        elif subject['title'] == 2:
            person_info = 'Графиня'
        elif subject['title'] == 3:
            person_info = 'Баронесса'
        elif subject['title'] == 4:
            person_info = 'Леди'
        elif subject['title'] == 5:
            person_info = ''
    person_info += ' ' + subject['name']
    if subject['call'] != '':
        if subject['call'][:1] != 'I' and subject['call'][:1] != 'V':
            person_info += '"'
        else:
            person_info += ' '
        person_info += subject['call']
        if subject['call'][:1] != 'I' and subject['call'][:1] != 'V':
            person_info += '"'
    person_info += ' ' + subject['surname']

    if subject['house'] != '':
        person_info += ', ' + subject['house']

    person_info += ' @ @ Каста: '

    if subject['caste'] == 0:
        person_info += 'аристократы'
    elif subject['caste'] == 1:
        person_info += 'слуги'
    elif subject['caste'] == 2:
        person_info += 'пролы'
    elif subject['caste'] == 3:
        person_info += 'рабы'
    elif subject['caste'] == 4:
        person_info += 'клоны'

    person_info += ' @ @ Родная планета: ' + subject['home_planet'] + ' @ Пол: '

    if subject['gender'] == 0:
        person_info += ' мужской'
    elif subject['gender'] == 1:
        person_info += ' женский'

    person_info += ' @ @ Возраст: ' + str(subject['age']) + ' циклов @ Здоровье: ' + str(subject['health']) + '/100 @ @ '
    return person_info


def person_ava(person_list, persons_database, images):
    ava = pygame.Surface((300, 600))
    ava.fill('white')
    prompt = ''
    subject = persons_database[person_list]

    # Тело
    prompt = 'bo'
    height = 110
    if subject['gender'] == 0:
        prompt += 'ma'
    else:
        prompt += 'fe'
    if 'D2A0' in subject['genes']:
        prompt += 'no'
    elif 'D2A1' in subject['genes']:
        prompt += 'mi'
        height = 245
    elif 'D2A2' in subject['genes']:
        prompt += 'sh'
        height = 140
    elif 'D2A3' in subject['genes']:
        prompt += 'ta'
        height = 60
    elif 'D2A4' in subject['genes']:
        prompt += 'gi'
        height = 30
    if 'D5A0' in subject['genes']:
        prompt += 'no'
    elif 'D5A1' in subject['genes']:
        prompt += 'tn'
    elif 'D5A2' in subject['genes']:
        prompt += 'tk'
    prompt += '1'
    file = pygame.image.load("images/avatars/" + prompt + ".png").convert_alpha()
    ava.blit(file, (0, 0))

    # Лицо
    prompt = 'fa'
    if subject['gender'] == 1:
        prompt += 'fe'
    else:
        prompt += 'ma'
    if 'D4A0' in subject['genes']:
        prompt += 'wh'
    elif 'D4A1' in subject['genes']:
        prompt += 'ye'
    elif 'D4A2' in subject['genes']:
        prompt += 'br'
    elif 'D4A3' in subject['genes']:
        prompt += 'bl'
    elif 'D4A4' in subject['genes']:
        prompt += 'gr'
    else:
        prompt += 'wh'
    prompt += 'me'
    prompt += '1'
    file = pygame.image.load("images/avatars/" + prompt + ".png").convert_alpha()
    ava.blit(file, (101, height))

    # Волосы
    prompt = 'ha'
    if subject['gender'] == 1:
        prompt += 'fe'
    else:
        prompt += 'ma'
    if 'D1A5' in subject['genes']:
        prompt = ''
    elif 'D1A0' in subject['genes']:
        prompt += 'wh'
    elif 'D1A1' in subject['genes']:
        prompt += 'ye'
    elif 'D1A2' in subject['genes']:
        prompt += 'bl'
    elif 'D1A3' in subject['genes']:
        prompt += 'br'
    elif 'D1A4' in subject['genes']:
        prompt += 're'
    if prompt != '':
        prompt += 'st'
        prompt += '1'
        file = pygame.image.load("images/avatars/" + prompt + ".png").convert_alpha()
        ava.blit(file, (101, height))

    return ava

