<script>
    export let menu;
  </script>
  
  <div id="componente-nav">
    <ul>
      <li><a href="/" on:click|preventDefault={() => (menu = 1)}>Filmes</a></li>
      <li><a href="/" on:click|preventDefault={() => (menu = 2)}>Favoritos</a></li>
      <li><a href="/" on:click|preventDefault={() => (menu = 3)}>Artista</a></li>
      <li><a href="/" on:click|preventDefault={() => (menu = 4)}>Lista Artistas</a></li>
      <li><a href="/" on:click|preventDefault={() => (menu = 5)}>Artistas Favoritos</a></li>
      <li><a href="/" on:click|preventDefault={() => (menu = 6)}>Users</a></li>
      <li><a href="/" on:click|preventDefault={() => (menu = 7)}>Users List</a></li>
    </ul>
  </div>
  
  <style>
  div{
    background-color: rgb(217, 217, 217);
  }
  ul { 
    color: navy; 
    padding: 10px;
  }
  li {
    display: inline-block;
    padding-right: 10px;
  }
  </style>