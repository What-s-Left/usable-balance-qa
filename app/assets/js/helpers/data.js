
class Data {
    static async get(key){
        const { value } = await Storage.get({ key });
        return JSON.parse(value);
    }

    static async set(key, value) {
        value = JSON.stringify(value);
        await Storage.set({key, value});
        return value;
    }

    static async del(key) {
        await Storage.remove({key});
        return true;
    }
}

export { Data };
