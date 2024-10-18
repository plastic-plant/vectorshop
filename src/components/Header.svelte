<script>
  import { createEventDispatcher } from 'svelte';

  const dispatch = createEventDispatcher();

  let query = '';

  function search() {
    dispatch('search', { query });
  }
</script>

<header>
  <input type="text" bind:value={query} on:keydown={(e) => e.key === 'Enter' && search()} placeholder="Search..." />
  <button on:click={search}>Search</button>
</header>

<style>
  header {
    display: flex;
    padding: 1rem;
  }

  input {
    flex: 1;
    padding: 0.5rem;
    margin-right: 0.5rem;
  }
  
  button {
    padding: 0.5rem 1rem;
  }
</style>