import "../../styles/styles.css";

// This component displays a card containing all information that the webscraper
// could find about a product
export default function Product(props) {

    const openWebsite = (link) => {
        window.open(link);
    }

    return (
        <div className="product">
            <div>
                <h1>
                    {props.data.store}
                    {props.data.isCheapest !== undefined && props.data.isCheapest &&
                        <img alt="" src="https://img.icons8.com/officel/40/000000/fire-element.png"/>}
                </h1>
            </div>

            {/*
                If the webscraper was able to match a product then it will contain
                $, then it will also have a product name to display
            */}
            {props.data.price.includes("$") && <div>
                {props.data.name}
            </div>}

            <div>
                <h2>{props.data.price}</h2>
            </div>

            {props.data.price.includes("$") &&
                <button className="redirectButton" onClick={() => openWebsite(props.data.link)}>Link to product</button>}

            {/*
                If the webscraper wasn't able to match a product then it will
                return a URL to website with the query used, for the user to
                check themselves
            */}
            {!props.data.price.includes("$") && !props.data.link !== undefined &&
                <button className="redirectButton" onClick={() => openWebsite(props.data.link)}>Link to website</button>}
        </div>
    )

};
