<script>
	let menu = 1;
	let email = "";
	import Movie from "./Movie.svelte";
	import Artista from "./Artist.svelte";
	import Nav from "./Nav.svelte";
	import User from "./User.svelte";
	import UserList from "./UserList.svelte";
	import Favoritos from "./Favoritos.svelte";
    import { onMount } from "svelte";
    import ArtistList from "./ArtistList.svelte";
    import FavoriteArtist from "./FavoriteArtist.svelte";
	onMount(getStandardUser);
	async function getStandardUser(id) {
		let res;
		if (id == null)
			res = await fetch(`http://localhost:8000/user/getUserById?id=1`);
		else
			res = await fetch(`http://localhost:8000/user/getUserById?id=${id}`);
		
		const text = await res.json();
		email = text.email;
		
	}
</script>

<Nav bind:menu/>

<div class="card">
	{#if menu === 1}
		<Movie bind:email/>
	{:else if menu === 2}
		<Favoritos bind:email/>
	{:else if menu === 3}
		<Artista/>
	{:else if menu === 4}
		<ArtistList bind:email/>
	{:else if menu === 5}
		<FavoriteArtist bind:email/>
	{:else if menu === 6}
		<User bind:email/>
	{:else if menu === 7}
		<UserList bind:email/>
	{:else}
		OPTION 5
	{/if}
</div>