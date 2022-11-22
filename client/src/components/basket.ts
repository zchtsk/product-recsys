import {get, writable} from "svelte/store";

export const basket = writable({});

export async function getNextBasket() {
    fetch(`http://127.0.0.1:5000/basket/`).then(async (response) => {
        if (response.status == 200) {
            let json = await response.json();
            basket.set(json)
        }
    })
}
