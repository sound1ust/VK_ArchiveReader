from bs4 import BeautifulSoup
from os import walk
import requests


# Парсит html файл и возвращает ссылку на фото
def find_photo(file):
    with open(file, 'r') as page:
        soup = BeautifulSoup(page, 'html.parser')
        for a in soup.find_all('a', href=True, class_="attachment__link"):
            if "impg" in a['href']:
                return a['href']


# Возвращает номер сообщения
def page_num(page):
    return int(page.replace('messages', '').replace('.html', ''))


path = input('Введите путь до папки: ')

for root, dirs, files in walk(path):
    for filename in sorted(files, key=page_num):
        result = find_photo(file=f'{path}/{filename}')
        if result is not None:
            result = requests.get(result)

            with open(f'Content\\{filename}.png', 'wb') as photo:
                photo.write(result.content)
