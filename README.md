# What is this?
This website will search for the cheapest price listed online for a product at selected stores. It uses individual Google Cloud Functions to scrape information about the product at each store. The stores are found by interacting with a HTTP API Lambda Function to access the latest JSON in the Amazon S3 bucket, ultimately dictating what web scrapers are available.

## Features
* Can search for the price of a specific product
* Can see the cheapest price of a product at selected major retail stores

## How can I access it?
Compatible on all devices, but for the best experience, use a computer.

https://main.d2xbdqzx6twygh.amplifyapp.com/

## Stack
This was developed using ReactJS and is hosted on an AWS Amplify Cloud Server.

## What did I learn from this?
* Focused on improving my web development skills
* Gained familiarity with **AWS Lambda Functions**
* Gained familiarity with **Amazon S3**
* Developed a greater experience with **Google Cloud Functions**
* React Redux
* Sass

---

## Similarity Algorithm
To minimise the reliance on dependencies, I will only use the [FuzzyWuzzy](https://github.com/seatgeek/fuzzywuzzy) library for string-searching.

**What is the Levenshtein distance algorithm?**
* It is an edit distance based string-matching algorithm, counting the amount of character substitutions/insertions/deletions that are necessary to transform one string into another
* The Levenshtein distance algorithm has a time complexity of O(n * m)
* Easy to implement & multiple libraries use/offer it

**Comparing tested string-searching libraries:**
||Pros|Cons|
|-|-|-|
|[FuzzyWuzzy](https://github.com/seatgeek/fuzzywuzzy)|Already integrates string preprocessing|Only offers Levenshtein distance algorithm|
|[TextDistance](https://github.com/life4/textdistance)|Provides a wide variety of string-searching algorithms|Implemented algorithms are slow|
|[PolyFuzz](https://github.com/MaartenGr/PolyFuzz)|Provides different string-searching methods compared to the other 2|Relies upon big dependencies|
