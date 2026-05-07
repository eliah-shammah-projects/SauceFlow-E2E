const params = new URLSearchParams(window.location.search);
const requestId = params.get("id");
const contentEl = document.getElementById("content");
const errorBox = document.getElementById("error-box");
const inlineError = document.getElementById("inline-error");

if (!requestId) {
  window.location.href = "/";
} else {

function showError(msg) {
  errorBox.textContent = msg;
  errorBox.style.display = "block";
}

function showInlineError(msg) {
  inlineError.textContent = msg;
  inlineError.style.display = "block";
}

function renderTable(products) {
  if (!products || products.length === 0) {
    contentEl.innerHTML =
      "<p style='color:#555; margin-top:16px;'>No products found for this search.</p>" +
      "<p style='color:#555; margin-top:8px;'>Try a different term or increase the maximum price.</p>";
    return;
  }

  let rows = "";
  products.forEach((product, index) => {
    const isCheapest = index === 0;
    const badge = isCheapest
      ? "<span style='font-size:0.75rem; background:#f39c12; color:#fff; border-radius:3px; padding:2px 6px; margin-left:8px;'>cheapest</span>"
      : "";

    rows += `
      <tr class="${isCheapest ? "cheapest" : ""}">
        <td>${product.title}${badge}</td>
        <td>$${product.price.toFixed(2)}</td>
        <td>
          <button
            class="btn btn-buy"
            data-index="${index}"
          >Buy</button>
        </td>
      </tr>`;
  });

  contentEl.innerHTML = `
    <table>
      <thead>
        <tr>
          <th>Product</th>
          <th>Price</th>
          <th>Action</th>
        </tr>
      </thead>
      <tbody>
        ${rows}
      </tbody>
    </table>`;

  contentEl.querySelectorAll(".btn-buy").forEach((btn) => {
    btn.addEventListener("click", () => {
      const index = parseInt(btn.getAttribute("data-index"), 10);
      handleBuy(products[index]);
    });
  });
}

async function handleBuy(product) {
  contentEl.querySelectorAll(".btn-buy").forEach((b) => {
    b.disabled = true;
    b.textContent = "Please wait...";
  });
  inlineError.style.display = "none";

  try {
    const response = await fetch("/run-checkout", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ requestId, product }),
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || "Failed to process the purchase.");
    }

    sessionStorage.setItem("orderResult", JSON.stringify(data));
    window.location.href = "/checkout-status";
  } catch (err) {
    contentEl.querySelectorAll(".btn-buy").forEach((b) => {
      b.disabled = false;
      b.textContent = "Buy";
    });
    showInlineError(err.message);
  }
}

async function loadResults() {
  try {
    const response = await fetch("/status/" + encodeURIComponent(requestId));

    if (response.status === 404) {
      showError("Session expired. Please start a new search.");
      return;
    }

    const data = await response.json();

    if (data.status !== "done") {
      showError("Search not completed yet. Please go back and try again.");
      return;
    }

    renderTable(data.results);
  } catch (err) {
    showError("Failed to load results. Please try again.");
  }
}

loadResults();

} // end else
