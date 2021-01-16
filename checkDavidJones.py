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
            product = createProductJSON("David Jones", productName, productBrand, price, link)

        # davidJonesProducts[link] = (productName, productBrand, price)

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
        "body": checkDavidJones(request["body"]["query"])
    }
