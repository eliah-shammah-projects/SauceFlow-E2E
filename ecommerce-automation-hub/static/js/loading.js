const PHRASES = [
  "Abrindo o navegador...",
  "Fazendo login no site...",
  "Navegando até o catálogo...",
  "Coletando os produtos...",
  "Aplicando filtros de preço...",
  "Quase lá, organizando resultados...",
];

const POLL_INTERVAL_MS = 2000;
const PHRASE_INTERVAL_MS = 3000;
const TIMEOUT_MS = 60000;

const phraseEl = document.getElementById("phrase");
const params = new URLSearchParams(window.location.search);
const requestId = params.get("id");

// Se não há requestId na URL, volta para o início
if (!requestId) {
  window.location.href = "/";
} else {

// ── Rotação de frases ──
let phraseIndex = 0;
phraseEl.textContent = PHRASES[0];

const phraseTimer = setInterval(() => {
  phraseIndex = (phraseIndex + 1) % PHRASES.length;
  phraseEl.textContent = PHRASES[phraseIndex];
}, PHRASE_INTERVAL_MS);

// ── Polling do status ──
const startTime = Date.now();

const pollTimer = setInterval(async () => {
  // Timeout global de 60s
  if (Date.now() - startTime > TIMEOUT_MS) {
    clearInterval(pollTimer);
    clearInterval(phraseTimer);
    window.location.href =
      "/?erro=" + encodeURIComponent("A busca demorou demais. Tente novamente.");
    return;
  }

  try {
    const response = await fetch("/status/" + encodeURIComponent(requestId));

    // Se o job não foi encontrado (servidor reiniciado), volta ao início
    if (response.status === 404) {
      clearInterval(pollTimer);
      clearInterval(phraseTimer);
      window.location.href =
        "/?erro=" + encodeURIComponent("Sessão expirada. Por favor, faça uma nova busca.");
      return;
    }

    const data = await response.json();

    if (data.status === "done") {
      clearInterval(pollTimer);
      clearInterval(phraseTimer);
      window.location.href = "/resultados?id=" + encodeURIComponent(requestId);
    } else if (data.status === "error") {
      clearInterval(pollTimer);
      clearInterval(phraseTimer);
      const msg = data.error || "Erro durante a busca.";
      window.location.href = "/?erro=" + encodeURIComponent(msg);
    }
    // Se "running", não faz nada — próximo tick do intervalo irá verificar novamente
  } catch (err) {
    // Erro de rede — não interrompe, tenta no próximo tick
    console.error("Erro ao verificar status:", err);
  }
}, POLL_INTERVAL_MS);

} // fim do else
