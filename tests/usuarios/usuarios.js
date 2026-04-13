const API_URL = 'http://localhost:8000';

// 1. CADASTRAR USUÁRIO
document.getElementById('formCadastro').addEventListener('submit', async (e) => {
    e.preventDefault();
    try {
        const resposta = await fetch(`${API_URL}/users/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                name: document.getElementById('cadNome').value,
                email: document.getElementById('cadEmail').value,
                password: document.getElementById('cadSenha').value
            })
        });
        const dados = await resposta.json();
        document.getElementById('msgCadastro').innerText = resposta.ok ? "Usuário cadastrado!" : JSON.stringify(dados);
    } catch (erro) {
        console.error(erro);
    }
});

// 2. FAZER LOGIN E SALVAR TOKEN
// Atenção: O FastAPI (OAuth2) exige que o login seja enviado como Form Data (URLSearchParams), não como JSON!
document.getElementById('formLogin').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = new URLSearchParams();
    formData.append('username', document.getElementById('loginEmail').value); // FastAPI espera o campo "username"
    formData.append('password', document.getElementById('loginSenha').value);

    try {
        const resposta = await fetch(`${API_URL}/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: formData
        });
        
        const dados = await resposta.json();
        
        if (resposta.ok) {
            // Salva o token no navegador do aluno
            localStorage.setItem('token', dados.access_token);
            document.getElementById('msgLogin').innerText = "Login feito com sucesso! Token guardado.";
        } else {
            document.getElementById('msgLogin').innerText = "Erro: " + JSON.stringify(dados);
        }
    } catch (erro) {
        console.error(erro);
    }
});

// 3. BUSCAR PERFIL PROTEGIDO
document.getElementById('btnMeuPerfil').addEventListener('click', async () => {
    const token = localStorage.getItem('token');
    
    if (!token) {
        document.getElementById('msgPerfil').innerText = "Você não tem um token. Faça login primeiro!";
        return;
    }

    try {
        const resposta = await fetch(`${API_URL}/users/me`, {
            method: 'GET',
            headers: { 
                'Authorization': `Bearer ${token}` // Envia o token na requisição
            }
        });
        
        const dados = await resposta.json();
        document.getElementById('msgPerfil').innerText = JSON.stringify(dados, null, 2);
    } catch (erro) {
        console.error(erro);
    }
});