import "./styles/styles.css";
import { useEffect, useState } from 'react';
import SearchBar from './SearchBar.js';


function App() {

    const [selectedStores, setSelectedStores] = useState([]);

    const updateSelectedStores = (storeName) => {
        if (selectedStores.includes(storeName)) {
            // delete it
        } else {
            selectedStores.push(storeName);
            setSelectedStores(selectedStores);
        }
    };

    return (
        <div className="App">
            <SearchBar />
            <input
                type="checkbox"
                id="vehicle1"
                className="vehicle1"
                value="Bike"
                onChange={() => updateSelectedStores()}
            />
            <label htmlFor="vehicle1"> I have a bike</label>
        </div>
    );
};

export default App;
