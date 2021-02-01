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

def checkBigW(query):
    bigwProducts = {}
    query["name"] = query["name"].replace("&", "%26")

    URL = f"https://www.bigw.com.au/search?pageSize=144&q={query['name']}%3Arelevance#"
    product = createProductJSON("Big W", "", "", "", URL)
    maxNameSimilarity = 0
    maxBrandSimilarity = 0

    request = requests.get(URL, headers=headers)
    soup = BeautifulSoup(request.content, "lxml")

    # It doesn't display productBrands so this assumes every product relates to the productBrand
    # thus only 1 dict is necessary
    for tag in soup.findAll("div", {"class": "productDescription"}):
        productName = tag.find("a").text.strip()
        productBrand = ""
        link = "https://www.bigw.com.au" + tag.find("h4").find("a")["href"].strip()

        # The price is split up across 3 divs to display:
        #               Currency ($) | Dollars | Cents
        # So the text values across these divs must be combined
        priceDiv = tag.find("div", {"class": "online-price padding-right-zero"})
        price = "$" + priceDiv.find("span", {"class": "priceClass"}).text.strip()
        cents = priceDiv.find("span", {"class": "priceSuffix"})
        if cents is not None:
            price += "." + cents.text.strip()

        newSimilarity = checkSimilarity(productName, productBrand, query, maxNameSimilarity, maxBrandSimilarity)
        if newSimilarity:
            maxNameSimilarity = newSimilarity[0]
            maxBrandSimilarity = newSimilarity[1]
            price = findLowestPrice(product["price"], price)

            if price is not False:
                product = createProductJSON("Big W", productName, "", price, link)

        # bigwProducts[link] = (productName, "", price)

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

    return (checkBigW(request["query"]), 200, responseHeader)
