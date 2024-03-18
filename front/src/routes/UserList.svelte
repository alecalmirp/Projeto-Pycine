<script>
	export let email;
	let promise;
	async function getUsuarios() {
    // faz um request GET para endpoint /filmes
		const res = await fetch(`http://localhost:8000/user`);
		const text = await res.json();
		if (res.ok)
			return text;
    	else 
			throw new Error(text);
	}

	async function deleteUsuario(id) {
		if (confirm("Tem certeza que deseja deletar este usuário?")) {
			const res = await fetch(`http://localhost:8000/user?id=${id}`, {
				method: "DELETE"
			});
			if (res.ok) {
				let element = document.querySelector(`#user${id}`);
				element.style.display = "none";
				const text = await res.json();
				if (text.email == email) {
					alert("Você deletou seu usuário principal! Por favor, selecione ou crie um novo.")
					email = "";
				}
				else
					alert("Usuário deletado com sucesso!")
			}
			else if (res.status == 404)
				alert("Usuário não existe.");
				
		}
	}

	async function getStandardUser(id) {
		let res;
		if (id == null)
			res = await fetch(`http://localhost:8000/user/getUserById?id=1`);
		else
			res = await fetch(`http://localhost:8000/user/getUserById?id=${id}`);
		
		const text = await res.json();
		email = text.email;
		alert(`Agora o email ${email} é o principal!`)
	}

	promise = getUsuarios();
</script>

{#await promise}
	<p>...waiting</p>
{:then usuarios}
	{#if promise != null}
	<h1>Lista de usuarios - </h1>
		{#if email != "" && email != null}
			<h2>Usuário principal: {email}</h2>
		{/if}
    <table>
        <tr>
            <th>Id</th>
            <th>Email</th>
			<th>Ação</th>
        </tr>
    {#each usuarios as usuario}
        <tr id="user{usuario.id}">
            <td>{usuario.id}</td>
            <td>{usuario.email}</td>
			<td><button on:click={deleteUsuario(usuario.id)}>Deletar usuário</button></td>
			<td><button on:click={getStandardUser(usuario.id)}>Colocar como principal</button></td>
        </tr>
	{/each}
    </table>
	{/if}
{:catch error}
	<p style="color: red">{error.message}</p>
{/await}

