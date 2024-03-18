<script>
	export let email;
	import { browser } from '$app/environment';

	let promise;
	async function getArtistas() {
	    // faz um request GET para endpoint /filmes
		let pesquisa;
		if (browser) {
			const pesquisaButton = document.querySelector('#pesquisa');
			pesquisa = pesquisaButton.value;
		}
		if (pesquisa != "" && pesquisa != null) {
			const res = await fetch(`http://localhost:8000/atores/getAtorByName/${pesquisa}`);
			const text = await res.json();
			if (res.ok) 
				return text;
			else 
				throw new Error(text);
		}
		else {
			alert("Por favor, insira o nome de algum artista no campo de pesquisa!")
			setTimeout(function () {
				if (browser) {
					document.querySelector("#waiting").innerHTML = "";
				}
			}, 50)
			return null
		}
	    
	}

	async function favoritarArtistas(event) {
		const buttonValue = event.currentTarget.value;
		let res1 = await fetch(`http://localhost:8000/user/getUserByEmail?email=${email}`);
		if (res1.status == 200) {
			let usuario = await res1.json();
			const data = {
			"idPerson": parseInt(buttonValue),
			"idUser": parseInt(usuario.id)
			}
			const res2 = await fetch(`http://localhost:8000/atores/favorite`, {
			method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
			body: JSON.stringify(data)
			})
			
			if (res2.status != 200) {
				if (res2.status == 409)
					alert("Esse artista já foi favoritado!");
			}
			else
				alert("Artista adicionado aos favoritos!");
			
		}
		else
			alert("Email inválido!");
	}

	function setEvent() {
		promise = getArtistas();
	}
</script>
<input type="text" id="pesquisa" placeholder="Deixe vazio para ver os mais populares" style="width: 20%;">
<button on:click={setEvent}> Get artistas </button>

{#await promise}
	<p id="waiting">...waiting</p>
{:then artistas}
	{#if promise != null}
	<h1>Lista de artistas -</h1>
	<ul>
    {#each artistas as artista}
		<li>
			<img src={artista.imagem} alt="Imagem do perfil do artista">
			<p>{artista.nome} | <button value="{artista.id}" on:click={favoritarArtistas}>+ Favoritar</button></p>
			<p>Popularidade: {artista.popularidade}</p>
			<p>Data de nascimento: {artista.nascimento}</p>
		</li>
	{/each}
	</ul>
	{:else}
	<p></p>
	{/if}
{:catch error}
	<p style="color: red">{error.message}</p>
{/await}

