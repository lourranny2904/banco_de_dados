import { useState, useEffect } from "react";

export default function Login() {
  const [nome, setNome] = useState("");
  const [senha, setSenha] = useState("");

  const handleName = (e) => setNome(e.target.value);
  const handleSenha = (e) => setSenha(e.target.value);

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log(nome, senha);

    setNome("");
    setSenha("");
  };

  useEffect(() => {
    if (senha == "lolo"){
        document.body.style.backgroundColor = "red";
        document.body.style.transition = "background-color 0.3s";
    }
  }, [senha]);

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <div>
          <label htmlFor="name">Nome</label>
          <input type="text" id="nome" name="nome" onChange={handleName} value={nome} placeholder="Nome"/>
        </div>

        <div>
          <label>
            Senha:
            <input type="text" placeholder="Digite sua senha" value={senha} onChange={handleSenha}/>
          </label>
        </div>

      </form>
    </div>
  );
} 