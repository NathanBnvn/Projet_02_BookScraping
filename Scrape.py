import requests
from bs4 import BeautifulSoup

url_base = "http://books.toscrape.com/"
url1 = "http://books.toscrape.com/catalogue/category/books/classics_6/index.html"

response = requests.get(url1)
soup = BeautifulSoup(response.text, 'lxml')
body = soup.find('body')
book_url_range = []

if response.ok:
	articles = body.findAll('h3')
	for link in articles:
		book_url = link.find('a').get('href').replace('../../../', str(url_base) + 'catalogue/')
		book_url_range.append(book_url)

	with open('links.txt', 'w') as urls_file:
		for product_url in book_url_range:
			urls_file.write(product_url + '\n')

	with open('links.txt', 'r') as urls_file:
		with open('classics_category.csv', 'w') as output_file:
			output_file.write('product_page_url, universal_ product_code (upc), title, price_including_tax, price_excluding_tax, number_available, product_description, category, review_rating, image_url,\n')

			for product_unity in urls_file:
				url_product_unity = product_unity.strip()
				response2 = requests.get(url_product_unity)

				if response2.ok:
					borsch = BeautifulSoup(response2.text, 'lxml')
					body2 = borsch.find('body')

					table = body2.find('table')
					universal_product_code = table.select('td')[0].get_text(strip = True)
					price_excluding_tax = table.select('td')[2].get_text(strip = True)
					price_including_tax = table.select('td')[3].get_text(strip = True)
					number_available = table.select('td')[5].get_text(strip = True)
					review_rating = table.select('td')[6].get_text(strip = True)

					title = body2.find('h1').get_text(strip = True)
					image_url = body2.find('img').get('src').replace('../../', str(url_base))
					product_description = body2.find('article', {'class':'product_page'}).select('p')[3].get_text(strip = True)
					category = body2.find('ul', {'class':'breadcrumb'}).select('li')[2].find('a').get_text(strip = True)

					output_file.write(str(url_product_unity) + ', ' + str(universal_product_code) + ', ' + str(title) + ', ' + str(price_including_tax) + ', ' + str(price_excluding_tax) + ', ' + str(number_available) + ', ' + str(product_description) + ', ' + str(category) + ', ' + str(review_rating) + ', ' + str(image_url) + '\n')




