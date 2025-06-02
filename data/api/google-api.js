import {BASE_API_URL, PROGRAMMABLE_SE_ID_PARAM} from '../../secret.js'



// params search for top 10 relevant & safe pages from several typical online store fronts
// https://developers.google.com/custom-search/v1/reference/rest/v1/cse.siterestrict/list

const ADDITIONAL_PARAMS = `
    &lr=lang_en
    &dateRestrict=y[2]
    &num=10
    &safe=active
    &siteSearch=etsy.com&siteSearchFilter=i
`

const fs = require('fs');

async function query(item){
    let param = `&q=${item}`
    let res = await fetch(

        // api w/ its key + current search item + additional params + search ID for API
        BASE_API_URL + param + ADDITIONAL_PARAMS + PROGRAMMABLE_SE_ID_PARAM,
       {
        method: 'GET',
        headers: {
            // "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
            'Content-Type': 'application/json',
        },
       }
    )
    console.log(res)
    if (res.ok){
        let data = await res.json()
        const jsonString = JSON.stringify(data, null, 2); // The '2' adds indentation for readability
        let filePath = `./json/product.json`;
        fs.writeFileSync(filePath, jsonString);
    } else {
        console.log('error')
    }
}

async function test_query(item){
    let param = `&q=${item}`
    let res = await fetch(

        // api w/ its key + current search item + additional params + search ID for API
        BASE_API_URL + param + ADDITIONAL_PARAMS + PROGRAMMABLE_SE_ID_PARAM,
       {
        method: 'GET',
        headers: {
            // "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
            'Content-Type': 'application/json',
        },
       }
    )
    console.log(res)
    if (res.ok){
        let data = await res.json()
         try {
            const jsonData = JSON.stringify(data, null, 2);
            fs.writeFileSync('../json/api-output/test.json', jsonData, 'utf-8');
            console.log(`Data successfully written to ${filePath}`);
            } catch (error) {
                console.error(`An error occurred: ${error}`);
            }
        }
}

test_query('shoe')
