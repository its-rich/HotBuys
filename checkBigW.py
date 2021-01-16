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

def checkBigW(query):
    bigwProducts = {}

    URL = f"https://www.bigw.com.au/search?pageSize=144&q={query['name']}%3Arelevance#"
    product = createProductJSON("Big W", "", "", "", URL)
    maxSimilarity = 0

    request = requests.get(URL, headers=headers)
    soup = BeautifulSoup(request.content, "lxml")

    # It doesn't display productBrands so this assumes every product relates to the productBrand
    # thus only 1 dict is necessary
    for tag in soup.findAll("div", {"class": "productDescription"}):
        productName = tag.find("a").text.strip()
        link = "https://www.bigw.com.au" + tag.find("h4").find("a")["href"].strip()

        # The price is split up across 3 divs to display:
        #               Currency ($) | Dollars | Cents
        # So the text values across these divs must be combined
        priceDiv = tag.find("div", {"class": "online-price padding-right-zero"})
        price = "$" + priceDiv.find("span", {"class": "priceClass"}).text.strip()
        cents = priceDiv.find("span", {"class": "priceSuffix"})
        if cents is not None:
            price += "." + cents.text.strip()

        updateSimilarity = checkSimilarity(productName, "", query, maxSimilarity)
        if updateSimilarity:
            maxSimilarity = updateSimilarity
            product = createProductJSON("Big W", productName, "", price, link)

       # bigwProducts[link] = (productName, "", price)

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
        "body": checkBigW(request["body"]["query"])
    }
