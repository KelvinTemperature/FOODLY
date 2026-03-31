const API_BASE = localStorage.getItem("foodly_api_base") || "http://127.0.0.1:5000";

const fallbackProducts = [
  {
    id: 1,
    name: "Machboos Chicken Bowl",
    description: "Kuwaiti spiced rice with grilled chicken",
    price: 2.75,
    quantity: 30,
    shop_id: 1,
    image: "Images/2-REFUEL-FRIED-RICE-MEAL.jpg",
  },
  {
    id: 2,
    name: "Saffron Shrimp Plate",
    description: "Saffron basmati with Gulf shrimp",
    price: 3.9,
    quantity: 18,
    shop_id: 1,
    image: "Images/7-REFUEL-MAX-FRIED-RICE-MEAL.jpg",
  },
  {
    id: 3,
    name: "Desert Heat BBQ Chicken",
    description: "Smoky grilled chicken with date glaze",
    price: 3.2,
    quantity: 24,
    shop_id: 1,
    image: "Images/BBQ Chicken.jpg",
  },
  {
    id: 4,
    name: "Harissa Pasta Fusion",
    description: "Creamy pasta with gentle chili heat",
    price: 2.45,
    quantity: 20,
    shop_id: 1,
    image: "Images/8-REFUEL-MAX-SPAGHETTI-MEAL.jpg",
  },
];

const governorates = {
  "Al Asimah": 1.0,
  Hawalli: 1.25,
  Farwaniya: 1.5,
  "Mubarak Al-Kabeer": 1.75,
  Ahmadi: 2.0,
  Jahra: 2.25,
};

let products = [];
const cart = new Map();
let rivalIndex = 0;

const rivalShops = ["Freej Feast", "Marina Meals", "Desert Fork", "Gulf Spoon", "City Bites KW"];

const rivalMealTemplates = [
  { meal: "Machboos Chicken Plate", emojiPng: "https://cdn.jsdelivr.net/gh/twitter/twemoji@14.0.2/assets/72x72/1f357.png" },
  { meal: "Shrimp Biryani Box", emojiPng: "https://cdn.jsdelivr.net/gh/twitter/twemoji@14.0.2/assets/72x72/1f364.png" },
  { meal: "Lamb Ouzi Bowl", emojiPng: "https://cdn.jsdelivr.net/gh/twitter/twemoji@14.0.2/assets/72x72/1f356.png" },
  { meal: "Mixed Grill Combo", emojiPng: "https://cdn.jsdelivr.net/gh/twitter/twemoji@14.0.2/assets/72x72/1f372.png" },
  { meal: "Falafel Wrap Meal", emojiPng: "https://cdn.jsdelivr.net/gh/twitter/twemoji@14.0.2/assets/72x72/1f959.png" },
  { meal: "Chicken Shawarma Deluxe", emojiPng: "https://cdn.jsdelivr.net/gh/twitter/twemoji@14.0.2/assets/72x72/1f32f.png" },
  { meal: "Seafood Rice Pot", emojiPng: "https://cdn.jsdelivr.net/gh/twitter/twemoji@14.0.2/assets/72x72/1f958.png" },
  { meal: "Zaatar Flatbread Set", emojiPng: "https://cdn.jsdelivr.net/gh/twitter/twemoji@14.0.2/assets/72x72/1f355.png" },
  { meal: "Kabsa Family Tray", emojiPng: "https://cdn.jsdelivr.net/gh/twitter/twemoji@14.0.2/assets/72x72/1f35b.png" },
  { meal: "Harissa Pasta Bowl", emojiPng: "https://cdn.jsdelivr.net/gh/twitter/twemoji@14.0.2/assets/72x72/1f35d.png" },
];

