async function postData(url, data = {}) {
	const response = await fetch(url, {
		method: 'POST', headers: { 'Content-Type': 'application/json' },
		body: JSON.stringify(data)
	});

	return response.json();
}

class Drawers {
	static overlay = null;

	static init() {
		Drawers.overlay = document.getElementById("drawer-overlay");
		Drawers.overlay.addEventListener("click", Drawers.close);
	}

	static close() {
		const openedDrawers = document.querySelectorAll(".drawer.open");
		openedDrawers.forEach(drawer => drawer.classList.remove("open"));

		Drawers.overlay.classList.remove("show");
		document.body.style.overflow = "";
	}

	static open(drawer) {
		Drawers.close();

		drawer.classList.add("open");
		Drawers.overlay.classList.add("show");
		document.body.style.overflow = "hidden";
	}

	static toggle(drawer) {
		if (drawer.classList.contains("open")) Drawers.close();
		else Drawers.open(drawer);
	}
}

// ===============================

class CartAPI {
	static postChgQty(id, delta) {
		return postData("/api/cart/chg-qty", { id: `${id}`, delta: `${delta}` });
	}

	static postRmv(id) {
		return postData("/api/cart/rmv", { id: `${id}` });
	}
}

class Product {
	static createCard(id, imagePath, title, desc, price, selQty, whQty) {
		if (!Number.isInteger(id)) id = Number.parseInt(id, 10);

		const fnRedir = () => window.location.href = `/product?id=${id}`;

		var productCard = document.createElement("div");
		productCard.classList.add("product-card");
		productCard.addEventListener("click", fnRedir);
		productCard.dataset.id = id;

		var productImage = document.createElement("img");
		productImage.classList.add("product-image");
		productImage.src = imagePath;
		productImage.alt = "Изображение товара";
		productImage.addEventListener("click", fnRedir);

		var productTitle = document.createElement("h3");
		productTitle.classList.add("product-title");
		productTitle.innerHTML = title;
		productTitle.addEventListener("click", fnRedir);

		var productDescription = document.createElement("p");
		productDescription.classList.add("product-description");
		productDescription.innerHTML = desc;
		productDescription.addEventListener("click", fnRedir);

		var productPrice = document.createElement("div");
		productPrice.classList.add("product-price");
		productPrice.innerHTML = price;
		productPrice.addEventListener("click", fnRedir);

		var controls = document.createElement("div");
		controls.classList.add("cart-controls", "hidden");

		var qtyRow = document.createElement("div");
		qtyRow.classList.add("cart-quantity-row");

		var txtAmount = document.createElement("span");
		txtAmount.innerHTML = "Количество:";

		var inpAmount = document.createElement("input");
		inpAmount.classList.add("quantity-input");
		inpAmount.type = "number";
		inpAmount.min = "1";
		inpAmount.value = `${selQty}`;

		var btnIncQty = document.createElement("button");
		btnIncQty.classList.add("btn-increase-qty", "cart-actions-btn");
		btnIncQty.innerHTML = "+";

		var btnDecQty = document.createElement("button");
		btnDecQty.classList.add("btn-decrease-qty", "cart-actions-btn");
		btnDecQty.innerHTML = "-";

		qtyRow.appendChild(txtAmount);
		qtyRow.appendChild(inpAmount);
		qtyRow.appendChild(btnIncQty);
		qtyRow.appendChild(btnDecQty);

		var stockRow = document.createElement("div");
		stockRow.classList.add("cart-stock-row");

		var txtWhAmount = document.createElement("span");
		txtWhAmount.innerHTML = `На складах: ${whQty}`

		var btnRemoveFromCart = document.createElement("button");
		btnRemoveFromCart.classList.add("btn-remove-from-cart", "cart-actions-btn");
		btnRemoveFromCart.innerHTML = "Убрать из корзины";

		stockRow.appendChild(txtWhAmount);
		stockRow.appendChild(btnRemoveFromCart);

		controls.appendChild(qtyRow);
		controls.appendChild(stockRow);

		var btnAddToCart = document.createElement("button");
		btnAddToCart.classList.add("btn-add-to-cart", "cart-actions-btn");
		btnAddToCart.innerHTML = "В корзину";
		btnAddToCart.addEventListener("click", (e) => {
			controls.classList.remove("hidden");
			btnAddToCart.remove();
		});

		productCard.appendChild(productImage);
		productCard.appendChild(productTitle);
		productCard.appendChild(productDescription);
		productCard.appendChild(productPrice);
		productCard.appendChild(btnAddToCart);
		productCard.appendChild(controls);
		return productCard;
	}

	static setUI(inCart, controls, btnAddToCart) {
		controls.classList.toggle("hidden", !inCart);
		btnAddToCart.classList.toggle("hidden", inCart);
	}

	static setControls(controls, enable) {
		[...controls].forEach(c => c.disabled = !enable);
	}

	static addToCart(id, controls, btnAddToCart) {
		Product.setUI(true, controls, btnAddToCart);
		Product.setControls(false);

		CartAPI.postChgQty(id, 1).catch(() => Product.setUI(false, controls, btnAddToCart)).finally(
			() => Product.setControls(true)
		);
	}

	static removeFromCart(id, controls, btnAddToCart) {
		Product.setUI(false, controls, btnAddToCart);
		Product.setControls(false);

		CartAPI.postRmv(id).catch(() => Product.setUI(true, controls, btnAddToCart));
	}

	static increaseQty(id, inpAmount) {
		const oldValue = Number(inpAmount.value);
		inpAmount.value = `${(oldValue + 1)}`;
		
		Product.setControls(false);
		CartAPI.postChgQty(id, 1).catch(() => inpAmount.value = `${(oldValue)}`);
	}

	static decreaseQty(id, inpAmount, controls, btnAddToCart) {
		const oldValue = Number(inpAmount.value);
		if (oldValue <= 1) {
			Product.removeFromCart(id, controls, btnAddToCart);
			return;
		}

		inpAmount.value = `${(oldValue - 1)}`;
		CartAPI.postChgQty(id, -1).catch(() => inpAmount.value = `${(oldValue)}`);
	}
}

document.addEventListener("DOMContentLoaded", () => {
	const tbCart = document.getElementById("tb-cart");
	const tbProfile = document.getElementById("tb-profile");
	const cartDrawer = document.getElementById("cart-drawer");
	const profileDrawer = document.getElementById("profile-drawer");
	const closeDrawers = document.querySelectorAll(".drawer-close");

	const mainGrid = document.getElementById("main-grid");

	// drawers
	
	Drawers.init();
	tbCart.addEventListener("click", () => Drawers.toggle(cartDrawer));
	tbProfile.addEventListener("click", () => Drawers.toggle(profileDrawer));
	closeDrawers.forEach(el => el.addEventListener("click", Drawers.close));
	document.addEventListener("keydown", (event) => { if (event.key === "Escape") Drawers.close(); });

	// ...


	var pc1 = Product.createCard("static/img/question.svg", "Название", "Краткое описание", "Цена (₽)", 1, 15);
	console.log(pc1);
	mainGrid.appendChild(pc1);
});
