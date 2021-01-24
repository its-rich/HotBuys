import "./styles/styles.css";

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

            {props.data.price.includes("$") && <div>
                {props.data.name}
            </div>}

            <div>
                <h2>{props.data.price}</h2>
            </div>

            {props.data.price.includes("$") &&
                <button onClick={() => openWebsite(props.data.link)}>Link to product</button>}

            {!props.data.price.includes("$") && !props.data.link !== "" &&
                <button onClick={() => openWebsite(props.data.link)}>Link to website</button>}
        </div>
    )

};
