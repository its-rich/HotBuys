import json
import requests
from fuzzywuzzy import fuzz
from bs4 import BeautifulSoup

headers = requests.utils.default_headers()
headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
})

def checkSimilarity(productName, productBrand, query, maxNameSimilarity, maxBrandSimilarity):
    nameSimilarity = fuzz.token_set_ratio(productName, query["name"])

    if query["brand"] != "":
        brandSimilarity = fuzz.partial_ratio(productBrand.lower(), query["brand"].lower())
    else:
        brandSimilarity = 0

    if maxNameSimilarity <= nameSimilarity and maxBrandSimilarity <= brandSimilarity:
        return (nameSimilarity, brandSimilarity)
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

    currPriceNum = float(currPrice.replace("$", "").replace(",", ""))
    newPriceNum = float(newPrice.replace("$", "").replace(",", ""))

    if currPriceNum < newPriceNum:
        return False

    return newPrice

def checkMyPetWarehouse(query):
    myPetWareHouseProducts = {}

    pageNum = 1
    url = f"https://results.mypetwarehouse.com.au/api/search?cid=109928273aef45ce8f9a7b655e10f7a1&q={query['name']}&page={pageNum}&ps=32&ss=&so="
    product = createProductJSON("My Pet Warehouse", "", "", "", f"https://www.mypetwarehouse.com.au/store/search.asp?q={query['name']}&ps=24&ss=&so=")

    maxNameSimilarity = 0
    maxBrandSimilarity = 0
    productHasUpdated = True

    while productHasUpdated:
        productHasUpdated = False
        url = f"https://results.mypetwarehouse.com.au/api/search?cid=109928273aef45ce8f9a7b655e10f7a1&q={query['name']}&page={pageNum}&ps=32&ss=&so="
        request = requests.get(url, headers=headers)
        soup = BeautifulSoup(request.content, "lxml")

        productJSON = json.loads(soup.text)

        for item in productJSON["p"]:
            productName = item["name"].strip()
            productBrand = item["brand"].strip()
            link = item["url"].strip()
            price = str(item["price"]).strip()

            if "$" not in price:
                price = "$" + price

            newSimilarity = checkSimilarity(productName, productBrand, query, maxNameSimilarity, maxBrandSimilarity)
            if newSimilarity:
                productHasUpdated = True
                maxNameSimilarity = newSimilarity[0]
                maxBrandSimilarity = newSimilarity[1]
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
