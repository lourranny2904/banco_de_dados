import { useState, useEffect } from 'react';

export default function Listas() {
  const [idDoFiltro, setIdDoFiltro] = useState('');
  const [postsFiltrados, setPostsFiltrados] = useState([]);
  const [estaCarregando, setEstaCarregando] = useState(false);
  const [erro, setErro] = useState(null);
  const [atualizar, setAtualizar] = useState(0);

  useEffect(() => {
    const buscarPosts = async () => {
      setEstaCarregando(true);
      setErro(null);

      try {
        const resposta = await fetch('https://jsonplaceholder.typicode.com/albums');
        if (!resposta.ok) throw new Error(`Erro: ${resposta.status}`); //  verificar se a requisição fetch deu certo

        //  pega os dados da resposta da API e filtra
        const dados = await resposta.json();
        const filtrados = idDoFiltro === ''
          ? dados
          : dados.filter(post => post.userId === Number(idDoFiltro));

        setPostsFiltrados(filtrados);
      } catch (erro) {
        setErro.console.erro('erro ao buscar id:', erro.message);
      } finally {
        setEstaCarregando(false);
      }
    };

    buscarPosts();
  }, [idDoFiltro, atualizar]);

  return (
    <div>
      <h1>Álbuns</h1>

      <input
        type="number"
        placeholder="ID do usuário (até 10)"
        value={idDoFiltro}
        onChange={(e) => setIdDoFiltro(e.target.value)}
      />

      <button onClick={() => setAtualizar(a => a + 1)}>
        Atualizar Lista
      </button>


      {!estaCarregando && !erro && (
        //renderiza  se não estiver carregando e nem tiver erro
        postsFiltrados.length === 0 && idDoFiltro !== '' ? (
            //caso o numero digitado não for encontrado 
          <p>não encontrado"{idDoFiltro}".</p>
        ) : (
          postsFiltrados.map(post => (
            <div key={post.id}>
              <h3>{post.title}</h3>
              <p>Usuário: {post.userId}</p>
            </div>
          ))
        )
      )}
    </div>
  );
}