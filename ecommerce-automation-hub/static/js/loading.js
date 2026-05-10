const POLL_INTERVAL_MS = 2000;
const TIMEOUT_MS = 60000;

const stepsEl = document.getElementById("steps");
const params = new URLSearchParams(window.location.search);
const requestId = params.get("id");

if (!requestId) {
  window.location.href = "/";
} else {

let renderedCount = 0;

function renderSteps(steps) {
  if (!steps || steps.length === 0) return;
  for (let i = renderedCount; i < steps.length; i++) {
    const li = document.createElement("li");
    li.className = "trace-step trace-step--new";
    li.textContent = "✓ " + steps[i];
    stepsEl.appendChild(li);
    setTimeout(() => li.classList.remove("trace-step--new"), 50);
  }
  renderedCount = steps.length;
}

const startTime = Date.now();

const pollTimer = setInterval(async () => {
  if (Date.now() - startTime > TIMEOUT_MS) {
    clearInterval(pollTimer);
    window.location.href =
      "/?error=" + encodeURIComponent("Search timed out. Please try again.");
    return;
  }

  try {
    const response = await fetch("/status/" + encodeURIComponent(requestId));

    if (response.status === 404) {
      clearInterval(pollTimer);
      window.location.href =
        "/?error=" + encodeURIComponent("Session expired. Please start a new search.");
      return;
    }

    const data = await response.json();

    renderSteps(data.steps);

    if (data.status === "done") {
      clearInterval(pollTimer);
      setTimeout(() => {
        window.location.href = "/resultados?id=" + encodeURIComponent(requestId);
      }, 1500);
    } else if (data.status === "error") {
      clearInterval(pollTimer);
      const msg = data.error || "An error occurred during the search.";
      window.location.href = "/?error=" + encodeURIComponent(msg);
    }
  } catch (err) {
    console.error("Error checking status:", err);
  }
}, POLL_INTERVAL_MS);

} // end else
