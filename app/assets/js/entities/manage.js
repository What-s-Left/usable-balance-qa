class EntitiesManage {
    static async setup_listeners(){

        const entity_create = document.getElementById('entities-entity-create');

        // Respond to search button being hit
        if (entity_create)
        {
            entity_create.addEventListener('click', event => {

                event.preventDefault();

                const name = document.getElementById('entity_name')
                const name_legal = document.getElementById('entity_name_legal')

                const data= {
                    "name": (name && name.value && name.value.trim() !== '') ? name.value : null,
                    "name_legal": (name_legal && name_legal.value && name_legal.value.trim() !== '') ? name_legal.value : null,
                    "desc": document.getElementById('entity_desc').value,
                    "country": document.getElementById('entity_country').value,
                    "identifier": [
                        {
                            "type": "BANK:PAYEE",
                            "value": document.getElementById('entity_identifier_payee').value
                        }
                    ]
                };

                const identifier_nzbn = document.getElementById('entity_identifier_nzbn')
                if (identifier_nzbn.value !== "")
                {
                    data["id_src"] = "GS1:" +identifier_nzbn.value
                    data["identifier"].push(
                        {
                            "type": "GS1",
                            "value": identifier_nzbn.value
                        }
                    )
                }

                const identifier_ird = document.getElementById('entity_identifier_ird')
                if (identifier_ird.value !== "")
                {
                    data["identifier"].push(
                        {
                            "type": "IRD",
                            "value": identifier_ird.value
                        }
                    )
                }

                const identifier_gst = document.getElementById('entity_identifier_gst_registered')
                if (identifier_gst.value == "Y")
                {
                    data["identifier"].push(
                        {
                            "type": "NZ:GST",
                            "value": identifier_gst.value
                        }
                    )
                }

                const contact_email = document.getElementById('entity_contact_email')
                if (contact_email.value !== "")
                {
                    data["contact"].push(
                        {
                            "type": "EMAIL",
                            "value": contact_email.value
                        }
                    )
                }

                const contact_phone = document.getElementById('entity_contact_phone')
                if (contact_phone.value !== "")
                {
                    data["contact"].push(
                        {
                            "type": "PHONE",
                            "value": contact_phone.value
                        }
                    )
                }

                const contact_website = document.getElementById('entity_contact_website')
                if (contact_website.value !== "")
                {
                    data["contact"].push(
                        {
                            "type": "WEBSITE",
                            "value": contact_website.value
                        }
                    )
                }

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
                    element.innerHTML = "<i class=\"bi bi-check-circle-fill\"></i> Entity Created"
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

            });
        }


    }

}

export { EntitiesManage };
