from bs4 import BeautifulSoup
from os import walk
import requests
import tkinter as tk


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


# Проходится по файлам в директории и парсит каждый из них,
# сохраняя все фото из ссылок, что он найдет в папке "Content" в "png." формате
def content_saver(path):
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


def use_path():
	content_saver(e.get())


# GUI
if __name__ == '__main__':
	root = tk.Tk()

	root['bg'] = '#fafafa'
	root.title('VK_ArchiveReader')
	root.wm_attributes('-alpha')

	root.resizable(width=False, height=False)

	tk.Label(root, text="Введите путь к папке: ", font='Roboto', background='#fafafa').grid()

	e = tk.Entry(root, width=50)
	e.grid(row=0, column=1)

	btn = tk.Button(root, text='Submit', font='Roboto', command=use_path)
	btn.grid(row=1, column=0, pady=10)

	root.mainloop()
