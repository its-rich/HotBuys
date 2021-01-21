import { createStore, applyMiddleware } from "redux";
import axios from "axios";

const checkboxReducer = (state = { stores: [], checked: [] }, action) => {
    switch (action.type) {
        case "UPDATE":
            let index = state.stores.indexOf(action.store);
            let prevChecked = state.checked[index];
            let newCheckedState = [...state.checked];
            newCheckedState[index] = !prevChecked;
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
                checked: checkedState
            }
            return initialState;

        default:
            return state;
    }
}

const getValidStoresMiddleware = (store) => (next) => (action) => {
    switch (action.type) {
        case "SET":
            axios.get("https://9pfmbtxb4f.execute-api.ap-southeast-2.amazonaws.com/default/getValidStores")
            .then((stores) => {
                store.dispatch({
                    type: "INITIALISE",
                    store: stores.data.stores
                })
            })
            return next(action)
        default:
            return next(action)
    }
}

const store = createStore(checkboxReducer, applyMiddleware(getValidStoresMiddleware));
store.dispatch({type:"SET"})

export default store;
