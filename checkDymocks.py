import json
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

    return json.dumps(product)

def initiateScrape(request):

    query = None

    # Necessary headers to allow CORS
    responseHeader = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "POST, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type",
        "Access-Control-Max-Age": "3600",
        "Access-Control-Allow-Credentials": "true",
        "Content-Type":"text/plain"
    }

    # Inform API requests/axios on what is allowed
    if request.method == "OPTIONS":
        return ("", 204, responseHeader)

    # Ensure only POST requests are allowed
    if request.method != "POST":
        return ("", 400, responseHeader)

    request = request.get_json()

    # Verify the payload received is formatted correctly
    try:
        if len(request["query"]) != 2:
            return ("", 400, responseHeader)
        request["query"]["name"]
        request["query"]["brand"]

    except:
        return ("", 400, responseHeader)

    return (checkDymocks(request["query"]), 200, responseHeader)
