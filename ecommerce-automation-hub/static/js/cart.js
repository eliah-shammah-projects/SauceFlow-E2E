const params = new URLSearchParams(window.location.search);
const requestId = params.get("id");
const contentEl = document.getElementById("content");
const errorBox = document.getElementById("error-box");
const inlineError = document.getElementById("inline-error");

// Se não há requestId na URL, volta para o início
if (!requestId) {
  window.location.href = "/";
} else {

// ── Exibe erro principal (acima da tabela) ──
function showError(msg) {
  errorBox.textContent = msg;
  errorBox.style.display = "block";
}

// ── Exibe erro inline (abaixo da tabela, após tentar comprar) ──
function showInlineError(msg) {
  inlineError.textContent = msg;
  inlineError.style.display = "block";
}

// ── Renderiza a tabela de produtos ──
function renderTable(produtos) {
  if (!produtos || produtos.length === 0) {
    contentEl.innerHTML =
      "<p style='color:#555; margin-top:16px;'>Nenhum produto encontrado para essa busca.</p>" +
      "<p style='color:#555; margin-top:8px;'>Tente um termo diferente ou aumente o preço máximo.</p>";
    return;
  }

  // Monta o HTML da tabela
  let rows = "";
  produtos.forEach((produto, index) => {
    const isCheapest = index === 0;
    const badge = isCheapest
      ? "<span style='font-size:0.75rem; background:#f39c12; color:#fff; border-radius:3px; padding:2px 6px; margin-left:8px;'>mais barato</span>"
      : "";

    rows += `
      <tr class="${isCheapest ? "cheapest" : ""}">
        <td>${produto.title}${badge}</td>
        <td>$${produto.price.toFixed(2)}</td>
        <td>
          <button
            class="btn btn-buy"
            data-index="${index}"
          >Comprar</button>
        </td>
      </tr>`;
  });

  contentEl.innerHTML = `
    <table>
      <thead>
        <tr>
          <th>Produto</th>
          <th>Preço</th>
          <th>Ação</th>
        </tr>
      </thead>
      <tbody>
        ${rows}
      </tbody>
    </table>`;

  // ── Adiciona listener em cada botão "Comprar" ──
  contentEl.querySelectorAll(".btn-buy").forEach((btn) => {
    btn.addEventListener("click", () => {
      const index = parseInt(btn.getAttribute("data-index"), 10);
      handleComprar(produtos[index]);
    });
  });
}

// ── Executa a compra do produto selecionado ──
async function handleComprar(produto) {
  // Desativa todos os botões para evitar duplo clique
  contentEl.querySelectorAll(".btn-buy").forEach((b) => {
    b.disabled = true;
    b.textContent = "Aguarde...";
  });
  inlineError.style.display = "none";

  try {
    const response = await fetch("/run-checkout", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ requestId, produto }),
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || "Erro ao processar a compra.");
    }

    // Salva o resultado no sessionStorage para a tela de checkout lê-lo
    sessionStorage.setItem("orderResult", JSON.stringify(data));
    window.location.href = "/checkout-status";
  } catch (err) {
    // Reativa os botões e mostra o erro inline
    contentEl.querySelectorAll(".btn-buy").forEach((b) => {
      b.disabled = false;
      b.textContent = "Comprar";
    });
    showInlineError(err.message);
  }
}

// ── Busca os resultados da busca já concluída ──
async function carregarResultados() {
  try {
    const response = await fetch("/status/" + encodeURIComponent(requestId));

    if (response.status === 404) {
      showError("Sessão expirada. Por favor, faça uma nova busca.");
      return;
    }

    const data = await response.json();

    if (data.status !== "done") {
      showError("A busca ainda não foi concluída. Volte e tente novamente.");
      return;
    }

    renderTable(data.resultados);
  } catch (err) {
    showError("Erro ao carregar os resultados. Tente novamente.");
  }
}

// Inicia ao carregar a página
carregarResultados();

} // fim do else
