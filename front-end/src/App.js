import "./styles/styles.css";
import { useState } from "react";
import SearchBar from "./SearchBar.js";
import axios from "axios";


function App() {

    const [selectedStores, setSelectedStores] = useState([]);
    const [scrapedResults, setScrapedResults] = useState([]);
    const [searchQueries, setSearchQueries] = useState([]);

    // If the store name is not in the array then add it
    // If the store name is in the array, then delete it
    const updateSelectedStores = (storeName) => {
        if (selectedStores.includes(storeName)) {
            selectedStores.splice(selectedStores.indexOf(storeName), 1);
        } else {
            selectedStores.push(storeName);
            setSelectedStores(selectedStores);
        }
    };

    // Send the user's search query to each of the APIs that correspond to their
    // selected stores
    const queryAPI = () => {
        const payload = {
            "query": scrapedResults[scrapedResults.length - 1]
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
            } catch (error) {
                resp = {
                    // Unable to check X store
                }
            } finally {
                results.push(resp);
            }

        });
        setScrapedResults(scrapedResults.push(results));
    };

    // USE REDUX AND DYNAMICALLY CREATE ALL CHECKBOXES

    return (
        <div className="App">
            <h1 style={{color: "#F13C20"}}>HotBuys</h1>
            <h2 style={{fontFamily: "Bradley Hand"}}>The easy way of finding the lowest prices, at your favourite stores</h2>
            <SearchBar
                queryAPI={() => queryAPI()}
                setSearchQueries={(query) => setSearchQueries(searchQueries.push(query))}
            />
            <input
                type="checkbox"
                className="vehicle1"
                value="Dymocks"
                onChange={(e) => updateSelectedStores(e.target.value)}
            />
            <input
                type="checkbox"
                className="vehicle2"
                value="BigW"
                onChange={(e) => updateSelectedStores(e.target.value)}
            />
            <label htmlFor="vehicle2">Dymocks</label>
        </div>
    );
};

export default App;
