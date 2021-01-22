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

def checkMyPetWarehouse(query):
    myPetWareHouseProducts = {}

    pageNum = 1
    url = f"https://results.mypetwarehouse.com.au/api/search?cid=109928273aef45ce8f9a7b655e10f7a1&q={query['name']}&page={pageNum}&ps=32&ss=&so="
    product = createProductJSON("My Pet Warehouse", "", "", "", f"https://www.mypetwarehouse.com.au/store/search.asp?q={query['name']}&ps=24&ss=&so=")
    maxSimilarity = 0
    pageExists = True

    while pageExists:
        pageExists = False
        url = f"https://results.mypetwarehouse.com.au/api/search?cid=109928273aef45ce8f9a7b655e10f7a1&q={query['name']}&page={pageNum}&ps=32&ss=&so="
        request = requests.get(url, headers=headers)
        soup = BeautifulSoup(request.content, "lxml")

        productJSON = json.loads(soup.text)

        for item in productJSON["p"]:
            pageExists = True
            productName = item["name"].strip()
            productBrand = item["brand"].strip()
            link = item["url"].strip()
            price = str(item["price"]).strip()

            if "$" not in price:
                price = "$" + price

            updateSimilarity = checkSimilarity(productName, productBrand, query, maxSimilarity)
            if updateSimilarity:
                maxSimilarity = updateSimilarity
                price = findLowestPrice(product["price"], price)

                if price is not False:
                product = createProductJSON("My Pet Warehouse", productName, productBrand, price, link)

            # myPetWareHouseProducts[link] = (productName, productBrand, price)

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

    return (checkMyPetWarehouse(request["query"]), 200, responseHeader)
