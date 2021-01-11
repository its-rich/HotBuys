import requests
import textdistance
from bs4 import BeautifulSoup

kmartBooks = {}

headers = requests.utils.default_headers()
headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
})

headers = {
   'accept':'*/*',
    'accept-encoding':'gzip, deflate, br',
    'accept-language':'en-GB,en;q=0.9,en-US;q=0.8,hi;q=0.7,la;q=0.6',
    'cache-control':'no-cache',
    'dnt':'1',
    'pragma':'no-cache',
    'referer':'https://www.google.com/',
    'sec-fetch-mode':'no-cors',
    'sec-fetch-site':'cross-site',
    'user-agent':"Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0",
 }

query = 'jk rowling'
url = f"https://www.kmart.com.au/webapp/wcs/stores/servlet/SearchDisplay?searchTerm={query}&categoryId=&storeId=10701&catalogId=10102&langId=-1&beginIndex=0&sType=SimpleSearch&resultCatEntryType=2&showResultsPage=true&searchSource=Q&pageView=#.plp-wrapper"
url = "https://www.kmart.com.au/"

a = requests.Session()
a.get(url)

request = a.get(url, headers=headers)
soup = BeautifulSoup(request.content, "html.parser")
print(soup)
for book in soup.findAll("div", {"class": "product product_box small-6 medium-4 large-4 columns clearfix col "}):
    print(book.find("div", {"class": "product-details"}))
    # print(book.find("p", {"class": "title"}))
    break

########filter out author name in title

# import requests
# import textdistance
# from bs4 import BeautifulSoup
#
# davidJonesBooks = {}
#
# headers = requests.utils.default_headers()
# headers.update({
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
# })
#
# query = 'jamie oliver'
# url = f"https://search.www.davidjones.com/search?w={query}"
#
# request = requests.get(url, headers=headers)
# soup = BeautifulSoup(request.content, "lxml")
#
# stylesLink = "https://search.www.davidjones.com/htmlapi/?"
#
# for styleNumber in soup.findAll("p", {"class": "style-number"}):
#     headers.update({
#         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
#         "referer": url
#     })
#     stylesLink += "&SKU=" + styleNumber.text.strip().split(" ")[2].strip()
#
# request = requests.get(stylesLink, headers=headers)
# soup = BeautifulSoup(request.text, "lxml")
#
# for book in soup.findAll("div", {"class": '\\"item-detail\\"'}):
#     title = book.find("a").text.strip()
#     price = book.find("span", {"itemprop": '\\"price\\"'}).text.strip()
#
#     davidJonesBooks[title] = price
#
# for key, value in davidJonesBooks.items():
#     print(key + " " + value)



# import requests
# import textdistance
# from bs4 import BeautifulSoup
#
# bigwBooks = {}
#
# headers = requests.utils.default_headers()
# headers.update({
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
# })
#
# query = 'jamie oliver'
# url = f"https://www.bigw.com.au/search?pageSize=144&q={query}%3Arelevance#"
#
# request = requests.get(url, headers=headers)
# soup = BeautifulSoup(request.content, "html.parser")
#
# # It doesn't display authors so this assumes every product relates to the author
# # thus only 1 dict is necessary
# for book in soup.findAll("div", {"class": "productDescription"}):
#     title = book.find("a").text.strip()
#
#     # The price is split up across 3 divs to display:
#     #               Currency ($) | Dollars | Cents
#     # So the text values across these divs must be combined
#     priceDiv = book.find("div", {"class": "online-price padding-right-zero"})
#     price = "$" + priceDiv.find("span", {"class": "priceClass"}).text.strip()
#     cents = priceDiv.find("span", {"class": "priceSuffix"})
#     if cents is not None:
#         price += "." + cents.text.strip()
#
#     bigwBooks[title] = price
#
# for key, value in bigwBooks.items():
#     print(key)