function buildRivalSamples() {
  const samples = [];
  for (let i = 0; i < 50; i += 1) {
    const template = rivalMealTemplates[i % rivalMealTemplates.length];
    const basePrice = 1.8 + (i % 10) * 0.28;
    const marketPrice = Number((basePrice + 0.7).toFixed(2));
    const foodlyPrice = Number((marketPrice - 0.35).toFixed(2));
    samples.push({
      id: i + 1,
      meal: template.meal,
      rival: rivalShops[i % rivalShops.length],
      marketPrice,
      foodlyPrice,
      image: template.emojiPng,
    });
  }
  return samples;
}

const rivalSamples = buildRivalSamples();

const menuGrid = document.getElementById("menuGrid");
const cartItems = document.getElementById("cartItems");
const cartCount = document.getElementById("cartCount");
const subtotalEl = document.getElementById("subtotal");
const deliveryEl = document.getElementById("delivery");
const totalEl = document.getElementById("total");
const feeHeroEl = document.getElementById("deliveryFee");
const governorateEl = document.getElementById("governorate");
const statusEl = document.getElementById("orderStatus");
const authStatusEl = document.getElementById("authStatus");
const authUserEl = document.getElementById("authUser");
const rivalTrackEl = document.getElementById("rivalTrack");
const rivalPrevEl = document.getElementById("rivalPrev");
const rivalNextEl = document.getElementById("rivalNext");

function setAuthStatus(message) {
  if (authStatusEl) {
    authStatusEl.textContent = message;
    return;
  }
  if (statusEl) {
    statusEl.textContent = message;
  }
}

function setOrderStatus(message) {
  if (statusEl) {
    statusEl.textContent = message;
  }
}

let authState = {
  token: localStorage.getItem("foodly_token") || null,
  user: JSON.parse(localStorage.getItem("foodly_user") || "null"),
};

function updateAuthBadge() {
  if (!authUserEl) return;
  authUserEl.textContent = authState.user ? authState.user.full_name : "Guest";
}

function persistAuth(nextState) {
  authState = nextState;
  if (authState.token) {
    localStorage.setItem("foodly_token", authState.token);
  } else {
    localStorage.removeItem("foodly_token");
  }
  if (authState.user) {
    localStorage.setItem("foodly_user", JSON.stringify(authState.user));
  } else {
    localStorage.removeItem("foodly_user");
  }
  updateAuthBadge();
}

