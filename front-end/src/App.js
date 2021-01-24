import "./styles/styles.css";
import { useEffect, useState } from "react";
import SearchBar from "./SearchBar.js";
import ScrapedProducts from "./ScrapedProducts.js";
import axios from "axios";
import { useSelector } from "react-redux";

function App() {

    const [selectedStores, setSelectedStores] = useState([]);
    const [scrapedResults, setScrapedResults] = useState([]);
    const [searchQueries, setSearchQueries] = useState([]);
    const [isLoading, setIsLoading] = useState(false);
    const isChecked = useSelector((state) => state.checked);

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
                results.sort((a, b) => {
                    return (a.price.slice(1) - b.price.slice(1))
                });

                if (currMin !== -1) {
                    // Create a deep clone
                    let updatedResults = JSON.parse(JSON.stringify(results));

                    updatedResults.map((product) => {
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

    const comparePrices = (currMin, price) => {

        if (currMin === -1) {
            return price;
        }

        const currMinFloat = Math.parseFloat(currMin.replace("$", ""));
        const priceFloat = Math.parseFloat(price.replace("$", ""));

        if (priceFloat < currMinFloat) {
            return price;
        }

        return currMin;
    };

    // {validStores !== undefined && validStores.map((store, index) => {
    //     return (
    //         <div key={store} >
    //             <input
    //                 type="checkbox"
    //                 value={store}
    //                 checked={isChecked[index]}
    //                 onChange={() => updateSelectedStores(store)}
    //             />
    //             <label>{store}</label>
    //         </div>
    //     )
    // })}

    return (
        <div className="App">
            <h1 style={{color: "#F13C20"}}>HotBuys</h1>
            <h2 style={{fontFamily: "Bradley Hand"}}>The easy way of finding the lowest prices, at your favourite stores</h2>
            <SearchBar
                queryAPI={(query) => queryAPI(query)}
                selectedStores={selectedStores}
                setSelectedStores={(stores) => setSelectedStores(stores)}
            />

            {isLoading &&
                <h4>
                Loading
                </h4>
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
