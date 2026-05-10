const params = new URLSearchParams(window.location.search);
const requestId = params.get("id");
const contentEl = document.getElementById("content");
const errorBox = document.getElementById("error-box");
const inlineError = document.getElementById("inline-error");
const cartLink = document.getElementById("cart-link");
const cartCount = document.getElementById("cart-count");

if (!requestId) {
  window.location.href = "/";
} else {

const CART_KEY = "sauceflow_cart_" + requestId;

cartLink.href = "/cart?id=" + encodeURIComponent(requestId);

function getCart() {
  try { return JSON.parse(sessionStorage.getItem(CART_KEY)) || []; }
  catch { return []; }
}

function saveCart(items) {
  sessionStorage.setItem(CART_KEY, JSON.stringify(items));
  updateCartUI();
}

function updateCartUI() {
  const cart = getCart();
  if (cart.length > 0) {
    cartCount.textContent = cart.length;
    cartLink.style.display = "inline";
  } else {
    cartLink.style.display = "none";
  }
}

function showError(msg) {
  errorBox.textContent = msg;
  errorBox.style.display = "block";
}

function renderTable(products) {
  if (!products || products.length === 0) {
    contentEl.innerHTML =
      "<p style='color:var(--text-muted); margin-top:16px;'>No products found for this search.</p>" +
      "<p style='color:var(--text-muted); margin-top:8px;'>Try a different term or increase the maximum price.</p>";
    return;
  }

  const cart = getCart();

  let rows = "";
  products.forEach((product, index) => {
    const isCheapest = index === 0;
    const badge = isCheapest
      ? "<span class='badge-cheapest'>cheapest</span>"
      : "";
    const inCart = cart.some(p => p.id === product.id);

    rows += `
      <tr class="${isCheapest ? "cheapest" : ""}">
        <td>${product.title}${badge}</td>
        <td>$${product.price.toFixed(2)}</td>
        <td>
          <button
            class="btn btn-buy${inCart ? " btn-in-cart" : ""}"
            data-index="${index}"
            ${inCart ? "disabled" : ""}
          >${inCart ? "In cart" : "Add to cart"}</button>
        </td>
      </tr>`;
  });

  contentEl.innerHTML = `
    <table>
      <thead>
        <tr>
          <th>Product</th>
          <th>Price</th>
          <th></th>
        </tr>
      </thead>
      <tbody>${rows}</tbody>
    </table>`;

  contentEl.querySelectorAll(".btn-buy:not(:disabled)").forEach((btn) => {
    btn.addEventListener("click", () => {
      const index = parseInt(btn.getAttribute("data-index"), 10);
      addToCart(products[index], btn);
    });
  });
}

function addToCart(product, btn) {
  const cart = getCart();
  if (!cart.some(p => p.id === product.id)) {
    cart.push(product);
    saveCart(cart);
  }
  btn.textContent = "In cart";
  btn.disabled = true;
  btn.classList.add("btn-in-cart");
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
    updateCartUI();
  } catch (err) {
    showError("Failed to load results. Please try again.");
  }
}

loadResults();

} // end else
