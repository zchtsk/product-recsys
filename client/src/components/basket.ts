import {get, writable} from "svelte/store";
import { env } from '$env/dynamic/public';

const API_URL = env.PUBLIC_API_ENDPOINT

export const basket = writable({});

function mergeRecommendationsIntoCategories(data) {
    if (!data.also_like || !data.show_also_like) {
        return data.data;
    }
    
    // Create a deep copy of the original data
    const merged = JSON.parse(JSON.stringify(data.data));
    
    // Add recommendations to their respective categories
    Object.entries(data.also_like).forEach(([dept, recommendations]) => {
        // Mark recommendations with a special flag for styling
        const styledRecommendations = recommendations.map(rec => ({
            ...rec,
            is_recommendation: true,
            subs: [], // Recommendations don't have substitutes
            show_subs: false
        }));
        
        if (merged[dept]) {
            // Add to existing category
            merged[dept] = [...merged[dept], ...styledRecommendations];
        } else {
            // Create new category for recommendations
            merged[dept] = styledRecommendations;
        }
    });
    
    return merged;
}

export async function getNextBasket() {
    await fetch(`${API_URL}/basket/`).then(async (response) => {
        if (response.status == 200) {
            let json = await response.json();
            // Keep the default behavior - don't show recommendations by default
            basket.set(json)
        }
    })
}
