# What is this?
This website will search for the cheapest price listed online for a product at selected stores. It uses individual Google Cloud Functions to scrape information about the product at each store. The stores are found by interacting with a HTTP API Lambda Function to access the latest JSON in the Amazon S3 bucket, ultimately dictating what web scrapers are available.

## Features
* Can search for the price of a specific product
* Can see the cheapest price of a product at selected major retail stores

## How can I access it?
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

## Similarity Algorithm
After researching what string-searching/string-matching algorithms to use, I had first decided to use a normalized Levenshtein distance algorithm from the [textdistance](https://github.com/life4/textdistance) library. I only used this to compare the website's product name, to the user's input for the product's name.

However after wanting to see if the string-searching algorithm could be improved I discovered the [PolyFuzz](https://github.com/MaartenGr/PolyFuzz) framework. I then changed the product name similarity algorithm to use PolyFuzz's n-gram TF-IDF, which operates as such:

1. Split the string into 3 letter n-grams
2. Then use Scikit-learn's TfidfVectorize function to convert each item into a vector
3. Finally use Scikit-learn's cosine similarity function to determine the similarity between vectors

I also recognised the product brand could be matched using an edit distance based algorithm, as it is more suitable for shorter strings. I don't know how much leverage should be placed on brand similarity, compared to the product name, more testing is required, or whatever seems to most suitable. But for now I will only update the possible product if both the brand & product similarity >= the current possible product's similarities.

Through basic testing the strcmp95 function seems to perform the best for partially matching strings, which is used for comparing the website's product brand, to the user's input for the product's brand.
