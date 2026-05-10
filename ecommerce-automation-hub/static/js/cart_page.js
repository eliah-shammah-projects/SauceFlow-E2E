const params = new URLSearchParams(window.location.search);
const requestId = params.get("id");
const cartContent = document.getElementById("cart-content");
const backLink = document.getElementById("back-link");

if (!requestId) {
  window.location.href = "/";
} else {

const CART_KEY = "sauceflow_cart_" + requestId;

backLink.href = "/resultados?id=" + encodeURIComponent(requestId);

function getCart() {
  try { return JSON.parse(sessionStorage.getItem(CART_KEY)) || []; }
  catch { return []; }
}

function saveCart(items) {
  sessionStorage.setItem(CART_KEY, JSON.stringify(items));
  render();
}

function removeFromCart(productId) {
  saveCart(getCart().filter(p => p.id !== productId));
}

function render() {
  const cart = getCart();

  if (cart.length === 0) {
    cartContent.innerHTML = `
      <p style="color:var(--text-muted); margin-top:16px;">Your cart is empty.</p>
      <a href="/resultados?id=${encodeURIComponent(requestId)}" class="link-back" style="display:inline-block; margin-top:20px;">← Back to results</a>`;
    return;
  }

  let rows = "";
  cart.forEach(product => {
    rows += `
      <tr>
        <td>${product.title}</td>
        <td>$${parseFloat(product.price).toFixed(2)}</td>
        <td><button class="btn btn-remove" data-id="${product.id}">Remove</button></td>
      </tr>`;
  });

  cartContent.innerHTML = `
    <table>
      <thead>
        <tr><th>Product</th><th>Price</th><th></th></tr>
      </thead>
      <tbody>${rows}</tbody>
    </table>

    <div class="shipping-form">
      <h2>Shipping details</h2>
      <div id="form-error" class="error-msg" style="display:none;"></div>
      <div class="form-group">
        <label for="first-name">First name</label>
        <input type="text" id="first-name" placeholder="John" autocomplete="given-name" />
      </div>
      <div class="form-group">
        <label for="last-name">Last name</label>
        <input type="text" id="last-name" placeholder="Doe" autocomplete="family-name" />
      </div>
      <div class="form-group">
        <label for="postal-code">Postal code</label>
        <input type="text" id="postal-code" placeholder="12345" autocomplete="postal-code" />
      </div>
      <button class="btn" id="checkout-btn">Checkout</button>
    </div>`;

  cartContent.querySelectorAll(".btn-remove").forEach(btn => {
    btn.addEventListener("click", () => removeFromCart(btn.getAttribute("data-id")));
  });

  document.getElementById("checkout-btn").addEventListener("click", handleCheckout);
}

async function handleCheckout() {
  const firstName = document.getElementById("first-name").value.trim();
  const lastName  = document.getElementById("last-name").value.trim();
  const postalCode = document.getElementById("postal-code").value.trim();
  const formError = document.getElementById("form-error");

  if (!firstName || !lastName || !postalCode) {
    formError.textContent = "Please fill in all shipping details.";
    formError.style.display = "block";
    return;
  }

  formError.style.display = "none";

  const cart = getCart();
  const product = cart.reduce((a, b) => a.price <= b.price ? a : b);

  const btn = document.getElementById("checkout-btn");
  btn.disabled = true;
  btn.textContent = "Processing...";

  try {
    const response = await fetch("/run-checkout", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ requestId, product, firstName, lastName, postalCode }),
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || "Failed to process the purchase.");
    }

    sessionStorage.setItem("orderResult", JSON.stringify({ ...data, firstName, lastName, postalCode }));
    window.location.href = "/checkout-status";
  } catch (err) {
    btn.disabled = false;
    btn.textContent = "Checkout";
    formError.textContent = err.message;
    formError.style.display = "block";
  }
}

render();

} // end else
