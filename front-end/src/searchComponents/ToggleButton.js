import "../styles/styles.css";

// This is a toggle button specifically for displaying which stores a user can
// search for a product, and allows them to include or exclude a specific store
// from their search
export default function ToggleButton(props) {

    const storeName = props.store;

    // If the user has clicked on this button, they have selected this store
    // so change the background colour
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

    // Otherwise display the default background colour for the button
    return (
        <div
            className="toggleButton"
            onClick={() => props.updateSelectedStores()}
        >
            {storeName}
        </div>
    );

};
