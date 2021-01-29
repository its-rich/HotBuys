import { createStore, applyMiddleware } from "redux";
import axios from "axios";

const checkboxReducer = (state = { stores: [], checked: [] }, action) => {
    switch (action.type) {

        // When a user selects a store that they want to search for a product,
        // update the checked array to ensure that this store is now visibly
        // selected and will be included in the search
        case "UPDATE":
            let i;
            for (i = 0; i < state.stores.length; i++) {
                if (state.stores[i].storeName === action.store) {
                    break;
                }
            }

            let prevChecked = state.checked[i];
            let newCheckedState = [...state.checked];
            newCheckedState[i] = !prevChecked;

            const newState = {
                stores: state.stores,
                checked: newCheckedState,
                groups: state.groups
            }

            return newState;

        // When the store is first initialised, set the state based on what
        // web scrapers are available for use
        case "INITIALISE":
            const allStores = action.store;
            const checkedState = new Array(allStores.length).fill(false);
            const initialState = {
                stores: allStores,
                checked: checkedState,
                groups: action.groups
            }

            return initialState;

        // case "ALL":

        default:
            return state;
    }
}

// I use a middleware to query an Amazon S3 lambda function which connects it to
// a JSON file in an Amazon S3 bucket - which contains all of the stores that a
// user can select from, the group the store belongs to, and the web scraper URL
const getValidStoresMiddleware = (store) => (next) => (action) => {
    switch (action.type) {
        case "SET":
            axios.get("https://9pfmbtxb4f.execute-api.ap-southeast-2.amazonaws.com/default/getValidStores")
            .then((resp) => {
                let stores = [];
                resp.data.options.forEach((group) => {
                    stores = stores.concat(group.stores);
                });

                store.dispatch({
                    type: "INITIALISE",
                    store: stores,
                    groups: resp.data.options
                })
            });

            return next(action)

        default:
            return next(action)
    }
}

const store = createStore(checkboxReducer, applyMiddleware(getValidStoresMiddleware));
store.dispatch({type:"SET"});

export default store;
