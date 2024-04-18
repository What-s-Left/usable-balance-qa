class Funcs {
    static parse_hash()
    {
        const params = new Proxy(
            new URLSearchParams(window.location.hash.slice(1)), {
                get: (searchParams, prop) => searchParams.get(prop),
            }
        );

        return params
    }

    static parse_query_string()
    {
        const params = new Proxy(
            new URLSearchParams(window.location.search), {
                get: (searchParams, prop) => searchParams.get(prop),
            }
        );

        return params
    }

    static random_string(length)
    {
        var result           = '';
        var characters       = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
        var charactersLength = characters.length;
        for ( var i = 0; i < length; i++ ) {
            result += characters.charAt(Math.floor(Math.random() * charactersLength));
        }

        return result;
    }
}

export { Funcs };