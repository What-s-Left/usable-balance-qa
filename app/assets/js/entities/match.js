import {Data} from "../helpers/data";

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
                const url = `/app/entities/match/api/feed?payee=${encodeURIComponent(payee)}&reference=${encodeURIComponent(reference)}&code=${encodeURIComponent(code)}`;

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
                const url = `/app/entities/match/api/entity?name=${encodeURIComponent(name)}`;

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
                const url = `/app/entities/match/api/ext-entity?name=${encodeURIComponent(name)}`;

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

        const entity_name_e = document.getElementById('entity_name');
        const entity_identifier_nzbn_e = document.getElementById('entity_identifier_nzbn');
        const entity_identifier_ird_e = document.getElementById('entity_identifier_ird');
        const entity_desc_e = document.getElementById('entity_desc');
        const entity_contact_address_e = document.getElementById('entity_contact_address');
        const entity_contact_postcode_e = document.getElementById('entity_contact_postcode');
        const entity_contact_phone_e = document.getElementById('entity_contact_phone');
        const entity_contact_website_e = document.getElementById('entity_contact_website');
        const entity_contact_country_e = document.getElementById('entity_contact_country');

        ext_entity_match_results.forEach(link => {
            link.addEventListener('click', event => {
                event.preventDefault(); // Prevent the default link action

                // Get the data attributes from the clicked link
                const entity_id = event.target.dataset.entityId
                const entity_name = event.target.dataset.entityName
                const entity_data = event.target.dataset

                const entity_identifier = JSON.parse(entity_data.entityIdentifier)
                const entity_classification = JSON.parse(entity_data.entityClassification)
                const entity_contact = JSON.parse(entity_data.entityContact)

                Data.set('entity_base', {
                    'name': entity_name,
                    'identifier': entity_identifier,
                    'classification': entity_classification,
                    'contact': entity_contact
                })

                var entity_identifier_tradingnames = []
                var entity_identifier_tradingnames_html = ''
                const entity_identifier_tradingnames_html_template= document.getElementById('entity_identifier_tradingname_value')
                var entity_identifier_tradingname_values = document.getElementById('entity_identifier_tradingname_values')
                var entity_identifier_tradingnames_html_placeholder = entity_identifier_tradingnames_html_template
                for (const identifier of entity_identifier)
                {
                    if (identifier.type == "TRADINGNAME")
                    {
                        entity_identifier_tradingnames_html_placeholder = entity_identifier_tradingnames_html_template.cloneNode(true)
                        entity_identifier_tradingnames_html_placeholder.removeAttribute('id')
                        entity_identifier_tradingnames_html_placeholder.classList.remove('visually-hidden')
                        entity_identifier_tradingnames_html_placeholder.classList.add('entity_trading_name')
                        entity_identifier_tradingnames_html_placeholder.innerHTML = identifier.value + "  <i class=\"bi bi-x-circle-fill\"></i>"
                        entity_identifier_tradingnames_html_placeholder.dataset.entityTradingName = identifier.value
                        entity_identifier_tradingnames.push(identifier.value)
                        entity_identifier_tradingnames_html += entity_identifier_tradingnames_html_placeholder.outerHTML
                    }
                }

                entity_identifier_tradingname_values.innerHTML = entity_identifier_tradingnames_html

                entity_name_e.value = entity_data.entityName
                entity_identifier_nzbn_e.value = entity_data.entityIdentifierNzbn
                entity_identifier_ird_e.value = entity_data.entityIdentifierIrd
                entity_desc_e.value = entity_data.entityClassificationBicDesc
                entity_contact_address_e.value = entity_data.entityContactAddress
                entity_contact_postcode_e.value = entity_data.entityContactPostcode
                entity_contact_phone_e.value = entity_data.entityContactPhone
                entity_contact_website_e.value = entity_data.entityContactWebsite
                //return EntitiesMatch.entity_match_payee(event.target, entity_id, payee)

                setTimeout(() => {
                      EntitiesMatch.setup_ext_entity_trading_name_listeners()
                  }, 100);
            });
        });

    }

    static async setup_ext_entity_trading_name_listeners(){

        const ext_entity_match_results = document.querySelectorAll('.entity_trading_name');

        ext_entity_match_results.forEach(link => {
            link.addEventListener('click', event => {
                event.preventDefault(); // Prevent the default link action
                event.target.remove()
            })
        })
    }

    static async entity_match_payee(element, entity_id, payee){

        const data = {
            "feed": [
                {
                    "type": "BANK:PAYEE",
                    "value": payee
                }
            ]
        };

        fetch('/app/entities/' + entity_id + '/match', {
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
