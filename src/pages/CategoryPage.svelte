<script>
  import { onMount } from 'svelte';
  import Sidebar from '../components/Sidebar.svelte';
  import Header from '../components/Header.svelte';
  import { products } from '../stores/store';
  import { client } from '../clients/typesenseClient';

  export let category;

  onMount(async () => {
    console.log(category);
    const searchParameters = {
      q: '*',
      query_by: 'category',
      filter_by: `category:=${category}`
    };
    const results = await client.collections('products').documents().search(searchParameters);
    console.log(results);
    products.set(results.hits.map(hit => hit.document));
  });

  function handleSearch(event) {
    const { query } = event.detail;
    window.location.href = `/search?q=${query}`;
  }
</script>

<main>
  <Sidebar />
  <div class="content">
    <Header on:search={handleSearch} />
    <div class="products">
      {#each $products as product}
        <div class="product">
          <a href={`/product/${product.nr}`}>
            <img src={`/products/${product.category}/${product.images[0]}`} alt={product.name} />
            <p>{product.name}</p>
          </a>
        </div>
      {/each}
    </div>
  </div>
</main>

<style>
  main {
    display: flex;
  }

  .content {
    flex: 1;
    padding: 1rem;
  }

  .products {
    display: flex;
    flex-wrap: wrap;
  }

  .product {
    width: 200px;
    margin: 1rem;
    text-align: center;
  }

  .product img {
    width: 100%;
    height: auto;
    overflow: hidden;
    border-radius: 15px;
    border: 1px solid #ddd;
  }
</style>