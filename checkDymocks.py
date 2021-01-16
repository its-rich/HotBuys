import requests
import textdistance
from bs4 import BeautifulSoup

headers = requests.utils.default_headers()
headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
})

def checkSimilarity(productName, productBrand, query, maxSimilarity):
    similarity = textdistance.levenshtein.normalized_similarity(productName.lower(), query["name"])

    if similarity < 0.5:
        return False
    elif query["brand"] != "":
        similarity += textdistance.levenshtein.normalized_similarity(productName.lower(), query["brand"])

    if maxSimilarity <= similarity:
        return similarity
    else:
        return False

def createProductJSON(store, productName, productBrand, price, link):
    JSON = {
        "store": store,
        "name": productName,
        "brand": productBrand,
        "price": price,
        "link": link
    }
    return JSON

def checkDymocks(query):
    pageNum = 1
    dymocksProducts = {}

    product = createProductJSON("Dymocks", "", "", "", "")
    maxSimilarity = 1

    while (maxSimilarity > 0.8):
        maxSimilarity = 0
        request = requests.get(f"https://www.dymocks.com.au/books/page-{pageNum}/?term={query['name']}&npp=96", headers=headers)
        soup = BeautifulSoup(request.content, "lxml")

        for tag in soup.findAll("div", {"class": "product-tile"}):
            productBrand = tag.find("div", {"class": "product-tile-desc product-tile-author"})["title"].strip()
            productName = tag.find("a", {"class": "product-tile-title product-title"})["title"].strip()
            link = "https://www.dymocks.com.au" + tag.find("a", {"class": "product-tile-title product-title"})["href"].strip()
            price = tag.find("div", {"class": "product-tile-price"}).text.strip()

            updateSimilarity = checkSimilarity(productName, productBrand, query, maxSimilarity)
            if updateSimilarity:
                maxSimilarity = updateSimilarity
                if product["price"] == "":
                    product = createProductJSON("Dymocks", productName, productBrand, price, link)
                elif product["price"] > price:
                    product = createProductJSON("Dymocks", productName, productBrand, price, link)

            # dymocksProducts[link] = (productName, productBrand, price)

        pageNum += 1

    return product

def initiateScrape(request):

    query = None

    # Only handle POST requests with data
    if request.method != "POST":
        return {
            "Status Code": 400
        }

    request = request.get_json()

    try:
        if len(request["body"]) != 1 or len(request["body"]["query"]) != 2:
            return {
                "Status Code": 400
            }

    except:
        return {
            "Status Code": 400
        }

    return {
        "Status Code": 200,
        "body": checkDymocks(request["body"]["query"])
    }
