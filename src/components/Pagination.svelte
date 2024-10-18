<script>
  export let currentPage = 1;
  export let totalPages = 1;
  export let onPageChange;

  function handlePageChange(page) {
    if (page >= 1 && page <= totalPages) {
      onPageChange(page);
    }
  }
</script>

<div class="pagination">
  <button on:click={() => handlePageChange(currentPage - 1)} disabled={currentPage === 1}>
    Previous
  </button>
  {#each Array(totalPages).fill(0).map((_, i) => i + 1) as page}
    <button on:click={() => handlePageChange(page)} class:active={page === currentPage}>
      {page}
    </button>
  {/each}
  <button on:click={() => handlePageChange(currentPage + 1)} disabled={currentPage === totalPages}>
    Next
  </button>
</div>

<style>
  .pagination {
    display: flex;
    justify-content: center;
    margin: 1rem 0;
  }
  button {
    margin: 0 0.25rem;
    padding: 0.5rem 1rem;
  }
  .active {
    font-weight: bold;
    background-color: #333;
    color: #fff;
  }
</style>