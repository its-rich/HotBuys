import "./styles/styles.css";
import { useState } from "react";
import { useSelector, useDispatch } from "react-redux";

export default function SearchBar(props) {

    const [productName, setProductName] = useState("");
    const [productBrand, setProductBrand] = useState("");
    const validStores = useSelector((state) => state.stores);
    const isChecked = useSelector((state) => state.checked);
    const dispatch = useDispatch();

    // If the store name is not in the array then add it
    // If the store name is in the array, then delete it
    const updateSelectedStores = (storeName) => {
        let newSelection = [...props.selectedStores];

        if (props.selectedStores.includes(storeName)) {
            newSelection.splice(newSelection.indexOf(storeName), 1)
        } else {
            newSelection.push(storeName);
        }

        props.setSelectedStores(newSelection);
        dispatch(
            {
                type: "UPDATE",
                store: storeName
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

                <div className="storeOptions" style={{ display:"flex"}}>
                    {validStores !== undefined && validStores.map((store, index) => {
                        return (
                            <div key={store.storeName} style={{}}>
                                {store.storeName}
                                <input
                                    style={{width: "50px"}}
                                    type="checkbox"
                                    value={store.URL}
                                    checked={isChecked[index]}
                                    onChange={() => updateSelectedStores(store.storeName)}
                                />
                            </div>
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
