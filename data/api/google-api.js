import {BASE_API_URL, PROGRAMMABLE_SE_ID_PARAM} from '../../secret.js'


// MAX_PAGES = "&lowRange=0&highRange=11"
const fs = require('fs');

async function query(item){
    let param = `&q=${item}`
    let res = await fetch(
        BASE_API_URL + param + PROGRAMMABLE_SE_ID_PARAM,
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
        let filePath = `./json/product.json`; // Specify the desired path and filename
        fs.writeFileSync(filePath, jsonString);
    } else {
        console.log('error')
    }

}
