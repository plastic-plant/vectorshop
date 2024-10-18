<script>
  import { onMount } from 'svelte';
  import Sidebar from '../components/Sidebar.svelte';
  import Header from '../components/Header.svelte';
  import { client } from '../clients/typesenseClient';

  export let nr;
  let product;

  onMount(async () => {
    product = await client.collections('products').documents(nr).retrieve();
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
    {#if product}
      <div class="product-details">
        <h1>{product.name}</h1>
        <div class="images">
          {#each product.images as image}
            <img src={`/products/${product.category}/${image}`} alt={product.name} />
          {/each}
        </div>
        <p>{product.description}</p>
        <p>Price: ${product.price}</p>
        <p>Availability: {product.availability}</p>
        <a href={`/category/${product.category}`}>Return to category</a>
      </div>
    {/if}
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
  .product-details {
    text-align: center;
  }
  .images {
    display: flex;
    justify-content: center;
    flex-wrap: wrap;
  }
  .images img {
    width: 200px;
    margin: 0.5rem;
  }
</style>