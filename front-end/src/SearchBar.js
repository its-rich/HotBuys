import "./styles/styles.css";
import { useState } from "react";
import { useSelector, useDispatch } from "react-redux";
import ToggleButton from "./ToggleButton.js";

export default function SearchBar(props) {

    const [productName, setProductName] = useState("");
    const [productBrand, setProductBrand] = useState("");
    const validStores = useSelector((state) => state.stores);
    const isChecked = useSelector((state) => state.checked);
    const dispatch = useDispatch();

    // If the store name is not in the array then add it
    // If the store name is in the array, then delete it
    const updateSelectedStores = (storeData) => {
        let newSelection = [...props.selectedStores];

        if (props.selectedStores.includes(storeData.URL)) {
            newSelection.splice(newSelection.indexOf(storeData.storeName), 1)
        } else {
            newSelection.push(storeData.URL);
        }

        props.setSelectedStores(newSelection);
        dispatch(
            {
                type: "UPDATE",
                store: storeData.storeName
            }
        );
    };

    const initiateSearch = () => {
        if (productName === "") {
            return;
        }

        const query = {
            "name": productName,
            "brand": productBrand
        }
        props.queryAPI(query);
    };

    return (
        <div className="container">
            <div className="searchBar">
                <div className="searchInputs">
                    <h2>Product Name:</h2>
                    <input
                        type="text"
                        placeholder="Search product name..."
                        value={productName}
                        onChange={(e) => setProductName(e.target.value)}
                    />

                    <h2>Product Brand:</h2>
                    <input
                        type="text"
                        placeholder="Search product brand..."
                        value={productBrand}
                        onChange={(e) => setProductBrand(e.target.value)}
                    />
                </div>

                <div>
                    {validStores !== undefined && validStores.map((store, index) => {
                        return (
                            <ToggleButton
                                key={store.URL}
                                updateSelectedStores={() => updateSelectedStores(store)}
                                store={store.storeName}
                                active={isChecked[index]}
                            />
                        )
                    })}
                </div>

                {props.selectedStores.length === 0 &&
                    <button className="searchButton" disabled>
                    Search <i className="lni lni-search-alt"></i>
                    </button>}
                {props.selectedStores.length !== 0 && <button
                    className="searchButton"
                    onClick={() => initiateSearch()}
                >
                Search <i className="lni lni-search-alt"></i>
                </button>}

            </div>
        </div>
    );
};
