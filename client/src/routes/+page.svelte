<script>
    import {onMount} from "svelte";

    const get_basket = async () => {
        let response = await fetch('http://127.0.0.1:8000/basket/3');
        let json = await response.json();
        console.log(json)
        return json
    }

    let jsondata = {
        "data": {
            "beverages": [
                {
                    "product_id": 24759,
                    "product_name": "Club Soda",
                    "aisle_id": 77,
                    "department_id": 7,
                    "department_name": "beverages",
                    "id": 693,
                    "subs": []
                },
                {
                    "product_id": 8475,
                    "product_name": "Diet 12 Oz Ginger Ale",
                    "aisle_id": 77,
                    "department_id": 7,
                    "department_name": "beverages",
                    "id": 1422,
                    "subs": [
                        {
                            "product_id": 42731,
                            "product_name": "Original Citrus Sparkling Flavored Soda",
                            "aisle_id": 77,
                            "department_id": 7,
                            "department_name": "beverages"
                        },
                        {
                            "product_id": 31808,
                            "product_name": "Lemon-Lime 12 Pack Soda",
                            "aisle_id": 77,
                            "department_id": 7,
                            "department_name": "beverages"
                        },
                        {
                            "product_id": 47877,
                            "product_name": "Coke Zero",
                            "aisle_id": 77,
                            "department_id": 7,
                            "department_name": "beverages"
                        },
                        {
                            "product_id": 49198,
                            "product_name": "Zero Soda",
                            "aisle_id": 77,
                            "department_id": 7,
                            "department_name": "beverages"
                        },
                        {
                            "product_id": 12140,
                            "product_name": "Diet Soda",
                            "aisle_id": 77,
                            "department_id": 7,
                            "department_name": "beverages"
                        }
                    ]
                }
            ],
            "dairy eggs": [
                {
                    "product_id": 1263,
                    "product_name": "American Cheese Slices 12 Count",
                    "aisle_id": 21,
                    "department_id": 16,
                    "department_name": "dairy eggs",
                    "id": 1115,
                    "subs": [
                        {
                            "product_id": 22788,
                            "product_name": "Singles American Cheese Slices",
                            "aisle_id": 21,
                            "department_id": 16,
                            "department_name": "dairy eggs"
                        }
                    ]
                }
            ],
            "snacks": [
                {
                    "product_id": 14381,
                    "product_name": "Whole Grain Cheddar Baked Goldfish Crackers",
                    "aisle_id": 78,
                    "department_id": 19,
                    "department_name": "snacks",
                    "id": 1887,
                    "subs": []
                },
                {
                    "product_id": 18721,
                    "product_name": "Baked Rice and Corn Puffs, Aged White Cheddar",
                    "aisle_id": 107,
                    "department_id": 19,
                    "department_name": "snacks",
                    "id": 1402,
                    "subs": []
                }
            ]
        },
        "also_like": [
            {
                "product_id": 24852,
                "product_name": "Banana",
                "aisle_id": 24,
                "department_id": 4,
                "department_name": "produce"
            },
            {
                "product_id": 23909,
                "product_name": "2% Reduced Fat Milk",
                "aisle_id": 84,
                "department_id": 16,
                "department_name": "dairy eggs"
            },
            {
                "product_id": 16953,
                "product_name": "Creamy Peanut Butter",
                "aisle_id": 88,
                "department_id": 13,
                "department_name": "pantry"
            },
            {
                "product_id": 47141,
                "product_name": "Cola",
                "aisle_id": 77,
                "department_id": 7,
                "department_name": "beverages"
            },
            {
                "product_id": 5077,
                "product_name": "100% Whole Wheat Bread",
                "aisle_id": 112,
                "department_id": 3,
                "department_name": "bakery",
                "id": 53,
                "subs": []
            }
        ]
    }
    onMount(()=>{
        for (const [key, value] of Object.entries(jsondata["data"])){
            console.log(key)
        }
    })

</script>

