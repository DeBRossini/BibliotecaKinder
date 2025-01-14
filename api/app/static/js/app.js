
function toggleMenu() {
    const menu = document.getElementById('menu');
    menu.classList.toggle('open');
}

document.addEventListener("DOMContentLoaded", function () {
    const alterarOp = document.getElementById("alterar-op");

    const campoStatus = document.getElementById("campo-status");
    const campoNome = document.getElementById("campo-nome");
    const campoSenha = document.getElementById("campo-senha");
    const campoCargo = document.getElementById("campo-cargo");

    function atualizarCampos() {
        const valor = alterarOp.value;

        campoStatus.style.display = "none";
        campoNome.style.display = "none";
        campoSenha.style.display = "none";
        campoCargo.style.display = "none";

        if (valor === "status") {
            campoStatus.style.display = "block";
        } else if (valor === "nome_completo") {
            campoNome.style.display = "block";
        } else if (valor === "senha") {
            campoSenha.style.display = "block";
        } else if (valor === "cargo") {
            campoCargo.style.display = "block";
        }
    }

    atualizarCampos();

    alterarOp.addEventListener("change", atualizarCampos);
});

document.addEventListener("DOMContentLoaded", function () {
    const alterarOptLivro = document.getElementById("alterar-op-livro");

    const campoNomeLivro = document.getElementById("campo-nome");
    const campoAutor = document.getElementById("campo-autor");
    const campoDesc = document.getElementById("campo-descricao");
    const campoPalch = document.getElementById("campo-palch");

    function atualizarCampos() {
        const valor = alterarOptLivro.value;

        campoNomeLivro.style.display = "none";
        campoAutor.style.display = "none";
        campoDesc.style.display = "none";
        campoPalch.style.display = "none";

        if (valor === "nome-livro") {
            campoNomeLivro.style.display = "block";
        } else if (valor === "autor") {
            campoAutor.style.display = "block";
        } else if (valor === "descricao") {
            campoDesc.style.display = "block";
        } else if (valor === "palavras-chave") {
            campoPalch.style.display = "block";
        }
    }

    atualizarCampos();

    alterarOptLivro.addEventListener("change", atualizarCampos);
});
