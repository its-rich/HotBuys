import { createStore, applyMiddleware } from "redux";
import axios from "axios";

const checkboxReducer = (state = { stores: [], checked: [] }, action) => {
    switch (action.type) {
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
                checked: newCheckedState
            }

            return newState;

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
store.dispatch({type:"SET"})

export default store;
