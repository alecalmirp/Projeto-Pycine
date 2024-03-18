<script>
    export let email;
    let promise;
    async function getYuriFavorites() {
        const res = await fetch(`http://localhost:8000/atores/favorite?email=${email}`);
        if (res.status == 200) {
            const text = await res.json();
            return text;
        }
    }

    async function getYuriId() {
        const res = await fetch(`http://localhost:8000/user/getUserByEmail?email=${email}`);
        if (res.status == 200) {
            const text = await res.json();
            return text;
        }
        console.log("Teste");
        
    }

	async function getFavoritos() {
        debugger;
        const text = await getYuriFavorites();
        let peopleQueryString = `http://localhost:8000/atores/getMultiplePeopleById?`;
        text.forEach(function(element, idx, array) {
            if (idx == 0) {
                peopleQueryString += `ids=${element.idPerson}`;
            }
            else {
                peopleQueryString += `&ids=${element.idPerson}`;
            }
        });
        const res2 = await fetch(peopleQueryString);
        if (res2.status == 200) {
            const text2 = await res2.json();

            return text2;
        }
        else
            alert("Erro desconhecido.");
	}

    async function removerFavoritos(event) {
        const button = event.currentTarget.value;
        let text = await getYuriId();
        let data = {
            "idPerson": button,
            "idUser": text.id
        }

        await fetch(`http://localhost:8000/atores/favorite`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })

        document.querySelector(`#favorito${button}`).style.display = "none"
        alert("Ator desfavoritado.");
    }

    function setEvent() {
        promise = getFavoritos();
    }
</script>

<button on:click={setEvent}> Get artistas favoritos </button>

{#await promise}
	<p>...waiting</p>
{:then favoritos}
	{#if promise != null}
	<h1>Lista de favoritos -</h1>
	<ul>
    {#each favoritos as favorito}
		<li id="favorito{favorito.id}">
			<img src={favorito.imagem} alt="Imagem de perfil do ator">
			<p>{favorito.nome} | <button value="{favorito.id}" on:click={removerFavoritos}>- Desfavoritar</button></p>
            <p>Popularidade: {favorito.popularidade}</p>
            <p>Data de nascimento: {favorito.nascimento}</p>
		</li>
	{/each}
	</ul>
	{/if}
{:catch error}
	<p style="color: red">Email não existe, ou usuário não possui favoritos!</p>
{/await}