# import requests
# import textdistance
# from bs4 import BeautifulSoup
#
# targetBooks = {}
#
# headers = requests.utils.default_headers()
# headers.update({
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
# })
#
# query = 'jamie oliver'
# url = f"https://www.target.com.au/search?text={query}"
#
# request = requests.get(url, headers=headers)
# soup = BeautifulSoup(request.content, "html.parser")
#
# for book in soup.findAll("div", {"class": "detail"}):
#
#     if "-" in book.find("a")["title"].strip():
#         metadata = book.find("a")["title"].strip().split("-")
#         author = metadata.pop().strip()
#         title = "-".join(metadata).strip()
#     else:
#         pass
#     price = book.find("span", {"class": "price-regular price"}).text.strip()
#
#     if author in targetBooks:
#         targetBooks[author][title] = price
#     else:
#         targetBooks[author] = {title: price}
#
# for book in targetBooks['Jamie Oliver']:
#     print(targetBooks['Jamie Oliver'][book])
#     if textdistance.levenshtein.normalized_similarity(book.lower(), 'Harry Potter and the Half-Blood Prince') > 0.8:
#         print(price)


# import requests
# import textdistance
# from bs4 import BeautifulSoup
#
# authorSimilarity = 1
# pageNum = 1
# dymocksBooks = {}
#
# headers = requests.utils.default_headers()
# headers.update({
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
# })
#
# query = "j.k. rowling"
#
# while (authorSimilarity > 0.8):
#     authorSimilarity = 0
#     request = requests.get(f"https://www.dymocks.com.au/books/page-{pageNum}/?term={query}&npp=96", headers=headers)
#     soup = BeautifulSoup(request.content, "html.parser")
#
#     for book in soup.findAll("div", {"class": "product-tile"}):
#         author = book.find("div", {"class": "product-tile-desc product-tile-author"})["title"].strip()
#         title = book.find("a", {"class": "product-tile-title product-title"})["title"].strip()
#         price = book.find("div", {"class": "product-tile-price"}).text.strip()
#
#         similarity = textdistance.levenshtein.normalized_similarity(author.lower(), query)
#         if similarity > authorSimilarity:
#             authorSimilarity = similarity
#
#         if author in dymocksBooks:
#             dymocksBooks[author][title] = price
#         else:
#             dymocksBooks[author] = {title: price}
#
#     pageNum += 1
#
# for book in dymocksBooks['J.K. Rowling']:
#     if textdistance.levenshtein.normalized_similarity(book.lower(), 'Harry Potter and the Half-Blood Prince') > 0.8:
#         print(dymocksBooks['J.K. Rowling'][book])


# import requests
# import textdistance
# from bs4 import BeautifulSoup
#
# myerBooks = {}
# query = "J.K. Rowling"
#
# headers = requests.utils.default_headers()
# headers.update({
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
# })
#
# request = requests.get(f"https://www.myer.com.au/search?query={query}", headers=headers)
# soup = BeautifulSoup(request.content, "html.parser")
#
# for book in soup.findAll("div", {"class": "css-m4cs32"}):
#     author = book.find("span", {"data-automation": "product-brand"}).text.strip()
#     title = book.find("span", {"data-automation": "product-name"}).text.strip()
#     if book.find("p", {"data-automation": "product-price-now"}) is not None:
#         price = book.find("p", {"data-automation": "product-price-now"}).findAll("span")[1].text.strip()
#     else:
#         price = book.find("p", {"data-automation": "product-price-was"}).findAll("span")[1].text.strip()
#
#     if author in myerBooks:
#         myerBooks[author][title] = price
#     else:
#         myerBooks[author] = {title: price}
#
#
# for book in myerBooks['J.K. Rowling']:
#     print(myerBooks['J.K. Rowling'][book])
#     # print(book + str(textdistance.levenshtein.normalized_similarity(book.lower(), 'Harry Potter and the Half-Blood Prince')))
#     if textdistance.levenshtein.normalized_similarity(book.lower(), 'Harry Potter and the Half-Blood Prince') > 0.8:
#         print(myerBooks['J.K. Rowling'][book])
