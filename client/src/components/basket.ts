import {get, writable} from "svelte/store";
import { env } from '$env/dynamic/public';

const API_URL = env.PUBLIC_API_ENDPOINT

export const basket = writable({});

export async function getNextBasket() {
    await fetch(`${API_URL}/basket/`).then(async (response) => {
        if (response.status == 200) {
            let json = await response.json();
            basket.set(json)
        }
    })
}