async function authRequest(path, payload) {
  const response = await fetch(`${API_BASE}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  const body = await response.json().catch(() => ({}));
  if (!response.ok) {
    throw new Error(body.message || "Authentication request failed");
  }
  persistAuth({ token: body.access_token, user: body.user });
  setAuthStatus(`Welcome ${body.user.full_name}. Your account is active.`);
}

async function handleRegister(event) {
  event.preventDefault();
  const data = new FormData(event.target);
  try {
    await authRequest("/auth/register", {
      full_name: data.get("registerName"),
      email: data.get("registerEmail"),
      phone: data.get("registerPhone") || null,
      password: data.get("registerPassword"),
    });
    event.target.reset();
  } catch (error) {
    setAuthStatus(error.message);
  }
}

async function handleLogin(event) {
  event.preventDefault();
  const data = new FormData(event.target);
  try {
    await authRequest("/auth/login", {
      email: data.get("loginEmail"),
      password: data.get("loginPassword"),
    });
    event.target.reset();
  } catch (error) {
    setAuthStatus(error.message);
  }
}

function handleLogout() {
  persistAuth({ token: null, user: null });
  setAuthStatus("You are logged out.");
}

function kwd(value) {
  return `KWD ${Number(value).toFixed(2)}`;
}

function seedGovernorates() {
  if (!governorateEl) {
    return;
  }

  Object.keys(governorates).forEach((name) => {
    const option = document.createElement("option");
    option.value = name;
    option.textContent = name;
    governorateEl.append(option);
  });
}

function renderMenu() {
  if (!menuGrid) {
    return;
  }

  menuGrid.innerHTML = "";
  products.forEach((product) => {
    const card = document.createElement("article");
    card.className = "menuCard";
    card.innerHTML = `
      <img src="${product.image || "Images/ChickenRepublic_RefuelSpaghettiMeal.jpg"}" alt="${product.name}" loading="lazy" decoding="async" width="320" height="150" />
      <div class="menuBody">
        <h3>${product.name}</h3>
        <p class="small">${product.description || "Freshly prepared meal"}</p>
        <div class="priceLine">
          <span>${kwd(product.price)}</span>
          <span class="small">In stock: ${product.quantity}</span>
        </div>
        <button data-product-id="${product.id}" type="button">Add to cart</button>
      </div>
    `;
    menuGrid.append(card);
  });

  menuGrid.querySelectorAll("button").forEach((button) => {
    button.addEventListener("click", () => addToCart(Number(button.dataset.productId)));
  });
}

function renderRivalSamples() {
  if (!rivalTrackEl) {
    return;
  }

  rivalTrackEl.innerHTML = "";
  rivalSamples.forEach((sample) => {
    const card = document.createElement("article");
    card.className = "rivalCard";
    card.innerHTML = `
      <img src="${sample.image}" alt="${sample.meal}" loading="lazy" decoding="async" width="320" height="140" />
      <div class="rivalBody">
        <strong>${sample.meal}</strong>
        <span class="small">${sample.rival}</span>
        <div class="rivalPrice">
          <span>Market: ${kwd(sample.marketPrice)}</span>
          <span>Foodly: ${kwd(sample.foodlyPrice)}</span>
        </div>
      </div>
    `;
    rivalTrackEl.append(card);
  });
}

function moveRivalTrack(direction) {
  if (!rivalTrackEl) {
    return;
  }

  const cards = rivalTrackEl.querySelectorAll(".rivalCard");
  if (!cards.length) {
    return;
  }

  rivalIndex = (rivalIndex + direction + cards.length) % cards.length;
  cards[rivalIndex].scrollIntoView({ behavior: "smooth", inline: "start", block: "nearest" });
}

function addToCart(productId) {
  const product = products.find((item) => item.id === productId);
  if (!product) return;
  const current = cart.get(productId) || { product, qty: 0 };
  if (current.qty + 1 > product.quantity) {
    setOrderStatus("Cannot add more than available stock.");
    return;
  }
  current.qty += 1;
  cart.set(productId, current);
  renderCart();
}

function updateCartQty(productId, nextQty) {
  if (nextQty <= 0) {
    cart.delete(productId);
  } else {
    const entry = cart.get(productId);
    if (!entry) return;
    if (nextQty > entry.product.quantity) {
      setOrderStatus("Selected quantity exceeds available stock.");
      return;
    }
    entry.qty = nextQty;
  }
  renderCart();
}

function getSubtotal() {
  let subtotal = 0;
  cart.forEach((entry) => {
    subtotal += entry.product.price * entry.qty;
  });
  return subtotal;
}

function getDeliveryFee() {
  if (!governorateEl) {
    return 0;
  }

  return governorates[governorateEl.value] || 0;
}

function renderCart() {
  if (!cartItems || !cartCount || !subtotalEl || !deliveryEl || !totalEl || !feeHeroEl) {
    return;
  }

  cartItems.innerHTML = "";
  let count = 0;

  cart.forEach((entry, productId) => {
    count += entry.qty;
    const item = document.createElement("div");
    item.className = "cartItem";
    item.innerHTML = `
      <div>
        <strong>${entry.product.name}</strong>
        <div class="small">${kwd(entry.product.price)} each</div>
      </div>
      <div class="cartActions">
        <button type="button" data-action="minus">-</button>
        <span>${entry.qty}</span>
        <button type="button" data-action="plus">+</button>
      </div>
    `;

    const [minus, plus] = item.querySelectorAll("button");
    minus.addEventListener("click", () => updateCartQty(productId, entry.qty - 1));
    plus.addEventListener("click", () => updateCartQty(productId, entry.qty + 1));
    cartItems.append(item);
  });

  const subtotal = getSubtotal();
  const deliveryFee = cart.size ? getDeliveryFee() : 0;
  const total = subtotal + deliveryFee;

  cartCount.textContent = String(count);
  subtotalEl.textContent = kwd(subtotal);
  deliveryEl.textContent = kwd(deliveryFee);
  totalEl.textContent = kwd(total);
  feeHeroEl.textContent = kwd(deliveryFee);
}

async function loadCatalog() {
  try {
    const response = await fetch(`${API_BASE}/catalog`);
    if (!response.ok) throw new Error("Catalog request failed");
    const body = await response.json();
    products = body.products.map((product, index) => ({
      ...product,
      image: fallbackProducts[index % fallbackProducts.length].image,
    }));
    setOrderStatus("Connected to FOODLY backend.");
  } catch (error) {
    products = fallbackProducts;
    setOrderStatus("Running in demo mode. Start backend for live ordering.");
  }

  renderMenu();
}

async function placeOrder(event) {
  event.preventDefault();

  if (!cart.size) {
    setOrderStatus("Your cart is empty. Add at least one meal.");
    return;
  }

  const formData = new FormData(event.target);
  const payloadBase = {
    customer_name: formData.get("customerName"),
    customer_phone: formData.get("customerPhone"),
    customer_email: formData.get("customerEmail") || null,
    delivery_address: formData.get("deliveryAddress"),
    governorate: governorateEl.value,
    payment_method: formData.get("paymentMethod"),
    notes: formData.get("notes") || null,
  };

  const items = Array.from(cart.values());

  try {
    const createdOrders = [];
    for (const item of items) {
      const response = await fetch(`${API_BASE}/orders`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          ...(authState.token ? { Authorization: `Bearer ${authState.token}` } : {}),
        },
        body: JSON.stringify({
          ...payloadBase,
          product_id: item.product.id,
          quantity: item.qty,
        }),
      });

      if (!response.ok) {
        const errorBody = await response.json().catch(() => ({}));
        throw new Error(errorBody.message || "Could not place your order");
      }
      createdOrders.push(await response.json());
    }

    const orderRefs = createdOrders.map((order) => `#${order.id}`).join(", ");
    setOrderStatus(`Order placed successfully. Tracking IDs: ${orderRefs}.`);
    cart.clear();
    renderCart();
    event.target.reset();
  } catch (error) {
    setOrderStatus(`Checkout failed: ${error.message}`);
  }
}

