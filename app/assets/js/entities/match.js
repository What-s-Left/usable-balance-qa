class EntitiesMatch {
    static async setup_listeners(){

        const entity_feed_match_search = document.getElementById('entities-feed-match-search');

        // Respond to search button being hit
        if (entity_feed_match_search)
        {
            entity_feed_match_search.addEventListener('click', event => {

                event.preventDefault();
                const payee_e = document.getElementById('entity_identifier_payee');
                const reference_e = document.getElementById('entity_identifier_reference');
                const code_e = document.getElementById('entity_identifier_code');

                // Get the values from the input fields
                const payee = payee_e.value;
                const reference = reference_e.value;
                const code = code_e.value;

                // Construct the URL with the parameters
                const url = `/app/entities/match/feed?payee=${encodeURIComponent(payee)}&reference=${encodeURIComponent(reference)}&code=${encodeURIComponent(code)}`;

                const output_e = document.getElementById('entities-feed-match-results')
                // Make the AJAX GET request using Fetch
                fetch(url)
                  .then(response => response.text())
                  .then(data => {
                    // Handle the response data
                    output_e.innerHTML = data;
                  })
                  .catch(error => {
                    // Handle any errors
                    console.error('Error:', error);
                  });

            });
        }

        const entity_search = document.getElementById('entities-search');

        // Respond to search button being hit
        if (entity_search)
        {
            entity_search.addEventListener('click', event => {

                event.preventDefault();
                const name_e = document.getElementById('entity_name');

                // Get the values from the input fields
                const name = name_e.value;

                // Construct the URL with the parameters
                const url = `/app/entities/match/entity?name=${encodeURIComponent(name)}`;

                const output_e = document.getElementById('entities-match-results')
                // Make the AJAX GET request using Fetch
                fetch(url)
                  .then(response => response.text())
                  .then(data => {
                    // Handle the response data
                    output_e.innerHTML = data;
                  })
                  .catch(error => {
                    // Handle any errors
                    console.error('Error:', error);
                  });

            });
        }
    }

}

export { EntitiesMatch };
