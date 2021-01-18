import requests
from bs4 import BeautifulSoup
from os.path import basename

url = "http://books.toscrape.com/"

urls_categories = []
next_page_categories = []
categories_range = []
names_categories = []
book_url_range = []
picture_url_range = []
images_range = []

def scrape_categories(element_category):
	url_category = url + element_category.get('href')
	urls_categories.append(url_category)
	name_category = element_category.get_text(strip=True)
	names_categories.append(name_category)
	return names_categories, urls_categories

def to_next_page(minestrone, link_category):
	next_page = minestrone.find('li', {'class': 'next'})

	if next_page != None:
		next_page_element = next_page.find('a').get('href')
		next_page_url = link_category.replace('index.html', str(next_page_element))
		next_page_categories.append(next_page_url)
		print(next_page_url)
		# urls_categories.append(next_page_url)

	for t in next_page_categories:
		response_next = requests.get(t)
		miso = BeautifulSoup(response_next.text, 'lxml')
		body0 = miso.find('body')
		next_page2 = miso.find('li', {'class': 'next'})			

		if next_page2 != None:
			next_page_element_2 = next_page2.find('a').get('href')
			next_page_url_2 = link_category.replace('index.html', str(next_page_element_2))
			next_page_categories.append(next_page_url_2)

			print('2 ' + next_page_url_2)

		return next_page_categories

def get_url_book(link):
	book_url = link.find('a').get('href').replace('../../../', str(url) + 'catalogue/').replace('../../', str(url) + 'catalogue/')
	book_url_range.append(book_url)
	return book_url_range

def scrape_book_data(body2):
	table = body2.find('table')
	universal_product_code = table.select('td')[0].get_text(strip = True)
	price_excluding_tax = table.select('td')[2].get_text(strip = True)
	price_including_tax = table.select('td')[3].get_text(strip = True)
	number_available = table.select('td')[5].get_text(strip = True)
	review_rating = table.select('td')[6].get_text(strip = True)

	title = body2.find('h1').get_text(strip = True)
	image_url = body2.find('img').get('src').replace('../../', str(url))
	picture_url_range.append(image_url)
	product_description = body2.find('article', {'class':'product_page'}).select('p')[3].get_text(strip = True)
	category = body2.find('ul', {'class':'breadcrumb'}).select('li')[2].find('a').get_text(strip = True)
	categories_range.append(category)
	return universal_product_code, price_including_tax, price_excluding_tax, number_available, review_rating, title, image_url, product_description, category, picture_url_range


response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')

# Récupère la liste des catégories dans le panel de navigation

navigation_panel = soup.find('ul', {'class': 'nav nav-list'}).find('ul').select('a')

for element_category in navigation_panel:
	scrape_categories(element_category)

for link_category in urls_categories:
	response1 = requests.get(link_category)
	minestrone = BeautifulSoup(response1.text, 'lxml')
	body = minestrone.find('body')

	if response1.ok:
		#to_next_page(minestrone, link_category)

		articles = body.findAll('h3')
		for link in articles:
			get_url_book(link)


"""

# Stocke les informations relatives aux catégories

with open('category.csv', 'w') as category_name_file:
	for name in names_categories:
		category_name_file.write(name + '\n')

with open('categories links.txt', 'w') as categories_links_file:
	for link_category in urls_categories:
		response1 = requests.get(link_category)
		minestrone = BeautifulSoup(response1.text, 'lxml')
		body = minestrone.find('body')
		categories_links_file.write(link_category + '\n')

		if response1.ok:

			# Verifie s'il y a une nouvelle page en fonction du nombre de livre

			to_next_page(minestrone)
			print(urls_categories)

			# Récupère tous les livres d'une catégorie

			articles = body.findAll('h3')
			for link in articles:
				get_url_book(link)

			with open('links.txt', 'w') as urls_file:
				for product_url in book_url_range:
					urls_file.write(product_url + '\n')

			# Scrape l'ensemble des données d'un livre

			with open('links.txt', 'r') as urls_file:

					for product_unity in urls_file:
						url_product_unity = product_unity.strip()
						response2 = requests.get(url_product_unity)

						if response2.ok:
							borsch = BeautifulSoup(response2.text, 'lxml')
							body2 = borsch.find('body')
							scrape_book_data(body2)


						# Télécharge les images des livres (200)
								for pic in picture_url_range:
									with open(basename(pic), 'wb') as picture_file
									picture_file.write(requests.get(pic).content)


						
						#output_file.write(url_product_unity + ', ' + universal_product_code + ', ' + title + ', ' + price_including_tax + ', ' + price_excluding_tax + ', ' + number_available + ', ' + product_description + ', ' + category + ', ' + review_rating + ', ' + image_url + '\n')
						

					#for category in categories_range:
						#with open('category.csv', 'w') as :
							#travel_file.write('product_page_url, universal_ product_code (upc), title, price_including_tax, price_excluding_tax, number_available, product_description, category, review_rating, image_url,\n')




"""


