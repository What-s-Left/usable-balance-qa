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
                  .then(async data => {
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
                      setTimeout(() => {
                          EntitiesMatch.setup_entity_result_listeners()
                      }, 100);
                  })
                  .catch(error => {
                    // Handle any errors
                    console.error('Error:', error);
                  })

            });
        }

        const ext_entity_search = document.getElementById('ext-entities-search');


        // Respond to search button being hit
        if (ext_entity_search)
        {
            ext_entity_search.addEventListener('click', event => {

                event.preventDefault();
                const name_e = document.getElementById('entity_name_search');

                // Get the values from the input fields
                const name = name_e.value;

                // Construct the URL with the parameters
                const url = `/app/entities/match/ext-entity?name=${encodeURIComponent(name)}`;

                const output_e = document.getElementById('ext-entities-match-results')
                // Make the AJAX GET request using Fetch
                fetch(url)
                  .then(response => response.text())
                  .then(data => {
                      // Handle the response data
                      output_e.innerHTML = data;
                      setTimeout(() => {
                          EntitiesMatch.setup_ext_entity_result_listeners()
                      }, 100);
                  })
                  .catch(error => {
                    // Handle any errors
                    console.error('Error:', error);
                  })

            });
        }
    }

    static async setup_entity_result_listeners(){

        const entity_match_results = document.querySelectorAll('.entity-transaction-match');

        const payee_e = document.getElementById('entity_identifier_payee');
        const reference_e = document.getElementById('entity_identifier_reference');
        const code_e = document.getElementById('entity_identifier_code');

        // Get the values from the input fields
        const payee = payee_e.value;
        const reference = reference_e.value;
        const code = code_e.value;

        entity_match_results.forEach(link => {
            link.addEventListener('click', event => {
                event.preventDefault(); // Prevent the default link action

                // Get the data attributes from the clicked link
                const entity_id = event.target.dataset.entityId

                return EntitiesMatch.entity_match_payee(event.target, entity_id, payee)
            });
        });

    }

    static async setup_ext_entity_result_listeners(){

        const ext_entity_match_results = document.querySelectorAll('.ext-entity-transaction-match');

        const name_e = document.getElementById('entity_name');
        const name_legal_e = document.getElementById('entity_name_legal');
        const nzbn_e = document.getElementById('entity_identifier_nzbn');

        ext_entity_match_results.forEach(link => {
            link.addEventListener('click', event => {
                event.preventDefault(); // Prevent the default link action

                // Get the data attributes from the clicked link
                const entity_id = event.target.dataset.entityId
                const entity_data = event.target.dataset

                console.log(entity_data)

                name_e.value = JSON.parse(entity_data.entityName).join(", ")
                name_legal_e.value = entity_data.entityNameLegal
                nzbn_e.value = entity_data.entityNzbn
                //return EntitiesMatch.entity_match_payee(event.target, entity_id, payee)
            });
        });

    }

    static async entity_match_payee(element, entity_id, payee){

        const data = {
            "identifier": [
                {
                    "type": "BANK:PAYEE",
                    "value": payee
                }
            ]
        };

        fetch('/app/entities/' + entity_id, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data) // Convert the JavaScript object to a JSON string
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            element.innerHTML = "<i class=\"bi bi-check-circle-fill\"></i> Matched Transaction(s)"
            element.classList.remove('btn-primary')
            element.classList.add('btn-success')
            element.classList.add('disabled')
            element.disabled = true
        })
        .then(data => {
            return true;
        })
        .catch(error => {
            console.error('Error:', error);
            return false;
        });


    }

}

export { EntitiesMatch };
