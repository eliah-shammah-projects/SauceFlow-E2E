const PHRASES = [
  "Opening browser...",
  "Logging into the store...",
  "Navigating to the catalogue...",
  "Collecting products...",
  "Applying price filters...",
  "Almost there, sorting results...",
];

const POLL_INTERVAL_MS = 2000;
const PHRASE_INTERVAL_MS = 3000;
const TIMEOUT_MS = 60000;

const phraseEl = document.getElementById("phrase");
const params = new URLSearchParams(window.location.search);
const requestId = params.get("id");

if (!requestId) {
  window.location.href = "/";
} else {

// ── Phrase rotation ──
let phraseIndex = 0;
phraseEl.textContent = PHRASES[0];

const phraseTimer = setInterval(() => {
  phraseIndex = (phraseIndex + 1) % PHRASES.length;
  phraseEl.textContent = PHRASES[phraseIndex];
}, PHRASE_INTERVAL_MS);

// ── Status polling ──
const startTime = Date.now();

const pollTimer = setInterval(async () => {
  if (Date.now() - startTime > TIMEOUT_MS) {
    clearInterval(pollTimer);
    clearInterval(phraseTimer);
    window.location.href =
      "/?error=" + encodeURIComponent("Search timed out. Please try again.");
    return;
  }

  try {
    const response = await fetch("/status/" + encodeURIComponent(requestId));

    if (response.status === 404) {
      clearInterval(pollTimer);
      clearInterval(phraseTimer);
      window.location.href =
        "/?error=" + encodeURIComponent("Session expired. Please start a new search.");
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
      const msg = data.error || "An error occurred during the search.";
      window.location.href = "/?error=" + encodeURIComponent(msg);
    }
  } catch (err) {
    console.error("Error checking status:", err);
  }
}, POLL_INTERVAL_MS);

} // end else