<main class="h-screen">
    <!-- Navigation -->
    <div class="border py-5 pl-12">
        <p class="font-bold text-3xl text-gray-700">Product Recommender</p>
    </div>
    <!--Main Content-->
    <div class="max-w-6xl mx-auto">
        <div class="py-10 flex justify-center items-center gap-3">
            <p class="text-4xl tracking-tight text-center text-gray-800">Load a sample basket and see recommended
                options</p>
        </div>
        <!-- Generator -->
        <div class="flex justify-center">
            <button class="border border-gray-300 px-5 py-4 rounded-lg shadow-md flex items-center gap-2 active:translate-y-[1px] hover:shadow-lg">
                <div class="bg-teal-400 text-white rounded-full p-2">
                    <svg class="w-7 h-7" fill="none" stroke="currentColor" viewBox="0 0 24 24"
                         xmlns="http://www.w3.org/2000/svg">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                              d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z"></path>
                    </svg>
                </div>
                <p class="text-2xl text-gray-800">Choose random basket</p>
            </button>
        </div>
        <!-- Basket -->
        <div class="flex justify-center">
            <div class="px-4 sm:px-6 lg:px-8">

                <div class="mt-8 flex flex-col">
                    <div class="-my-2 -mx-4 overflow-x-auto sm:-mx-6 lg:-mx-8">
                        <div class="inline-block min-w-full py-2 align-middle md:px-6 lg:px-8">
                            <div class="overflow-hidden shadow ring-1 ring-black ring-opacity-5 md:rounded-lg">
                                <table class="min-w-full">
                                    <thead class="bg-white">
                                    <tr>
                                        <th scope="col"
                                            class="py-3.5 pl-4 pr-3 text-left text-sm font-semibold text-gray-900 sm:pl-6">
                                            Basket #3
                                        </th>
                                    </tr>
                                    </thead>
                                    <tbody class="bg-white">

                                    <tr class="border-t border-gray-200">
                                        <th colspan="5" scope="colgroup"
                                            class="bg-gray-50 px-4 py-2 text-left text-sm font-semibold text-gray-900 sm:px-6">
                                            Edinburgh
                                        </th>
                                    </tr>

                                    <tr class="border-t border-gray-300">
                                        <td class="whitespace-nowrap py-4 pl-4 pr-3 text-sm font-medium text-gray-900 sm:pl-6">
                                            Lindsay Walton
                                        </td>
                                        <td class="whitespace-nowrap px-3 py-4 text-sm text-gray-500">Front-end
                                            Developer
                                        </td>
                                        <td class="whitespace-nowrap px-3 py-4 text-sm text-gray-500">
                                            lindsay.walton@example.com
                                        </td>
                                        <td class="whitespace-nowrap px-3 py-4 text-sm text-gray-500">Member</td>
                                        <td class="relative whitespace-nowrap py-4 pl-3 pr-4 text-right text-sm font-medium sm:pr-6">
                                            <a href="#" class="text-indigo-600 hover:text-indigo-900">Edit<span
                                                    class="sr-only">, Lindsay Walton</span></a>
                                        </td>
                                    </tr>

                                    <tr class="border-t border-gray-200">
                                        <td class="whitespace-nowrap py-4 pl-4 pr-3 text-sm font-medium text-gray-900 sm:pl-6">
                                            Courtney Henry
                                        </td>
                                        <td class="whitespace-nowrap px-3 py-4 text-sm text-gray-500">Designer</td>
                                        <td class="whitespace-nowrap px-3 py-4 text-sm text-gray-500">
                                            courtney.henry@example.com
                                        </td>
                                        <td class="whitespace-nowrap px-3 py-4 text-sm text-gray-500">Admin</td>
                                        <td class="relative whitespace-nowrap py-4 pl-3 pr-4 text-right text-sm font-medium sm:pr-6">
                                            <a href="#" class="text-indigo-600 hover:text-indigo-900">Edit<span
                                                    class="sr-only">, Courtney Henry</span></a>
                                        </td>
                                    </tr>

                                    <!-- More people... -->
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

        </div>
    </div>
</main>