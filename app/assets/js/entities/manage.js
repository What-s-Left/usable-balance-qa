import {Data} from "../helpers/data";
import {EntitiesMatch} from "./match";

class EntitiesManage {
    static async setup_listeners(){

        const entity_tradingname_add = document.getElementById('entity_identifier_tradingname-add');

        if (entity_tradingname_add)
        {
            entity_tradingname_add.addEventListener('click', event => {
                event.preventDefault();


                const entity_tradingname = document.getElementById('entity_identifier_tradingname')

                if (entity_tradingname.value != "") {
                    const entity_identifier_tradingnames_html_template = document.getElementById('entity_identifier_tradingname_value')
                    var entity_identifier_tradingname_values = document.getElementById('entity_identifier_tradingname_values')
                    var entity_identifier_tradingnames_html_placeholder = entity_identifier_tradingnames_html_template.cloneNode(true)

                    entity_identifier_tradingnames_html_placeholder.removeAttribute('id')
                    entity_identifier_tradingnames_html_placeholder.classList.remove('visually-hidden')
                    entity_identifier_tradingnames_html_placeholder.classList.add('entity_trading_name')
                    entity_identifier_tradingnames_html_placeholder.innerHTML = entity_tradingname.value + "  <i class=\"bi bi-x-circle-fill\"></i>"
                    entity_identifier_tradingnames_html_placeholder.dataset.entityTradingName = entity_tradingname.value

                    entity_identifier_tradingname_values.innerHTML += entity_identifier_tradingnames_html_placeholder.outerHTML

                    setTimeout(() => {
                        EntitiesMatch.setup_ext_entity_trading_name_listeners()
                    }, 100);
                }
            });
        }

        const entity_create = document.getElementById('entities-entity-create');

        // Respond to search button being hit
        if (entity_create)
        {
            entity_create.addEventListener('click', event => {

                event.preventDefault();

                if (!document.getElementById('entity-form').checkValidity())
                {
                    console.log("INVALID!");
                    return false;
                }

                const entity_name_e = document.getElementById('entity_name');
                const entity_identifier_nzbn_e = document.getElementById('entity_identifier_nzbn');
                const entity_identifier_ird_e = document.getElementById('entity_identifier_ird');

                const entity_classification_expense_e = document.getElementById('entity_classification_expense');
                const entity_classification_revenue_e = document.getElementById('entity_classification_revenue');
                const entity_classification_gst_e = document.getElementById('entity_classification_gst_registered');

                const entity_desc_e = document.getElementById('entity_desc');

                const entity_contact_address_e = document.getElementById('entity_contact_address');
                const entity_contact_postcode_e = document.getElementById('entity_contact_postcode');
                const entity_contact_email_e = document.getElementById('entity_contact_email');
                const entity_contact_phone_e = document.getElementById('entity_contact_phone');
                const entity_contact_website_e = document.getElementById('entity_contact_website');
                const entity_contact_country_e = document.getElementById('entity_contact_country');

                var entity_base = Data.get('entity_base')

                var entity_name = entity_name_e.value
                var entity_id_src
                var entity_identifier = []

                /*
                // Clear Trading Names incase we didn't want some of them, and use the chips to define what to keep
                for (let i = entity_identifier.length - 1; i >= 0; i--) {
                    if (entity_identifier[i].type == "TRADINGNAME")
                    {
                        entity_identifier.splice(i, 1);
                    }
                }
                 */

                const ext_entity_identifier_trading_names = document.querySelectorAll('.entity_trading_name');

                ext_entity_identifier_trading_names.forEach(elem => {
                    entity_identifier.push({
                        "type": "TRADINGNAME",
                        "value": elem.dataset.entityTradingName
                    })
                })

                if (entity_identifier_nzbn_e.value != "")
                {
                    entity_id_src = "GS1:" + entity_identifier_nzbn_e.value
                    entity_identifier.push({
                        "type": "GS1",
                        "value": entity_identifier_nzbn_e.value
                    })
                }
                
                if (entity_identifier_ird_e.value != "")
                {
                    entity_identifier.push({
                        "type": "IRD",
                        "value": entity_identifier_ird_e.value
                    })
                }


                var entity_classification = entity_base.classification

                entity_classification.push({
                    "type": "CREDIT",
                    "value": entity_classification_revenue_e.value
                })

                entity_classification.push({
                    "type": "DEBIT",
                    "value": entity_classification_expense_e.value
                })

                if (entity_classification_gst_e.value != "")
                {
                    entity_classification.push({
                        "type": "NZ:GST",
                        "value": entity_classification_gst_e.value
                    })
                }


                var entity_contact = []

                if (entity_contact_address_e.value != "")
                {
                    entity_contact.push({
                        "type": "ADDRESS",
                        "value": entity_contact_address_e.value
                    })
                }

                if (entity_contact_postcode_e.value != "")
                {
                    entity_contact.push({
                        "type": "POSTCODE",
                        "value": entity_contact_postcode_e.value
                    })
                }

                if (entity_contact_phone_e.value != "")
                {
                    entity_contact.push({
                        "type": "PHONE",
                        "value": entity_contact_phone_e.value
                    })
                }

                if (entity_contact_email_e.value != "")
                {
                    entity_contact.push({
                        "type": "EMAIL",
                        "value": entity_contact_email_e.value
                    })
                }

                if (entity_contact_website_e.value != "")
                {
                    entity_contact.push({
                        "type": "WEBSITE",
                        "value": entity_contact_website_e.value
                    })
                }

                var entity_desc = entity_desc_e.value
                var entity_country = entity_contact_country_e.value


                const data= {
                    "id_src": entity_id_src,
                    "name": entity_name,
                    "desc": entity_desc,
                    "identifier": entity_identifier,
                    "classification": entity_classification,
                    "contact": entity_contact,
                    "country": entity_country
                };

                fetch('/app/entities/new', {
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
                    event.target.innerHTML = "<i class=\"bi bi-check-circle-fill\"></i> Entity Created"
                    event.target.classList.remove('btn-primary')
                    event.target.classList.add('btn-success')
                    event.target.classList.add('disabled')
                    event.target.disabled = true
                })
                .catch(error => {
                    console.error('Error:', error);
                    return false;
                });

            });
        }


    }

}

export { EntitiesManage };
