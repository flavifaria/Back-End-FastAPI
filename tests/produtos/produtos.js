// Ajuste para '/produtos' ou '/products' dependendo de como está o seu routers.py
const API_URL = 'http://localhost:8000/produtos'; 

// 1. CRIAR (POST)
document.getElementById('formCriarProduto').addEventListener('submit', async (e) => {
    e.preventDefault();
    try {
        const resposta = await fetch(`${API_URL}/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                nome: document.getElementById('prodNome').value,
                preco: parseFloat(document.getElementById('prodPreco').value)
                // Se seu schema exige estoque ou descrição, adicione aqui!
            })
        });
        const dados = await resposta.json();
        document.getElementById('msgCriarProduto').innerText = resposta.ok ? `Criado! ID: ${dados.id}` : JSON.stringify(dados);
    } catch (erro) { console.error(erro); }
});

// 2. LISTAR (GET)
document.getElementById('btnListar').addEventListener('click', async () => {
    try {
        const resposta = await fetch(`${API_URL}/`); // Pode precisar de Token se a rota for protegida
        const produtos = await resposta.json();
        
        const listaHtml = document.getElementById('listaProdutos');
        listaHtml.innerHTML = ''; // Limpa a lista antes de preencher

        produtos.forEach(prod => {
            const li = document.createElement('li');
            li.innerText = `ID: ${prod.id} | Nome: ${prod.nome} | Preço: R$ ${prod.preco}`;
            listaHtml.appendChild(li);
        });
    } catch (erro) { console.error(erro); }
});

// 3. ATUALIZAR (PUT)
document.getElementById('formAtualizarProduto').addEventListener('submit', async (e) => {
    e.preventDefault();
    const id = document.getElementById('upId').value;
    try {
        const resposta = await fetch(`${API_URL}/${id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                nome: document.getElementById('upNome').value,
                preco: parseFloat(document.getElementById('upPreco').value)
            })
        });
        const dados = await resposta.json();
        document.getElementById('msgAtualizar').innerText = resposta.ok ? "Produto Atualizado!" : JSON.stringify(dados);
    } catch (erro) { console.error(erro); }
});

// 4. DELETAR (DELETE)
document.getElementById('formDeletarProduto').addEventListener('submit', async (e) => {
    e.preventDefault();
    const id = document.getElementById('delId').value;
    try {
        const resposta = await fetch(`${API_URL}/${id}`, {
            method: 'DELETE'
        });
        
        if (resposta.ok) {
            document.getElementById('msgDeletar').innerText = "Produto apagado com sucesso!";
        } else {
            const dados = await resposta.json();
            document.getElementById('msgDeletar').innerText = JSON.stringify(dados);
        }
    } catch (erro) { console.error(erro); }
});