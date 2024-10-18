<script>
  import Sidebar from '../components/Sidebar.svelte';
  import Header from '../components/Header.svelte';
  import { categories } from '../stores/store';

  function handleSearch(event) {
    const { query } = event.detail;
    window.location.href = `/search?q=${query}`;
  }
</script>

<main>
  <Sidebar />
  <div class="content">
    <Header on:search={handleSearch} />
    <div class="categories">
      {#each $categories as category}
        <div class="category">
          <a href={`/category/${category}`}>
            <img src={`/products/${category}/category.png`} alt={category} />
            <p>{category}</p>
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

  .categories {
    display: flex;
    flex-wrap: wrap;
  }

  .category {
    width: 200px;
    margin: 1rem;
    text-align: center;
  }

  .category img {
    width: 100%;
    height: auto;
    overflow: hidden;
    border-radius: 15px;
    border: 1px solid #ddd;
    opacity: 0.8;
  }
  
  .category:hover img {
    opacity: 1.0;
  }
</style>