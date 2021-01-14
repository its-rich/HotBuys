import "./styles/styles.css";

export default function SearchBar() {

    const queryAPI = () => {

    };


    return (
        <div className="container">
            <div className="searchBar">
                <input
                    type="text"
                    placeholder="Search..."
                />

                <i
                    className="lni lni-search"
                    style={{
                        position: "relative",
                        fontSize:"36px",
                        left: "10px",
                        background: "blue",
                        width: "50px",
                        height: "50px", // 40px
                        borderRadius: "50%",
                        zIndex: "1"
                    }}
                    onClick={() => queryAPI()}
                >
                </i>

            </div>
        </div>
    );
};
