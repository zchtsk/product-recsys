<script>
    import {onMount} from "svelte";
    import {basket, getNextBasket} from "../components/basket";
    import {fly} from 'svelte/transition';

    let startup = true;
    onMount(async () => {
        await getNextBasket()
        startup = false;
    })

</script>

<main class="h-screen">
    <!-- Navigation -->
    <div class="border py-3 pl-12 bg-gray-100">
        <p class="font-bold text-2xl text-gray-700">Product Recommender</p>
    </div>
    <!--Main Content-->
    <div class="max-w-6xl mx-auto">
        <div class="py-6 flex justify-center items-center gap-3">
            <p class="text-4xl tracking-tight text-center text-gray-800">See recommended add-ons and substitutes</p>
        </div>
        <!-- Generator -->
        <div class="flex justify-center">
            <button on:click={async ()=>{await getNextBasket()}}
                    class="border border-gray-300 px-5 py-4 rounded-lg shadow-md flex items-center gap-2 active:translate-y-[1px] hover:shadow-lg">
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
        <!-- Recommendations -->
        {#if !startup}
            <div class="flex justify-center pb-24">
                <div class="relative px-4 sm:px-6 lg:px-8">
                    <div class="mt-8 flex flex-col">
                        <div class="-my-2 -mx-4 sm:-mx-6 lg:-mx-8">
                            <div class="inline-block min-w-full py-2 align-middle md:px-6 lg:px-8">
                                <div class="shadow ring-1 ring-black ring-opacity-5">
                                    <table class="min-w-full">
                                        <thead class="bg-white">
                                        <tr>
                                            <th scope="col"
                                                class="py-3.5 pl-4 pr-3 text-left text-sm font-semibold text-gray-900">
                                                <div>
                                                    Basket #{$basket.basket_id}
                                                    {#if "also_like" in $basket && Object.entries($basket["also_like"]).length > 0}
                                                        {#if !$basket["show_also_like"]}
                                                            <button on:click={()=>{$basket["show_also_like"] = !$basket["show_also_like"]}}
                                                                    class="bg-teal-100 px-2 py-1 rounded border border-teal-500 ml-1.5 hover:bg-teal-200">
                                                                Recommendations available
                                                            </button>
                                                        {:else}
                                                            <button on:click={()=>{$basket["show_also_like"] = !$basket["show_also_like"]}}
                                                                    class="bg-rose-100 px-2 py-1 rounded border border-rose-500 ml-1.5 hover:bg-rose-200">
                                                                Hide recommendations
                                                            </button>
                                                        {/if}
                                                    {:else}
                                                        <p class="text-gray-400">No recommended add-ons for this
                                                            basket</p>
                                                    {/if}
                                                </div>
                                            </th>
                                        </tr>
                                        </thead>
                                        <tbody class="bg-white">
                                        {#if "data" in $basket}
                                            {#each Object.entries($basket["data"]) as [dept, products]}
                                                <tr class="border-t border-gray-200">
                                                    <th colspan="5" scope="colgroup"
                                                        class="bg-gray-100 px-4 py-2 text-left text-sm font-semibold text-gray-900">
                                                        {dept}
                                                    </th>
                                                </tr>
                                                {#each products as prod}
                                                    <tr class="border-t border-gray-300">
                                                        <td class="whitespace-nowrap py-2 pl-4 pr-3 text-sm text-gray-900">
                                                            {prod.product_name.toLowerCase()}
                                                        </td>
                                                        <td class="whitespace-nowrap px-3 py-2 text-sm text-gray-500 italic">
                                                            {prod.aisle_name}
                                                        </td>
                                                        {#if prod.subs.length > 0}
                                                            <td class="relative whitespace-nowrap py-2 pl-3 pr-4 text-right text-sm font-medium sm:pr-6">
                                                                <button on:click={()=>{prod.show_subs = !prod.show_subs}}
                                                                        class="border border-gray-300 px-2 py-1.5 rounded hover:text-teal-500">
                                                                    {#if prod.show_subs}
                                                                        <p class="text-sm text-red-500">Hide
                                                                            Substitutes</p>
                                                                    {:else}
                                                                        <p class="text-sm">Show Substitutes</p>
                                                                    {/if}
                                                                </button>
                                                                {#if prod.show_subs}
                                                                    <div transition:fly
                                                                         class="absolute -right-3 -top-1">
                                                                        <div class="absolute border rounded justify-start text-start pb-1 bg-white shadow-sm">
                                                                            <!-- Header -->
                                                                            <div class="flex justify-left items-end gap-1.5 px-3">
                                                                                <p class="text-gray-800 text-lg text-teal-500 self-end">
                                                                                    Substitutes for</p>
                                                                                <span class="text-gray-800 font-medium pb-0.5">{prod.product_name.toLowerCase()}</span>
                                                                            </div>
                                                                            <!-- Items -->
                                                                            <ul class="list-none">
                                                                                {#each prod.subs as sub}
                                                                                    <li class="px-3 py-1 font-light text-md">
                                                                                        - {sub.product_name.toLowerCase()} </li>
                                                                                {/each}
                                                                            </ul>
                                                                        </div>
                                                                    </div>
                                                                {/if}
                                                            </td>
                                                        {/if}
                                                    </tr>
                                                {/each}
                                            {/each}
                                        {/if}
                                        </tbody>
                                    </table>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                {#if "also_like" in $basket && Object.entries($basket["also_like"]).length > 0 && $basket["show_also_like"]}
                    <div transition:fly class="left-10 px-4 sm:px-6 lg:px-8">
                        <div class="mt-8 flex flex-col">
                            <div class="-my-2 -mx-4 sm:-mx-6 lg:-mx-8">
                                <div class="inline-block min-w-full py-2 align-middle md:px-6 lg:px-8">
                                    <div class="shadow ring-1 ring-black ring-opacity-5">
                                        <table class="min-w-full">
                                            <thead class="bg-white">
                                            <tr>
                                                <th scope="col"
                                                    class="py-3.5 pl-4 pr-3 text-left text-sm font-semibold text-teal-500">
                                                    <p class="py-1 min-w-20">Recommended with this basket</p>
                                                </th>
                                            </tr>
                                            </thead>
                                            <tbody class="bg-white">
                                            {#if "also_like" in $basket}
                                                {#each Object.entries($basket["also_like"]) as [compl_dept, compl_product]}
                                                    <tr class="border-t border-gray-200">
                                                        <th colspan="5" scope="colgroup"
                                                            class="bg-gray-100 px-4 py-2 text-left text-sm font-semibold text-gray-900">
                                                            {compl_dept}
                                                        </th>
                                                    </tr>
                                                    {#each compl_product as prod}
                                                        <tr class="border-t border-gray-300">
                                                            <td class="whitespace-nowrap py-2 pl-4 pr-3 text-sm text-gray-900">
                                                                {prod.product_name.toLowerCase()}
                                                            </td>
                                                            <td class="whitespace-nowrap px-3 py-2 text-sm text-gray-500 italic">
                                                                {prod.aisle_name}
                                                            </td>
                                                        </tr>
                                                    {/each}
                                                {/each}
                                            {/if}
                                            </tbody>
                                        </table>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                {/if}
            </div>
        {:else}
            <div role="status" class="flex items-center justify-center">
                <div class="py-6 justify-center flex items-center px-3">
                    <svg aria-hidden="true" class="mr-2 w-8 h-8 text-gray-200 animate-spin dark:text-gray-600 fill-blue-600"
                         viewBox="0 0 100 101" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z"
                              fill="currentColor"/>
                        <path d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z"
                              fill="currentFill"/>
                    </svg>
                    <p class="text-gray-800 text-lg font-semibold">Loading...</p>
                </div>
            </div>

        {/if}
</main>