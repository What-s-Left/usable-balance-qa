class Data {
    static get(key){
        // Use sessionStorage.getItem to retrieve an item
        const value = sessionStorage.getItem(key);
        return JSON.parse(value);  // Parse the string to return as an object or other structure
    }

    static set(key, value) {
        // Convert value to a JSON string before storing
        value = JSON.stringify(value);
        sessionStorage.setItem(key, value);  // Use sessionStorage.setItem to store the item
        return value;
    }

    static del(key) {
        sessionStorage.removeItem(key);  // Use sessionStorage.removeItem to delete an item
        return true;
    }
}

export { Data };
