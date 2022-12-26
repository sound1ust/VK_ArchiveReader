import os
from bs4 import BeautifulSoup
from os import walk
import requests
import tkinter as tk
from tkinter import messagebox
import re


# Парсит html файл и возвращает список ссылок на фото
def find_photos(file):
	links = []

	with open(file, 'r') as page:
		soup = BeautifulSoup(page, 'html.parser')
		for a in soup.find_all('a', href=True, class_="attachment__link"):
			if "impg" in a['href'] and a['href'] not in links:
				links.append(a['href'])

	return links


# Возвращает номер страницы
def page_num(page):
	return int(page.replace('messages', '').replace('.html', ''))


# Проходится по файлам в директории и парсит каждый из них,
# сохраняя все фото из ссылок, что он найдет в "png." формате в папке с именем собеседника, созданной в папке "Content"
def content_saver(path):
	os.mkdir(f'Content\\{name.get()}')
	for root, dirs, files in walk(path):
		for filename in sorted(files, key=page_num):
			links = find_photos(file=f'{path}/{filename}')

			if links:
				count = 0
				for link in links:
					link = requests.get(link)
					count += 1

					with open(f'Content\\{name.get()}\\{filename}({count}).png', 'wb') as photo:
						photo.write(link.content)
			else:
				continue


# Ищет в веденном пути к архиву папку messages и в файле index-messages.html ищет введенное имя собеседника
def use_path():
	try:
		with open(f'{archive_path.get()}\messages\index-messages.html', 'r') as page:
			messages = page.read()

			try:
				num = re.findall(rf'<a href="(.+)(/messages0.html">)({name.get()})(</a>)', messages)[0][0]
				path = f'{archive_path.get()}\\messages\\{num}'
				content_saver(path)

			except IndexError:
				messagebox.showerror('Ошибка', 'Указано неверное имя собеседника')

	except FileNotFoundError:
		messagebox.showerror('Ошибка', 'Указан неверный путь к архиву')


# GUI
if __name__ == '__main__':
	root = tk.Tk()

	root['bg'] = '#fafafa'
	root.title('VK_ArchiveReader')
	root.wm_attributes('-alpha')

	root.resizable(width=False, height=False)

	tk.Label(root, text="Введите путь к архиву: ", font='Roboto', background='#fafafa').grid()
	archive_path = tk.Entry(root, width=50)
	archive_path.grid(row=0, column=1)

	tk.Label(root, text="Введите имя собеседника: ", font='Roboto', background='#fafafa').grid()
	global name
	name = tk.Entry(root, width=50)
	name.grid(row=1, column=1)

	btn = tk.Button(root, text='Старт', font='Roboto', command=use_path)
	btn.grid(row=2, column=0, pady=10)

	btn2 = tk.Button(root, text='Стоп', font='Roboto', command=root.destroy)
	btn2.grid(row=2, column=1, pady=10)
	root.mainloop()

