def checkSimilarity(productName, productCreator, query, maxSimilarity):
    similarity = textdistance.levenshtein.normalized_similarity(productName.lower(), query["name"])

    if similarity < 0.5:
        return False
    elif query["creator"] != "":
        similarity += textdistance.levenshtein.normalized_similarity(productName.lower(), query["creator"])

    if maxSimilarity <= similarity:
        return similarity
    else:
        return False

def createProductJSON(store, productName, productCreator, price, link):
    json = {
        "store": store,
        "name": productName,
        "creator": productCreator,
        "price": price,
        "link": link
    }
    return json

payload = []

query = {
    "name": "7 ways",
    "creator": "jamie oliver"
}

########filter out productCreator name in productName

import requests
import textdistance
from splinter import Browser
from bs4 import BeautifulSoup

kmartProducts = {}

url = f"https://www.kmart.com.au/webapp/wcs/stores/servlet/SearchDisplay?searchTerm={query['name']}&categoryId=&storeId=10701&catalogId=10102&langId=-1&beginIndex=0&sType=SimpleSearch&resultCatEntryType=2&showResultsPage=true&searchSource=Q&pageView=#.plp-wrapper"
product = createProductJSON("Kmart", "", "", "", url)
maxSimilarity = 0

# Since Kmart has the anti-scraping software by Incapsula the splinter library
# must be used to collect the HTML

browser = Browser("chrome", **executable_path ,incognito=True)
browser.visit(url)

soup = BeautifulSoup(browser.html, "lxml")

for tag in soup.findAll("div", {"class": "product-details"}):
    productCreator = ""
    productName = tag.find("p", {"class": "title"}).text.strip()
    price = tag.find("span", {"class": "price"}).text.strip()
    link = "https://www.kmart.com.au" + tag.find_parent("div").find("a")["href"].strip()

    if " - Book" in productName:
        productName = productName.replace(" - Book", "")

    if "by" in productName:
        metadata = productName.split(" by ")
        productCreator = metadata.pop().strip()
        productName = " by ".join(metadata).strip()

    updateSimilarity = checkSimilarity(productName, productCreator, query, maxSimilarity)
    if updateSimilarity:
        maxSimilarity = updateSimilarity
        product = createProductJSON("Kmart", productName, productCreator, price, link)

    kmartProducts[productName] = (price, link)

browser.quit()
payload.append(product)



# import requests
# import textdistance
# from bs4 import BeautifulSoup
#
# davidJonesProducts = {}
#
# url = f"https://search.www.davidjones.com/search?w={query['name']}"
# product = createProductJSON("David Jones", "", "", "", url)
# maxSimilarity = 0
#
# headers = requests.utils.default_headers()
# headers.update({
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
# })
#
# request = requests.get(url, headers=headers)
# soup = BeautifulSoup(request.content, "lxml")
#
# stylesLink = "https://search.www.davidjones.com/htmlapi/?"
#
# for styleNumber in soup.findAll("p", {"class": "style-number"}):
#     headers.update({
#         "referer": url
#     })
#     stylesLink += "&SKU=" + styleNumber.text.strip().split(" ")[2].strip()
#
# request = requests.get(stylesLink, headers=headers)
# soup = BeautifulSoup(request.text, "lxml")
#
# for tag in soup.findAll("div", {"class": '\\"item-detail\\"'}):
#     productCreator = tag.find("div", {"class": '\\"item-brand\\"'}).text.strip()
#     productName = tag.find("a").text.strip()
#     price = tag.find("span", {"itemprop": '\\"price\\"'}).text.strip()
#     link = tag.find("a")["href"].replace("\\", "")
#     link = link.replace("\"", "").strip()
#
#     updateSimilarity = checkSimilarity(productName, productCreator, query, maxSimilarity)
#     if updateSimilarity:
#         maxSimilarity = updateSimilarity
#         product = createProductJSON("Target", productName, productCreator, price, link)
#
#     # davidJonesProducts[link] = (productName, productCreator, price)
#
# payload.append(product)



# import requests
# import textdistance
# from bs4 import BeautifulSoup
#
# bigwProducts = {}
#
# url = f"https://www.bigw.com.au/search?pageSize=144&q={query['name']}%3Arelevance#"
# product = createProductJSON("Big W", "", "", "", url)
# maxSimilarity = 0
#
# headers = requests.utils.default_headers()
# headers.update({
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
# })
#
# request = requests.get(url, headers=headers)
# soup = BeautifulSoup(request.content, "lxml")
#
# # It doesn't display productCreators so this assumes every product relates to the productCreator
# # thus only 1 dict is necessary
# for tag in soup.findAll("div", {"class": "productDescription"}):
#     productName = tag.find("a").text.strip()
#     link = "https://www.bigw.com.au" + tag.find("h4").find("a")["href"].strip()
#
#     # The price is split up across 3 divs to display:
#     #               Currency ($) | Dollars | Cents
#     # So the text values across these divs must be combined
#     priceDiv = tag.find("div", {"class": "online-price padding-right-zero"})
#     price = "$" + priceDiv.find("span", {"class": "priceClass"}).text.strip()
#     cents = priceDiv.find("span", {"class": "priceSuffix"})
#     if cents is not None:
#         price += "." + cents.text.strip()
#
#     updateSimilarity = checkSimilarity(productName, "", query, maxSimilarity)
#     if updateSimilarity:
#         maxSimilarity = updateSimilarity
#         product = createProductJSON("Big W", productName, "", price, link)
#
#    # bigwProducts[link] = (productName, "", price)
#
# payload.append(product)



