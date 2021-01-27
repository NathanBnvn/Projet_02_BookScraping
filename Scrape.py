import requests
import os, csv
from bs4 import BeautifulSoup
from os.path import basename

url = "http://books.toscrape.com/"


def scrape_categories():

	response = requests.get(url)
	soup = BeautifulSoup(response.text, 'lxml')

	# Récupère la liste des catégories dans le panel de navigation

	navigation_panel = soup.find('ul', {'class': 'nav nav-list'}).find('ul').select('a')

	for element_category in navigation_panel: 
		url_category = url + element_category.get('href')
		get_url_book(url_category)
		name_category = element_category.get_text(strip = True)
	return url_category

def get_url_book(url_category):

	link_book = url_category

	while link_book != None:
		response = requests.get(link_book)
		soup = BeautifulSoup(response.text, 'lxml')
		body = soup.find('body')

		next_page = soup.find('li', {'class': 'next'})

		articles = body.findAll('h3')
		for link in articles:
			book_url = link.find('a').get('href').replace('../../../', str(url) + 'catalogue/').replace('../../', str(url) + 'catalogue/')
			scrape_book_data(book_url)

		if next_page != None:
			next_page_element = next_page.find('a').get('href')
			link_book = url_category.replace('index.html', str(next_page_element))
		else:
			link_book == None
			break
	return

def scrape_book_data(book_url):

	response = requests.get(book_url)
	soup = BeautifulSoup(response.text, 'lxml')
	body = soup.find('body')

	table = body.find('table')
	universal_product_code = table.select('td')[0].get_text(strip = True)
	price_excluding_tax = table.select('td')[2].get_text(strip = True)
	price_including_tax = table.select('td')[3].get_text(strip = True)
	number_available = table.select('td')[5].get_text(strip = True)
	review_rating = table.select('td')[6].get_text(strip = True)

	title = body.find('h1').get_text(strip = True)
	image_url = body.find('img').get('src').replace('../../', str(url))
	product_description = body.find('article', {'class':'product_page'}).select('p')[3].get_text(strip = True)
	category = body.find('ul', {'class':'breadcrumb'}).select('li')[2].find('a').get_text(strip = True)

	book_data = {'book_url': book_url, 'universal_product_code': universal_product_code, 'price_including_tax': price_including_tax, 'price_excluding_tax':price_excluding_tax, 'number_available': number_available, 'review_rating':review_rating, 'title':title, 'image_url':image_url, 'product_description': product_description, 'category':category}
	
	if os.path.exists('./'+str(category)):
		save_datas(book_data)
		with open(os.path.join('./'+ str(category), '') + basename(image_url), 'wb') as picture_file:
			picture_file.write(requests.get(image_url).content)

	else:
		os.mkdir(str(category))
		save_datas(book_data)
		with open(os.path.join('./'+ str(category), '') + basename(image_url), 'wb') as picture_file:
			picture_file.write(requests.get(image_url).content)

	return book_data

def save_datas(book_data):
	category = book_data['category']

	if os.path.exists('./' + str(category) + '/'+ str(category) +'.csv'):
		with open(os.path.join('./'+ str(category), '') + str(category)+'.csv', 'a', encoding = 'utf-8') as data_file:
			data_file.write(book_data['book_url'] + ', ' + book_data['universal_product_code'] + ', ' + book_data['title'] + ', ' + book_data['price_including_tax'] + ', ' + book_data['price_excluding_tax'] + ', ' + book_data['number_available'] + ', ' + book_data['product_description'] + ', ' + book_data['category'] + ', ' + book_data['review_rating'] + ', ' + book_data['image_url'] + '\n')

	else:
		with open(os.path.join('./'+ str(category), '') + str(category)+'.csv', 'w', encoding = 'utf-8', newline= '') as data_file:
			data_file.write('product_page_url, universal_product_code (upc), title, price_including_tax, price_excluding_tax, number_available, product_description, category, review_rating, image_url')
			data_file.write(book_data['book_url'] + ', ' + book_data['universal_product_code'] + ', ' + book_data['title'] + ', ' + book_data['price_including_tax'] + ', ' + book_data['price_excluding_tax'] + ', ' + book_data['number_available'] + ', ' + book_data['product_description'] + ', ' + book_data['category'] + ', ' + book_data['review_rating'] + ', ' + book_data['image_url'] + '\n')

	return

scrape_categories()
