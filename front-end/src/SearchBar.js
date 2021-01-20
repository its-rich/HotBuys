import "./styles/styles.css";
import { useState } from "react";

export default function SearchBar(props) {

    const [productName, setProductName] = useState("");
    const [productBrand, setProductBrand] = useState("");

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
                <button
                    className="searchButton"
                    onClick={() => initiateSearch()}
                >
                Search <i className="lni lni-search-alt"></i>
                </button>
            </div>
        </div>
    );
};
