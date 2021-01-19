import "./styles/styles.css";
import { useState } from "react";

export default function SearchBar(props) {

    const [productName, setProductName] = useState("");
    const [productBrand, setProductBrand] = useState("");

    const initiateSearch = () => {
        const query = {
            "name": productName,
            "brand": productBrand
        }
        props.queryAPI(query);
    };

    return (
        <div className="container">
            <div className="searchBar">
                <input
                    type="text"
                    placeholder="Search..."
                    value={productName}
                    onChange={(e) => setProductName(e.target.value)}
                />

                <i
                    className="lni lni-search"
                    style={{
                        position: "relative",
                        fontSize:"36px",
                        left: "10px",
                        // background: "blue",
                        width: "50px",
                        height: "50px", // 40px
                        borderRadius: "15px",
                        zIndex: "1",
                        margin: "10px",
                        top: "5px"
                    }}
                    onClick={() => initiateSearch()}
                >
                </i>

            </div>
        </div>
    );
};
