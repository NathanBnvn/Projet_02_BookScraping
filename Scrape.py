import requests
from bs4 import BeautifulSoup

url = "http://books.toscrape.com/"

urls_categories = []
names_categories = []
book_url_range = []
picture_url_range = []

response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')

def scrape_categories():
	url_category = url + element_category.get('href')
	urls_categories.append(url_category)
	name_category = element_category.get_text(strip=True)
	names_categories.append(name_category)
	return names_categories
					
def to_next_page():
	next_page = minestrone.find('li', {'class': 'next'}).find('a').get('href')
	next_page_url = classification_url.replace('index.html', str(next_page))
	urls_categories.append(next_page_url)
	return urls_categories

def scrape_book_data():
	table = body2.find('table')
	universal_product_code = table.select('td')[0].get_text(strip = True)
	price_excluding_tax = table.select('td')[2].get_text(strip = True)
	price_including_tax = table.select('td')[3].get_text(strip = True)
	number_available = table.select('td')[5].get_text(strip = True)
	review_rating = table.select('td')[6].get_text(strip = True)

	title = body2.find('h1').get_text(strip = True)
	image_url = body2.find('img').get('src').replace('../../', str(url))
	product_description = body2.find('article', {'class':'product_page'}).select('p')[3].get_text(strip = True)
	category = body2.find('ul', {'class':'breadcrumb'}).select('li')[2].find('a').get_text(strip = True)
	return universal_product_code, price_including_tax, price_excluding_tax, number_available, review_rating, title, image_url, product_description, category

def download_image():
	pass

# Récupèrer la liste des catégories dans le panel de navigation

navigation_panel = soup.find('ul', {'class': 'nav nav-list'}).find('ul').select('a')
#print(navigation_panel)
for element_category in navigation_panel:
	scrape_categories()
	print(scrape_categories())

with open('category.csv', 'w') as category_name_file:
	for name in names_categories:
		category_name_file.write(name + '\n')

with open('categories links.txt', 'w') as categories_links_file:
	for link_category in urls_categories:
		categories_links_file.write(link_category + '\n')

with open('categories links.txt', 'r') as categories_links_file:
	for classification in categories_links_file:
		classification_url = classification.strip()
		response1 = requests.get(classification_url)
		minestrone = BeautifulSoup(response1.text, 'lxml')
		body = minestrone.find('body')

		if response1.ok:

			# Verifie s'il y a une nouvelle page en fonction du nombre de livre

			result_items = minestrone.find('form', {'class': 'form-horizontal'}).find('strong').get_text(strip=True)
			if int(result_items) > 20 and int(result_items) < 1000:
				items_page_number = minestrone.find('form', {'class': 'form-horizontal'}).select('strong')[2].get_text(strip=True)
					
				if result_items > items_page_number :
					to_next_page()

			# Récupère tous les livres d'une catégorie

			articles = body.findAll('h3')
			for link in articles:
				book_url = link.find('a').get('href').replace('../../../', str(url) + 'catalogue/').replace('../../', str(url) + 'catalogue/')
				book_url_range.append(book_url)

			with open('links.txt', 'w') as urls_file:
				for product_url in book_url_range:
					urls_file.write(product_url + '\n')

		# Scrape l'ensemble des données d'un livre

			with open('links.txt', 'r') as urls_file:
				with open('travel_category.csv', 'w') as travel_file:
					travel_file.write('product_page_url, universal_ product_code (upc), title, price_including_tax, price_excluding_tax, number_available, product_description, category, review_rating, image_url,\n')

					for product_unity in urls_file:
						url_product_unity = product_unity.strip()
						response2 = requests.get(url_product_unity)

						if response2.ok:
							borsch = BeautifulSoup(response2.text, 'lxml')
							body2 = borsch.find('body')
							scrape_book_data()

							#picture_url_range.append(image_url)
							#for pic in picture_url_range:
								#pic_data = requests.get(pic).text
									
						"""
						output_file.write(url_product_unity + ', ' + universal_product_code + ', ' + title + ', ' + price_including_tax + ', ' + price_excluding_tax + ', ' + number_available + ', ' + product_description + ', ' + category + ', ' + review_rating + ', ' + image_url + '\n')

						"""