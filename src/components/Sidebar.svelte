<script>
  import { onMount } from 'svelte';
  import { categories } from '../stores/store';

  onMount(async () => {
    const response = await fetch('/products/categories.json');
    const data = await response.json();
    categories.set(data.categories);
  });
</script>

<aside>
  <ul>
    {#each $categories as category}
      <li><a href={`/category/${category}`}>{category}</a></li>
    {/each}
  </ul>
</aside>

<style>
  aside {
    width: 200px;
    padding: 1rem;
    background: #f4f4f4;
  }
  ul {
    list-style: none;
    padding: 0;
  }
  li {
    margin: 0.5rem 0;
  }
  a {
    text-decoration: none;
    color: #333;
  }
</style>