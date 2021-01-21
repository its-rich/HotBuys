import "./styles/styles.css";
import { useEffect, useState } from "react";
import SearchBar from "./SearchBar.js";
import ScrapedProducts from "./ScrapedProducts.js";
import axios from "axios";
import { useSelector, useDispatch } from "react-redux";

function App() {

    const [selectedStores, setSelectedStores] = useState([]);
    const [scrapedResults, setScrapedResults] = useState([]);
    const [searchQueries, setSearchQueries] = useState([]);
    const [isLoading, setIsLoading] = useState(false);
    const validStores = useSelector((state) => state.stores);
    const isChecked = useSelector((state) => state.checked);
    const dispatch = useDispatch();

    // If the store name is not in the array then add it
    // If the store name is in the array, then delete it
    const updateSelectedStores = (storeName) => {
        let newSelection = [...selectedStores];

        if (selectedStores.includes(storeName)) {
            newSelection.splice(newSelection.indexOf(storeName), 1)
        } else {
            newSelection.push(storeName);
        }

        setSelectedStores(newSelection);
        dispatch(
            {
                type: "UPDATE",
                store: storeName
            }
        );
    };

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

        const results = [];
        let resp;
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
                }

                results.push(resp);
            }

            // ORDER PRODUCTS BY LOWEST PRICE
            if (selectedStores[selectedStores.length - 1] === store) {
                results.sort((a, b) => {
                    return (a.price.slice(1) - b.price.slice(1))
                });
                let temp = [results, ...scrapedResults];
                setScrapedResults(temp);
                setIsLoading(false);
            }
        });
    };

    return (
        <div className="App">
            <h1 style={{color: "#F13C20"}}>HotBuys</h1>
            <h2 style={{fontFamily: "Bradley Hand"}}>The easy way of finding the lowest prices, at your favourite stores</h2>
            <SearchBar queryAPI={(query) => queryAPI(query)} isSelectedStores={selectedStores} />

            {validStores !== undefined && validStores.map((store, index) => {
                return (
                    <div key={store} >
                        <input
                            type="checkbox"
                            value={store}
                            checked={isChecked[index]}
                            onChange={() => updateSelectedStores(store)}
                        />
                        <label>{store}</label>
                    </div>
                )
            })}

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
