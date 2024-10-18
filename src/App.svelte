<script>
	import { Router, Route } from 'svelte-routing';
	import WelcomePage from './pages/WelcomePage.svelte';
	import CategoryPage from './pages/CategoryPage.svelte';
	import ProductPage from './pages/ProductPage.svelte';
	import SearchPage from './pages/SearchPage.svelte';
  </script>
  
  <Router>
	<Route path="/" component={WelcomePage} />
	<Route path="/category/:category" component={CategoryPage} />
	<Route path="/product/:nr" component={ProductPage} />
	<Route path="/search" component={SearchPage} />
  </Router>
