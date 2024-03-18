<script>
	export let email;
	import { browser } from '$app/environment';

	let promise;
	async function getFilmes() {
	    // faz um request GET para endpoint /filmes
		let pesquisa;
		if (browser) {
			const pesquisaButton = document.querySelector('#pesquisa');
			pesquisa = pesquisaButton.value;
		}
		if (pesquisa == "" || pesquisa == null) {
			const res = await fetch(`http://localhost:8000/filmes/getMovieInfo`);
			const text = await res.json();
			if (res.ok) 
				return text;
			else 
				throw new Error(text);
		}
		else {
			const res = await fetch(`http://localhost:8000/filmes/getMovieByNameAndSortByPopular/${pesquisa}`);
			const text = await res.json();
			if (res.ok)
				return text;
			else
				throw new Error(text);
		}
	    
	}

	async function favoritarFilme(event) {
		const buttonValue = event.currentTarget.value;
		let res1 = await fetch(`http://localhost:8000/user/getUserByEmail?email=${email}`);
		if (res1.status == 200) {
			let usuario = await res1.json();
			const data = {
			"idMovie": parseInt(buttonValue),
			"idUser": parseInt(usuario.id)
			}
			const res2 = await fetch(`http://localhost:8000/favorite`, {
			method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
			body: JSON.stringify(data)
			})
			if (res2.status == 409) {
				alert("Esse filme já foi favoritado!");
			}
			else
				alert("Filme adicionado aos favoritos!");
		}
		else
			alert("Email inválido!");
	}

	function setEvent() {
		promise = getFilmes();
	}
</script>
<input type="text" id="pesquisa" placeholder="Deixe vazio para ver os mais populares" style="width: 20%;">
<button on:click={setEvent}> Get filmes </button>

{#await promise}
	<p>...waiting</p>
{:then filmes}
	{#if promise != null}
	<h1>Lista de filmes -</h1>
	<ul>
    {#each filmes as filme}
		<li>
			<img src={filme.imagem} alt="Imagem do poster do filme">
			<p>{filme.nome} | <button value="{filme.id}" on:click={favoritarFilme}>+ Favoritar</button></p>
		</li>
	{/each}
	</ul>
	{/if}
{:catch error}
	<p style="color: red">{error.message}</p>
{/await}

