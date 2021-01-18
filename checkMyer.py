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

def checkMyer(query):
    myerProducts = {}

    url = f"https://www.myer.com.au/search?query={query['name']}"
    product = createProductJSON("Myer", "", "", "", url)
    maxSimilarity = 0

    request = requests.get(url, headers=headers)
    soup = BeautifulSoup(request.content, "lxml")

    for tag in soup.findAll("div", {"class": "css-m4cs32"}):
        productBrand = tag.find("span", {"data-automation": "product-brand"}).text.strip()
        productName = tag.find("span", {"data-automation": "product-name"}).text.strip()
        link = "https://www.myer.com.au" + tag.find("a")["href"].strip()

        if tag.find("p", {"data-automation": "product-price-now"}) is not None:
            price = tag.find("p", {"data-automation": "product-price-now"}).findAll("span")[1].text.strip()
        else:
            price = tag.find("p", {"data-automation": "product-price-was"}).findAll("span")[1].text.strip()

        updateSimilarity = checkSimilarity(productName, productBrand, query, maxSimilarity)
        if updateSimilarity:
            maxSimilarity = updateSimilarity
            product = createProductJSON("Myer", productName, productBrand, price, link)

        # myerProducts[link] = (productName, productBrand, price)

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

    return (checkMyer(request["query"]), 200, responseHeader)
