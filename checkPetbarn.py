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

def checkPetbarn(query):
    petbarnProducts = {}

    pageNum = 1
    url = f"https://www.petbarn.com.au/search?p={pageNum}&q={query['name']}"
    product = createProductJSON("Petbarn", "", "", "", url)

    maxSimilarity = 0
    pageExists = True

    while pageExists:
        pageExists = False
        url = f"https://www.petbarn.com.au/search?p={pageNum}&q={query['name']}"
        request = requests.get(url, headers=headers)
        soup = BeautifulSoup(request.content, "lxml")

        for tag in soup.findAll("li", {"class": "item last col-lg-3 col-md-3 col-xs-6"}):
            pageExists = True

            # first word in the title?
            productBrand = ""
            productName = tag.find("h2", {"class": "product-name"}).text.strip()
            price = tag.find("span", {"class": "regular-price"}).text.strip()
            link = tag.find("h2", {"class": "product-name"}).find("a")["href"].strip()

            updateSimilarity = checkSimilarity(productName, productBrand, query, maxSimilarity)
            if updateSimilarity:
                maxSimilarity = updateSimilarity
                product = createProductJSON("Petbarn", productName, productBrand, price, link)

            # petbarnProducts[link] = (productName, price)

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
        "body": checkPetbarn(request["body"]["query"])
    }
