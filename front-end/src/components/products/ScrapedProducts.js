import "../../styles/styles.css";
import Product from "./Product.js";

// This component contains the search query that the user inputted, and all of
// information that the web scrapers returned in product cards
export default function ScrapedProducts(props) {

    return (
        <div className="productGroup">
            <h1>Product Name:<br/>{props.query.name}</h1>
            <h1>Brand Name:<br/>{props.query.brand}</h1>
            <div className="allProducts">
                {props.products.map((product, index) => {
                    return (
                        <Product key={props.products[index].link} data={product} />
                    )
                })}
            </div>
        </div>
    )
};
