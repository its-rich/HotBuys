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
            price = str(item["price"]).strip()
            link = item["url"].strip()

            updateSimilarity = checkSimilarity(productName, productBrand, query, maxSimilarity)
            if updateSimilarity:
                maxSimilarity = updateSimilarity
                product = createProductJSON("My Pet Warehouse", productName, productBrand, price, link)

            # myPetWareHouseProducts[link] = (productName, productBrand, price)

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
        "body": checkMyPetWarehouse(request["body"]["query"])
    }
