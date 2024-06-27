(()=>{"use strict";var e,t,n,a,i={388:(e,t,n)=>{n.a(e,(async(e,t)=>{try{var a=n(330),i=n(420),c=n(704);async function s(){await a.$.setup_listeners(),await i.j.setup_listeners(),await c.a.setup_listeners(),console.log("Usable Balance QA - Ready :)")}await s(),t()}catch(r){t(r)}}),1)},420:(e,t,n)=>{n.d(t,{j:()=>c});var a=n(465),i=n(330);class c{static async setup_listeners(){const e=document.getElementById("entity_identifier_tradingname-add");e&&e.addEventListener("click",(e=>{e.preventDefault();const t=document.getElementById("entity_identifier_tradingname");if(""!=t.value){const e=document.getElementById("entity_identifier_tradingname_value");let n=document.getElementById("entity_identifier_tradingname_values"),a=e.cloneNode(!0);a.removeAttribute("id"),a.classList.remove("visually-hidden"),a.classList.add("entity_trading_name"),a.innerHTML=t.value+'  <i class="bi bi-x-circle-fill"></i>',a.dataset.entityTradingName=t.value,n.innerHTML+=a.outerHTML,setTimeout((()=>{i.$.setup_ext_entity_trading_name_listeners()}),100)}}));const t=document.getElementById("entities-entity-create");t&&t.addEventListener("click",(e=>{if(e.preventDefault(),!document.getElementById("entity-form").checkValidity())return console.log("INVALID!"),!1;const t=document.getElementById("entity_name"),n=document.getElementById("entity_identifier_nzbn"),i=document.getElementById("entity_identifier_ird"),c=document.getElementById("entity_classification_expense"),s=document.getElementById("entity_classification_revenue"),r=document.getElementById("entity_classification_gst_registered"),o=document.getElementById("entity_desc"),d=document.getElementById("entity_contact_address"),l=document.getElementById("entity_contact_postcode"),u=document.getElementById("entity_contact_email"),y=document.getElementById("entity_contact_phone"),m=document.getElementById("entity_contact_website"),_=document.getElementById("entity_contact_country");let p=a.B.get("entity_base");null==p&&(p={name:null,identifier:[],classification:[],contact:[]});let v,E=t.value,g=[];document.querySelectorAll(".entity_trading_name").forEach((e=>{g.push({type:"TRADINGNAME",value:e.dataset.entityTradingName})})),""!=n.value&&(v="GS1:"+n.value,g.push({type:"GS1",value:n.value})),""!=i.value&&g.push({type:"IRD",value:i.value});let h=[];h.push({type:"CREDIT",value:s.value}),h.push({type:"DEBIT",value:c.value}),""!=r.value&&h.push({type:"NZ:GST",value:r.value});let f=[];""!=d.value&&f.push({type:"ADDRESS",value:d.value}),""!=l.value&&f.push({type:"POSTCODE",value:l.value}),""!=y.value&&f.push({type:"PHONE",value:y.value}),""!=u.value&&f.push({type:"EMAIL",value:u.value}),""!=m.value&&f.push({type:"WEBSITE",value:m.value});let I=o.value,B=_.value;const b={id_src:v,name:E,desc:I,identifier:g,classification:h,contact:f,country:B};fetch("/app/entities/new",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(b)}).then((t=>{if(!t.ok)throw new Error(`HTTP error! status: ${t.status}`);e.target.innerHTML='<i class="bi bi-check-circle-fill"></i> Entity Created',e.target.classList.remove("btn-primary"),e.target.classList.add("btn-success"),e.target.classList.add("disabled"),e.target.disabled=!0})).catch((e=>(console.error("Error:",e),!1)))}));const n=document.getElementById("entities-entity-update");n&&(i.$.setup_ext_entity_trading_name_listeners(),n.addEventListener("click",(e=>{if(e.preventDefault(),!document.getElementById("entity-form").checkValidity())return console.log("INVALID!"),!1;const t=document.getElementById("entity_id"),n=document.getElementById("entity_name"),a=document.getElementById("entity_identifier_nzbn"),i=document.getElementById("entity_identifier_ird"),c=document.getElementById("entity_classification_expense"),s=document.getElementById("entity_classification_revenue"),r=document.getElementById("entity_classification_gst_registered"),o=document.getElementById("entity_desc"),d=document.getElementById("entity_contact_address"),l=document.getElementById("entity_contact_postcode"),u=document.getElementById("entity_contact_email"),y=document.getElementById("entity_contact_phone"),m=document.getElementById("entity_contact_website"),_=document.getElementById("entity_contact_country");let p,v=t.value,E=n.value,g=[];document.querySelectorAll(".entity_trading_name").forEach((e=>{g.push({type:"TRADINGNAME",value:e.dataset.entityTradingName})})),""!=a.value&&(p="GS1:"+a.value,g.push({type:"GS1",value:a.value})),""!=i.value&&g.push({type:"IRD",value:i.value});let h=[];h.push({type:"CREDIT",value:s.value}),h.push({type:"DEBIT",value:c.value}),""!=r.value&&h.push({type:"NZ:GST",value:r.value});let f=[];""!=d.value&&f.push({type:"ADDRESS",value:d.value}),""!=l.value&&f.push({type:"POSTCODE",value:l.value}),""!=y.value&&f.push({type:"PHONE",value:y.value}),""!=u.value&&f.push({type:"EMAIL",value:u.value}),""!=m.value&&f.push({type:"WEBSITE",value:m.value});let I=o.value,B=_.value;const b={id_src:p,name:E,desc:I,identifier:g,classification:h,contact:f,country:B};fetch("/app/entities/"+v,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(b)}).then((t=>{if(!t.ok)throw new Error(`HTTP error! status: ${t.status}`);e.target.innerHTML='<i class="bi bi-check-circle-fill"></i> Entity Updated',e.target.classList.remove("btn-primary"),e.target.classList.add("btn-success")})).catch((e=>(console.error("Error:",e),!1)))})))}}},330:(e,t,n)=>{n.d(t,{$:()=>i});var a=n(465);class i{static async setup_listeners(){const e=document.getElementById("entities-feed-match-search");e&&e.addEventListener("click",(e=>{e.preventDefault();const t=document.getElementById("entity_identifier_payee"),n=document.getElementById("entity_identifier_reference"),a=document.getElementById("entity_identifier_code"),i=t.value,c=n.value,s=a.value,r=`/app/entities/match/api/feed?payee=${encodeURIComponent(i)}&reference=${encodeURIComponent(c)}&code=${encodeURIComponent(s)}`,o=document.getElementById("entities-feed-match-results");fetch(r).then((e=>e.text())).then((async e=>{o.innerHTML=e})).catch((e=>{console.error("Error:",e)}))}));const t=document.getElementById("entities-search");t&&(document.getElementById("entity_name").addEventListener("keypress",(function(e){"Enter"===e.key&&(e.preventDefault(),document.getElementById("entities-search").click())})),document.getElementById("entity_contact").addEventListener("keypress",(function(e){"Enter"===e.key&&(e.preventDefault(),document.getElementById("entities-search").click())})),t.addEventListener("click",(e=>{e.preventDefault();const t=document.getElementById("entity_name"),n=document.getElementById("entity_contact"),a=t.value,c=n.value,s=`/app/entities/match/api/entity?name=${encodeURIComponent(a)}&contact=${encodeURIComponent(c)}`,r=document.getElementById("entities-match-results");fetch(s).then((e=>e.text())).then((e=>{r.innerHTML=e,setTimeout((()=>{i.setup_entity_result_listeners()}),100)})).catch((e=>{console.error("Error:",e)}))})));const n=document.getElementById("ext-entities-search");n&&(document.getElementById("ext_entity_id").addEventListener("keypress",(function(e){"Enter"===e.key&&(e.preventDefault(),document.getElementById("ext-entities-search").click())})),document.getElementById("ext_entity_name").addEventListener("keypress",(function(e){"Enter"===e.key&&(e.preventDefault(),document.getElementById("ext-entities-search").click())})),document.getElementById("ext_entity_contact").addEventListener("keypress",(function(e){"Enter"===e.key&&(e.preventDefault(),document.getElementById("ext-entities-search").click())})),n.addEventListener("click",(e=>{e.preventDefault();const t=document.getElementById("ext_entity_id"),n=document.getElementById("ext_entity_name"),a=document.getElementById("ext_entity_contact"),c=t.value,s=n.value,r=a.value,o=`/app/entities/match/api/ext-entity?id=${encodeURIComponent(c)}&name=${encodeURIComponent(s)}&contact=${encodeURIComponent(r)}`,d=document.getElementById("ext-entities-match-results");fetch(o).then((e=>e.text())).then((e=>{d.innerHTML=e,setTimeout((()=>{i.setup_ext_entity_result_listeners()}),100)})).catch((e=>{console.error("Error:",e)}))})))}static async setup_entity_result_listeners(){const e=document.querySelectorAll(".entity-transaction-match"),t=document.getElementById("entity_identifier_payee"),n=document.getElementById("entity_identifier_reference"),a=document.getElementById("entity_identifier_code"),c=t.value;n.value,a.value,e.forEach((e=>{e.addEventListener("click",(e=>{e.preventDefault();const t=e.target.dataset.entityId;return i.entity_match_payee(e.target,t,c)}))}))}static async setup_ext_entity_result_listeners(){const e=document.querySelectorAll(".ext-entity-transaction-match"),t=document.getElementById("entity_name"),n=document.getElementById("entity_identifier_nzbn"),c=document.getElementById("entity_identifier_ird"),s=document.getElementById("entity_desc"),r=document.getElementById("entity_contact_address"),o=document.getElementById("entity_contact_postcode"),d=document.getElementById("entity_contact_phone"),l=document.getElementById("entity_contact_website");document.getElementById("entity_contact_country"),e.forEach((e=>{e.addEventListener("click",(e=>{e.preventDefault(),e.target.dataset.entityId;const u=e.target.dataset.entityName,y=e.target.dataset,m=JSON.parse(y.entityIdentifier),_=JSON.parse(y.entityClassification),p=JSON.parse(y.entityContact);a.B.set("entity_base",{name:u,identifier:m,classification:_,contact:p});var v=[],E="";const g=document.getElementById("entity_identifier_tradingname_value");var h=document.getElementById("entity_identifier_tradingname_values"),f=g;for(const e of m)"TRADINGNAME"==e.type&&((f=g.cloneNode(!0)).removeAttribute("id"),f.classList.remove("visually-hidden"),f.classList.add("entity_trading_name"),f.innerHTML=e.value+'  <i class="bi bi-x-circle-fill"></i>',f.dataset.entityTradingName=e.value,v.push(e.value),E+=f.outerHTML);h.innerHTML=E,t.value=y.entityName,n.value=y.entityIdentifierNzbn,c.value=y.entityIdentifierIrd,s.value=y.entityClassificationBicDesc,r.value=y.entityContactAddress,o.value=y.entityContactPostcode,d.value=y.entityContactPhone,l.value=y.entityContactWebsite,setTimeout((()=>{i.setup_ext_entity_trading_name_listeners()}),100)}))}))}static async setup_ext_entity_trading_name_listeners(){document.querySelectorAll(".entity_trading_name").forEach((e=>{e.addEventListener("click",(e=>{e.preventDefault(),e.target.remove()}))}))}static async entity_match_payee(e,t,n){const a={feed:[{type:"BANK:PAYEE",value:n}]};fetch("/app/entities/"+t+"/match",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(a)}).then((t=>{if(!t.ok)throw new Error(`HTTP error! status: ${t.status}`);e.innerHTML='<i class="bi bi-check-circle-fill"></i> Matched Transaction(s)',e.classList.remove("btn-primary"),e.classList.add("btn-success"),e.classList.add("disabled"),e.disabled=!0})).then((e=>!0)).catch((e=>(console.error("Error:",e),!1)))}}},465:(e,t,n)=>{n.d(t,{B:()=>a});class a{static get(e){const t=sessionStorage.getItem(e);return JSON.parse(t)}static set(e,t){return t=JSON.stringify(t),sessionStorage.setItem(e,t),t}static del(e){return sessionStorage.removeItem(e),!0}}},704:(e,t,n)=>{n.d(t,{a:()=>i});class a{static param_add(e,t){const n=new URL(window.location),a=new URLSearchParams(n.search);a.set(e,t),n.search=a.toString(),window.location.href=n.href}static parse_hash(){return new Proxy(new URLSearchParams(window.location.hash.slice(1)),{get:(e,t)=>e.get(t)})}static parse_query_string(){return new Proxy(new URLSearchParams(window.location.search),{get:(e,t)=>e.get(t)})}static random_string(e){for(var t="",n=0;n<e;n++)t+="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789".charAt(Math.floor(62*Math.random()));return t}}class i{static async setup_listeners(){const e=document.getElementById("transactions-search-status");e&&e.addEventListener("change",(t=>{t.preventDefault(),a.param_add("status",e.value)}));const t=document.getElementById("transactions-search-keyword");t&&t.addEventListener("click",(e=>{e.preventDefault();var t=document.getElementById("transactions-search-keyword-text");a.param_add("search",t.value)}))}}}},c={};function s(e){var t=c[e];if(void 0!==t)return t.exports;var n=c[e]={exports:{}};return i[e](n,n.exports,s),n.exports}e="function"==typeof Symbol?Symbol("webpack queues"):"__webpack_queues__",t="function"==typeof Symbol?Symbol("webpack exports"):"__webpack_exports__",n="function"==typeof Symbol?Symbol("webpack error"):"__webpack_error__",a=e=>{e&&e.d<1&&(e.d=1,e.forEach((e=>e.r--)),e.forEach((e=>e.r--?e.r++:e())))},s.a=(i,c,s)=>{var r;s&&((r=[]).d=-1);var o,d,l,u=new Set,y=i.exports,m=new Promise(((e,t)=>{l=t,d=e}));m[t]=y,m[e]=e=>(r&&e(r),u.forEach(e),m.catch((e=>{}))),i.exports=m,c((i=>{var c;o=(i=>i.map((i=>{if(null!==i&&"object"==typeof i){if(i[e])return i;if(i.then){var c=[];c.d=0,i.then((e=>{s[t]=e,a(c)}),(e=>{s[n]=e,a(c)}));var s={};return s[e]=e=>e(c),s}}var r={};return r[e]=e=>{},r[t]=i,r})))(i);var s=()=>o.map((e=>{if(e[n])throw e[n];return e[t]})),d=new Promise((t=>{(c=()=>t(s)).r=0;var n=e=>e!==r&&!u.has(e)&&(u.add(e),e&&!e.d&&(c.r++,e.push(c)));o.map((t=>t[e](n)))}));return c.r?d:s()}),(e=>(e?l(m[n]=e):d(y),a(r)))),r&&r.d<0&&(r.d=0)},s.d=(e,t)=>{for(var n in t)s.o(t,n)&&!s.o(e,n)&&Object.defineProperty(e,n,{enumerable:!0,get:t[n]})},s.o=(e,t)=>Object.prototype.hasOwnProperty.call(e,t),s(388)})();
//# sourceMappingURL=app.bundle.js.map