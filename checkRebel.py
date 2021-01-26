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

def findLowestPrice(currPrice, newPrice):

    if currPrice == "":
        return newPrice

    currPriceNum = float(currPrice.replace("$", ""))
    newPriceNum = float(newPrice.replace("$", ""))

    if currPriceNum < newPriceNum:
        return False

    return newPrice

def checkRebel(query):
    rebelProducts = {}
    pageNum = 0

    URL = f"https://www.rebelsport.com.au/search?q={query['name']}&start={pageNum}&sz=60"
    product = createProductJSON("rebel", "", "", "", URL)
    maxSimilarity = 0
    pageExists = True

    while pageExists:
        pageExists = False
        URL = f"https://www.rebelsport.com.au/search?q={query['name']}&start={pageNum}&sz=60"
        request = requests.get(URL, headers=headers)
        soup = BeautifulSoup(request.content, "lxml")

        for tag in soup.findAll("div", {"class": "product-tile gtm-product-click"}):
            pageExists = True
            productName = tag.find("a", {"class": "name-link"}).text.strip()
            productBrand = tag.find("div", {"class": "brand-name"})

            if productBrand is None:
                productBrand = ""
            else:
                productBrand = productBrand.text.strip()

            link = tag.find("a", {"class": "name-link"})["href"].strip()
            price = tag.find("span", {"class": "price-sales"}).text.replace("^", "").strip()

            updateSimilarity = checkSimilarity(productName, "", query, maxSimilarity)
            if updateSimilarity:
                maxSimilarity = updateSimilarity
                price = findLowestPrice(product["price"], price)

                if price is not False:
                    product = createProductJSON("rebel", productName, "", price, link)

            # rebel[link] = (productName, productBrand, price)

        pageNum += 60

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

    return (checkRebel(request["query"]), 200, responseHeader)
