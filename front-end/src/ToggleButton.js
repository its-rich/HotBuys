import "./styles/styles.css";

export default function ToggleButton(props) {

    const storeName = props.store;

    // If this store is selected then change the background colour
    if (props.active) {
        return (
            <div
                className="toggleButton"
                onClick={(storeName) => props.updateSelectedStores(storeName)}
                style={{backgroundColor: "#46e7e7"}}
            >
                {storeName}
            </div>
        );
    };

    return (
        <div
            className="toggleButton"
            onClick={() => props.updateSelectedStores()}
        >
            {storeName}
        </div>
    );

};
