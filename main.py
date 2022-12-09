from bs4 import BeautifulSoup
from os import walk
import requests


# Парсит html файл и возвращает список ссылок на фото
def find_photo(file):
    links = []

    with open(file, 'r') as page:
        soup = BeautifulSoup(page, 'html.parser')
        for a in soup.find_all('a', href=True, class_="attachment__link"):
            if "impg" in a['href'] and a['href'] not in links:
                links.append(a['href'])

    return links


# Возвращает номер сообщения
def page_num(page):
    return int(page.replace('messages', '').replace('.html', ''))


path = input('Введите путь до папки: ')

# Проходится по файлам в директории и парсит каждый из них,
# сохраняя все фото из ссылок, что он найдет в папке "Content" в "png." формате
for root, dirs, files in walk(path):
    for filename in sorted(files, key=page_num):
        links = find_photo(file=f'{path}/{filename}')

        if links:
            count = 0
            for link in links:
                link = requests.get(link)
                count += 1

                with open(f'Content\\{filename}({count}).png', 'wb') as photo:
                    photo.write(link.content)
        else:
            continue
