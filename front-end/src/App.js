import "./styles/styles.css";
import { useState } from "react";
import SearchBar from "./searchComponents/SearchBar.js";
import ScrapedProducts from "./ScrapedProducts.js";
import axios from "axios";
import { useSelector } from "react-redux";

function App() {

    const [selectedStores, setSelectedStores] = useState([]);
    const [scrapedResults, setScrapedResults] = useState([]);
    const [searchQueries, setSearchQueries] = useState([]);
    const [isLoading, setIsLoading] = useState(false);
    const isChecked = useSelector((state) => state.checked);

    // This will count the amount of stores that have actually been selected by
    // the user, by counting the number of true values in the isChecked array
    const numSelectedStores = (arr) => arr.reduce((a, v) => (v ? a + 1 : a), 0);

    // Send the user's search query to each of the APIs that correspond to their
    // selected stores
    const queryAPI = (query) => {
        setIsLoading(true);
        let newQueries = [query, ...searchQueries];
        setSearchQueries(newQueries);

        const payload = {
            "query": query
        }

        const headers = {
            headers: {
                "Content-Type": "application/json"
            }
        }

        let results = [];
        let resp;
        let currMin = -1;

        selectedStores.map( async (store) => {
            try {
                resp = await axios.post(`https://australia-southeast1-hotbuys.cloudfunctions.net/check${store}`, payload, headers);
                resp = resp.data;

            } catch (error) {
                resp = {
                    "store": store,
                    "price": "An error occurred. Please check the website yourself."
                }
            } finally {
                if (resp.price === "") {
                    resp.price = "Based on your input we couldn't find a match. Please check the website yourself."
                } else {
                    currMin = comparePrices(currMin, resp.price);
                }

                results.push(resp);
            }

            // Only when axios has fully returned the scraped results from each store
            // should the scraped results be updated
            if (results.length === numSelectedStores(isChecked)) {

                // Sort the products by: no match found then lowest to highest price
                results.sort((a, b) => {
                    return (a.price.slice(1) - b.price.slice(1))
                });

                if (currMin !== -1) {

                    // Create a deep clone
                    let updatedResults = JSON.parse(JSON.stringify(results));

                    // Find all products with the lowest price and then approriately
                    // set its key to be true
                    updatedResults.forEach((product) => {
                        if (product.price === currMin) {
                            product["isCheapest"] = true;
                        } else {
                            product["isCheapest"] = false;
                        }
                    });
                    results = updatedResults;
                }

                let updatedProducts = [results, ...scrapedResults];
                setScrapedResults(updatedProducts);
                setIsLoading(false);
            }
        });
    };

    // This function will return the lowest price out of 2 strings
    const comparePrices = (currMin, price) => {

        if (currMin === -1) {
            return price;
        }

        const currMinFloat = parseFloat(currMin.replace("$", ""));
        const priceFloat = parseFloat(price.replace("$", ""));

        if (priceFloat < currMinFloat) {
            return price;
        }

        return currMin;
    };

    return (
        <div className="App">
            <h1 style={{color: "#F13C20"}}>HotBuys</h1>
            <h2 className="trademark">The easy way of finding the lowest prices, at your favourite stores</h2>
            <SearchBar
                queryAPI={(query) => queryAPI(query)}
                selectedStores={selectedStores}
                setSelectedStores={(stores) => setSelectedStores(stores)}
            />

            {isLoading &&
                <h1 className="loading">
                    <span className="loadingLetter">L</span>
                    <span className="loadingLetter">O</span>
                    <span className="loadingLetter">A</span>
                    <span className="loadingLetter">D</span>
                    <span className="loadingLetter">I</span>
                    <span className="loadingLetter">N</span>
                    <span className="loadingLetter">G</span>
                    <span className="loadingLetter">.</span>
                    <span className="loadingLetter">.</span>
                    <span className="loadingLetter">.</span>
                </h1>
            }
            {scrapedResults.map((product, index) => {
                return (
                    <ScrapedProducts key={index} query={searchQueries[index]} products={product} />
                )
            })}

        </div>
    );
};

export default App;
