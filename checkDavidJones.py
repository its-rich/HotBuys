import json
import requests
from bs4 import BeautifulSoup
from polyfuzz import PolyFuzz

headers = requests.utils.default_headers()
headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
})

def checkSimilarity(productName, productBrand, query, maxSimilarity):
    model = PolyFuzz("TF-IDF")
    model.match([productName], [query["name"]])
    table = model.get_matches()
    similarity = table.iloc[0]["Similarity"]

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

def checkDavidJones(query):
    davidJonesProducts = {}

    URL = f"https://search.www.davidjones.com/search?w={query['name']}"
    product = createProductJSON("David Jones", "", "", "", URL)
    maxSimilarity = 0

    request = requests.get(URL, headers=headers)
    soup = BeautifulSoup(request.content, "lxml")

    stylesLink = "https://search.www.davidjones.com/htmlapi/?"

    for styleNumber in soup.findAll("p", {"class": "style-number"}):
        headers.update({
            "referer": URL
        })
        stylesLink += "&SKU=" + styleNumber.text.strip().split(" ")[2].strip()

    request = requests.get(stylesLink, headers=headers)
    soup = BeautifulSoup(request.text, "lxml")

    for tag in soup.findAll("div", {"class": '\\"item-detail\\"'}):
        productBrand = tag.find("div", {"class": '\\"item-brand\\"'}).text.strip()
        productName = tag.find("a").text.strip()
        price = tag.find("span", {"itemprop": '\\"price\\"'}).text.strip()
        link = tag.find("a")["href"].replace("\\", "")
        link = link.replace("\"", "").strip()

        updateSimilarity = checkSimilarity(productName, productBrand, query, maxSimilarity)
        if updateSimilarity:
            maxSimilarity = updateSimilarity
            price = findLowestPrice(product["price"], price)

            if price is not False:
                product = createProductJSON("David Jones", productName, productBrand, price, link)

        # davidJonesProducts[link] = (productName, productBrand, price)

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

    return (checkDavidJones(request["query"]), 200, responseHeader)