# import requests
# import textdistance
# from bs4 import BeautifulSoup
#
# targetProducts = {}
#
# url = f"https://www.target.com.au/search?text={query['name']}"
# product = createProductJSON("Target", "", "", "", url)
# maxSimilarity = 0
#
# headers = requests.utils.default_headers()
# headers.update({
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
# })
#
# request = requests.get(url, headers=headers)
# soup = BeautifulSoup(request.content, "lxml")
#
# for tag in soup.findAll("div", {"class": "detail"}):
#     link = "https://www.target.com.au" + tag.find("a")["href"].strip()
#     productName = ""
#     productCreator = ""
#
#     if "-" in tag.find("a")["title"].strip():
#         metadata = tag.find("a")["title"].strip().split("-")
#         productCreator = metadata.pop().strip()
#         productName = "-".join(metadata).strip()
#     else:
#         ## TODO:
#         print(tag.find("a")["title"].strip())
#     price = tag.find("span", {"class": "price-regular price"}).text.strip()
#
#     updateSimilarity = checkSimilarity(productName, productCreator, query, maxSimilarity)
#     if updateSimilarity:
#         maxSimilarity = updateSimilarity
#         product = createProductJSON("Target", productName, productCreator, price, link)
#
#    # targetProducts[link] = (productName, productCreator, price)
#
# payload.append(product)


# import requests
# import textdistance
# from bs4 import BeautifulSoup
#
# pageNum = 1
# dymocksProducts = {}
#
# product = createProductJSON("Dymocks", "", "", "", "")
# maxSimilarity = 1
#
# headers = requests.utils.default_headers()
# headers.update({
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
# })
#
# while (maxSimilarity > 0.8):
#     maxSimilarity = 0
#     request = requests.get(f"https://www.dymocks.com.au/books/page-{pageNum}/?term={query['name']}&npp=96", headers=headers)
#     soup = BeautifulSoup(request.content, "lxml")
#
#     for tag in soup.findAll("div", {"class": "product-tile"}):
#         productCreator = tag.find("div", {"class": "product-tile-desc product-tile-author"})["title"].strip()
#         productName = tag.find("a", {"class": "product-tile-title product-title"})["title"].strip()
#         link = "https://www.dymocks.com.au" + tag.find("a", {"class": "product-tile-title product-title"})["href"].strip()
#         price = tag.find("div", {"class": "product-tile-price"}).text.strip()
#
#         updateSimilarity = checkSimilarity(productName, productCreator, query, maxSimilarity)
#         if updateSimilarity:
#             maxSimilarity = updateSimilarity
#             print(price)
#             if product["price"] == "":
#                 product = createProductJSON("Myer", productName, productCreator, price, link)
#             elif product["price"] > price:
#                 product = createProductJSON("Myer", productName, productCreator, price, link)
#
#         # dymocksProducts[link] = (productName, productCreator, price)
#
#     pageNum += 1
#
# payload.append(product)

# import requests
# import textdistance
# from bs4 import BeautifulSoup
#
# myerProducts = {}
#
# url = f"https://www.myer.com.au/search?query={query['name']}"
# product = createProductJSON("Myer", "", "", "", url)
# maxSimilarity = 0
#
# headers = requests.utils.default_headers()
# headers.update({
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
# })
#
# request = requests.get(url, headers=headers)
# soup = BeautifulSoup(request.content, "lxml")
#
# for tag in soup.findAll("div", {"class": "css-m4cs32"}):
#     productCreator = tag.find("span", {"data-automation": "product-brand"}).text.strip()
#     productName = tag.find("span", {"data-automation": "product-name"}).text.strip()
#     link = "https://www.myer.com.au" + tag.find("a")["href"].strip()
#
#     if tag.find("p", {"data-automation": "product-price-now"}) is not None:
#         price = tag.find("p", {"data-automation": "product-price-now"}).findAll("span")[1].text.strip()
#     else:
#         price = tag.find("p", {"data-automation": "product-price-was"}).findAll("span")[1].text.strip()
#
#     updateSimilarity = checkSimilarity(productName, productCreator, query, maxSimilarity)
#     if updateSimilarity:
#         maxSimilarity = updateSimilarity
#         product = createProductJSON("Myer", productName, productCreator, price, link)
#
#     # myerProducts[link] = (productName, productCreator, price)
#
# payload.append(product)
