import requests
import json
import textdistance
from bs4 import BeautifulSoup

payload = []

# In future check a file from S3
validStores = ["Kmart", "David Jones", "Big W", "Target", "Dymocks", "Myer"]

########filter out productBrand name in productName



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
    json = {
        "store": store,
        "name": productName,
        "brand": productBrand,
        "price": price,
        "link": link
    }
    return json

headers = requests.utils.default_headers()
headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
})

def checkDavidJones(query):
    davidJonesProducts = {}

    url = f"https://search.www.davidjones.com/search?w={query['name']}"
    product = createProductJSON("David Jones", "", "", "", url)
    maxSimilarity = 0

    request = requests.get(url, headers=headers)
    soup = BeautifulSoup(request.content, "lxml")

    stylesLink = "https://search.www.davidjones.com/htmlapi/?"

    for styleNumber in soup.findAll("p", {"class": "style-number"}):
        headers.update({
            "referer": url
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
            product = createProductJSON("Target", productName, productBrand, price, link)

        # davidJonesProducts[link] = (productName, productBrand, price)

    payload.append(product)

def checkBigW(query):
    bigwProducts = {}

    url = f"https://www.bigw.com.au/search?pageSize=144&q={query['name']}%3Arelevance#"
    product = createProductJSON("Big W", "", "", "", url)
    maxSimilarity = 0

    request = requests.get(url, headers=headers)
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

    payload.append(product)


def checkTarget(query):
    targetProducts = {}

    url = f"https://www.target.com.au/search?text={query['name']}"
    product = createProductJSON("Target", "", "", "", url)
    maxSimilarity = 0

    request = requests.get(url, headers=headers)
    soup = BeautifulSoup(request.content, "lxml")

    for tag in soup.findAll("div", {"class": "detail"}):
        link = "https://www.target.com.au" + tag.find("a")["href"].strip()
        productName = ""
        productBrand = ""

        if "-" in tag.find("a")["title"].strip():
            metadata = tag.find("a")["title"].strip().split("-")
            productBrand = metadata.pop().strip()
            productName = "-".join(metadata).strip()
        else:
            ## TODO:
            print(tag.find("a")["title"].strip())
        price = tag.find("span", {"class": "price-regular price"}).text.strip()

        updateSimilarity = checkSimilarity(productName, productBrand, query, maxSimilarity)
        if updateSimilarity:
            maxSimilarity = updateSimilarity
            product = createProductJSON("Target", productName, productBrand, price, link)

       # targetProducts[link] = (productName, productBrand, price)

    payload.append(product)



def checkDymocks(query):
    pageNum = 1
    dymocksProducts = {}

    product = createProductJSON("Dymocks", "", "", "", "")
    maxSimilarity = 1

    while (maxSimilarity > 0.8):
        maxSimilarity = 0
        request = requests.get(f"https://www.dymocks.com.au/books/page-{pageNum}/?term={query['name']}&npp=96", headers=headers)
        soup = BeautifulSoup(request.content, "lxml")

        for tag in soup.findAll("div", {"class": "product-tile"}):
            productBrand = tag.find("div", {"class": "product-tile-desc product-tile-author"})["title"].strip()
            productName = tag.find("a", {"class": "product-tile-title product-title"})["title"].strip()
            link = "https://www.dymocks.com.au" + tag.find("a", {"class": "product-tile-title product-title"})["href"].strip()
            price = tag.find("div", {"class": "product-tile-price"}).text.strip()

            updateSimilarity = checkSimilarity(productName, productBrand, query, maxSimilarity)
            if updateSimilarity:
                maxSimilarity = updateSimilarity
                if product["price"] == "":
                    product = createProductJSON("Dymocks", productName, productBrand, price, link)
                elif product["price"] > price:
                    product = createProductJSON("Dymocks", productName, productBrand, price, link)

            # dymocksProducts[link] = (productName, productBrand, price)

        pageNum += 1

    payload.append(product)


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

    payload.append(product)



def checkKmart(query):
    kmartProducts = {}

    url = f"https://www.kmart.com.au/webapp/wcs/stores/servlet/SearchDisplay?searchTerm={query['name']}&categoryId=&storeId=10701&catalogId=10102&langId=-1&beginIndex=0&sType=SimpleSearch&resultCatEntryType=2&showResultsPage=true&searchSource=Q&pageView=#.plp-wrapper"
    product = createProductJSON("Kmart", "", "", "", url)
    maxSimilarity = 0

    # Since Kmart has the anti-scraping software by Incapsula the splinter library
    # must be used to collect the HTML
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--incognito")

    browser.get(url)

    soup = BeautifulSoup(browser.page_source, "lxml")

    for tag in soup.findAll("div", {"class": "product-details"}):
        productBrand = ""
        productName = tag.find("p", {"class": "title"}).text.strip()
        price = tag.find("span", {"class": "price"}).text.strip()
        link = "https://www.kmart.com.au" + tag.find_parent("div").find("a")["href"].strip()

        if " - Book" in productName:
            productName = productName.replace(" - Book", "")

        if "by" in productName:
            metadata = productName.split(" by ")
            productBrand = metadata.pop().strip()
            productName = " by ".join(metadata).strip()

        updateSimilarity = checkSimilarity(productName, productBrand, query, maxSimilarity)
        if updateSimilarity:
            maxSimilarity = updateSimilarity
            product = createProductJSON("Kmart", productName, productBrand, price, link)

        # kmartProducts[link] = (productName, price)

    browser.quit()
    payload.append(product)



def checkPetBarn(query):
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

    payload.append(product)


query = {'name': 'kangaroo and pumpkin roll 2kg', "brand": "prime100"}



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

    payload.append(product)



def checkPETstock(query):
    petStockProducts = {}

    pageNum = 1
    url = f"https://www.petstock.com.au/pet/search/{query['name']}/page/{pageNum}"
    product = createProductJSON("PETstock", "", "", "", url)
    maxSimilarity = 0
    pageExists = True

    while pageExists:
        pageExists = False
        url = f"https://www.petstock.com.au/pet/search/{query['name']}/page/{pageNum}"
        request = requests.get(url, headers=headers)
        soup = BeautifulSoup(request.content, "lxml")

        for tag in soup.findAll("div", {"class": "product"}):
            pageExists = True
            productBrand = ""
            productName = tag.find("a", {"class": "desc"}).text.strip()
            price = "$" + tag.find("meta", {"itemprop": "price"})["content"].strip()
            link = "https://www.petstock.com.au" + tag.find("a", {"class": "desc"})["href"].strip()

            updateSimilarity = checkSimilarity(productName, productBrand, query, maxSimilarity)
            if updateSimilarity:
                maxSimilarity = updateSimilarity
                product = createProductJSON("PETstock", productName, productBrand, price, link)

            # petStockProducts[link] = (productName, price)

        pageNum += 1

    payload.append(product)



def checkHabitatPets(query):
    habitatPetsProducts = {}

    url = f"https://www.habitatpets.com.au/pages/search-results-page?q={query['name']}+rolls&page=16"
    product = createProductJSON("Habitat Pets", "", "", "", url)
    maxSimilarity = 0
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--incognito")

    browser.get(url)
    soup = BeautifulSoup(browser.page_source, "lxml")

    for tag in soup.findAll("li", {"class": "snize-product"}):
        productBrand = ""
        productName = tag.find("span", {"class": "snize-title"}).text.strip()
        link = tag.find("a")["href"].strip()
        price = None

        if tag.find("span", {"class": "snize-price money"}) is None:
            price = tag.find("span", {"class": "snize-price snize-price-with-discount money"}).text.strip()
        else:
            price = tag.find("span", {"class": "snize-price money"}).text.strip()

        updateSimilarity = checkSimilarity(productName, productBrand, query, maxSimilarity)
        if updateSimilarity:
            maxSimilarity = updateSimilarity
            product = createProductJSON("Habitat Pets", productName, productBrand, price, link)

    browser.quit()
    payload.append(product)


#
def checkStore(store, query):

    if store == "David Jones":
        checkDavidJones(query)
    elif store == "Big W":
        checkBigW(query)
    elif store == "Dymocks":
        checkDymocks(query)
    elif store == "Myer":
        checkMyer(query)
    elif store == "Petbarn":
        checkPetBarn(query)
    elif store == "My Pet Warehouse":
        checkMyPetWarehouse(query)
    elif store == "PETstock":
        checkPETstock(query)
    elif store == "Habitat Pets":
        checkHabitatPets(query)


def initiateScrape(event, context):

    query = None

    # Only handle POST requests with data
    if event["requestContext"]["http"]["method"] != "POST":
        return {
            "statusCode": 400
        }

    try:
        query = event["body"]["query"]

    except:
        return {
            "statusCode": 400
        }

    # if a store name has an associated web scraper then check that website
    for store in event["body"]["stores"]:
        checkStore(store, query)

    return {
        "statusCode": 200,
        "body": payload
    }
