<script>
    import { onMount } from 'svelte';
    import Sidebar from '../components/Sidebar.svelte';
    import Header from '../components/Header.svelte';
    import Pagination from '../components/Pagination.svelte';
    import { products } from '../stores/store';
    import { client } from '../clients/typesenseClient';
    import { getContext } from 'svelte';
    const page = getContext('page');
  
    let query = new URLSearchParams(page.query).get('q') || '';
    let currentPage = 1;
    let totalPages = 1;
    let perPage = 10;
  
    async function fetchProducts() {
      const searchParameters = {
        q: query,
        query_by: 'text_embedding',
        collection: 'products',
        prefix: 'false',
        exclude_fields: 'text_embedding,image_embedding',
        page: currentPage,
        per_page: perPage
      };
      const results = await client.collections('products').documents().search(searchParameters);
      products.set(results.hits.map(hit => hit.document));
      totalPages = Math.ceil(results.found / perPage);
    }
  
    onMount(fetchProducts);
  
    function handleSearch(event) {
      const { query: newQuery } = event.detail;
      query = newQuery;
      currentPage = 1;
      fetchProducts();
    }
  
    function handlePageChange(page) {
      currentPage = page;
      fetchProducts();
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
      <Pagination {currentPage} {totalPages} onPageChange={handlePageChange} />
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
    }
  </style>