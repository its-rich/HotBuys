import "./styles/styles.css";

export default function Product(props) {

    const openWebsite = (link) => {
        window.open(link);
    }

    return (
        <div className="product" key={props.data.store+props.data.link}>
            <div>
            {props.data.store}
            </div>

            {props.data.price.includes("$") && <div>
                {props.data.name}
            </div>}

            <div>
            {props.data.price}
            </div>

            {props.data.price.includes("$") &&
                <button onClick={() => openWebsite(props.data.link)}>Link to product</button>}

            {!props.data.price.includes("$") &&
                <button onClick={() => openWebsite(props.data.link)}>Link to website</button>}
        </div>
    )

};