const checkoutFormEl = document.getElementById("checkoutForm");
const openCartEl = document.getElementById("openCart");

if (checkoutFormEl) {
  checkoutFormEl.addEventListener("submit", placeOrder);
}

if (openCartEl) {
  openCartEl.addEventListener("click", () => {
    const cartPanel = document.getElementById("cartPanel");
    if (cartPanel) {
      cartPanel.scrollIntoView({ behavior: "smooth", block: "start" });
    }
  });
}

if (document.getElementById("registerForm")) {
  document.getElementById("registerForm").addEventListener("submit", handleRegister);
}
if (document.getElementById("loginForm")) {
  document.getElementById("loginForm").addEventListener("submit", handleLogin);
}
if (document.getElementById("logoutBtn")) {
  document.getElementById("logoutBtn").addEventListener("click", handleLogout);
}

if (governorateEl) {
  governorateEl.addEventListener("change", renderCart);
}

if (rivalPrevEl) {
  rivalPrevEl.addEventListener("click", () => moveRivalTrack(-1));
}

if (rivalNextEl) {
  rivalNextEl.addEventListener("click", () => moveRivalTrack(1));
}

seedGovernorates();
loadCatalog();
renderRivalSamples();
renderCart();
updateAuthBadge();

if ("serviceWorker" in navigator) {
  window.addEventListener("load", () => {
    navigator.serviceWorker.register("./service-worker.js").catch(() => {
      // Silent fallback keeps core app usable even if SW registration fails.
    });
  });
}
