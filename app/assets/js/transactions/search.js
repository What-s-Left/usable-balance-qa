import {Data} from "../helpers/data";
import {Funcs} from "../helpers/func";

class TransactionsSearch {
    static async setup_listeners(){

        const transactions_search_status = document.getElementById('transactions-search-status');

        // Respond to search button being hit
        if (transactions_search_status)
        {
            transactions_search_status.addEventListener('change', event => {

                event.preventDefault();

                Funcs.param_add('status', transactions_search_status.value);

            });
        }


        const transactions_search_keyword = document.getElementById('transactions-search-keyword');

        // Respond to search button being hit
        if (transactions_search_keyword)
        {
            transactions_search_keyword.addEventListener('click', event => {

                event.preventDefault();

                var transactions_search_filter_keyword = document.getElementById('transactions-search-keyword-text')

                Funcs.param_add('search', transactions_search_filter_keyword.value);

            });
        }

    }

}

export { TransactionsSearch };