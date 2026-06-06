import Carts from '../../api/client/carts.mjs';
import Status from '../../status.mjs';


export default class ProductCard {
	constructor(redirectUrl, storageKey, name, price, productId) {
		this._redirectUrl = redirectUrl;
		this._redirectFunction = () => {window.location.href = this._redirectUrl;};

		this._productId = productId;

		this._base = document.createElement('div');
		this._base.classList.add('card');

		this._elImg = document.createElement('img');
		this._elImg.classList.add('card-img');
		this.storageKey = storageKey;
		this._elImg.style.cursor = 'pointer';
		this._elImg.addEventListener('click', () => {this._redirectFunction();});

		this._elName = document.createElement('p');
		this._elName.classList.add('card-name');
		this._elName.innerHTML = name;
		this._elName.style.fontWeight = 'bold';
		this._elName.style.cursor = 'pointer';
		this._elName.addEventListener('click', () => {this._redirectFunction();});

		this._elPrice = document.createElement('p');
		this._elPrice.classList.add('card-price');
		this.price = price;
		this._elPrice.style.color = '#21c800';
		this._elPrice.style.cursor = 'pointer';
		this._elPrice.addEventListener('click', () => {this._redirectFunction();});

		this._base.appendChild(this._elImg);
		this._base.appendChild(this._elName);
		this._base.appendChild(this._elPrice);

		this.refresh();
	}

	get base() {return this._base;}

	set storageKey(storageKey) {
		const imgPath = `/image/${storageKey && storageKey != '?' ? storageKey : 'question.svg'}`;
		this._elImg.src = imgPath;
	}

	set price(price) {this._elPrice.innerHTML = `Цена: ${price} ₽/шт`;}

	get qty() {return this._elQty && parseFloat(this._elQty.innerHTML.split(' ')[0]);}

	set qty(quantity) {this._elQty && (this._elQty.innerHTML = `${quantity} шт`);}

	refresh() {
		Carts.GetItems('ACTIVE', null, true).then(r => {
			let found = false;
			for (const item of r['items']) {
				if (item['product_id'] == this._productId) {
					if (this._elQty) this.qty = item['quantity'];
					else this.addElQtyContainer(item['quantity']);
					found = true;
					break;
				}
			}

			if (!found) this.addElAddToCart();
		}).catch(e => Status.ShowError(e));
	}

	addElAddToCart() {
		if (this._elQtyContainer) {
			this._elQtyContainer.remove();
			this._elQtyContainer = null;
			this._elQty.remove();
			this._elQty = null;
			this._elIncQty.remove();
			this._elIncQty = null;
			this._elDecQty.remove();
			this._elDecQty = null;
			this._elRemove.remove();
			this._elRemove = null;
		}

		this._elAddToCart = document.createElement('button');
		this._elAddToCart.classList.add('card-add-to-cart');
		this._elAddToCart.innerHTML = 'В корзину';
		this._elAddToCart.style.cursor = 'pointer';
		this._elAddToCart.addEventListener('click', () => {
			Carts.Add('ACTIVE', this._productId).then(r => {
				this.refresh();
			}).catch(e => Status.ShowError(e));
		});

		this._base.appendChild(this._elAddToCart);
	}

	addElQtyContainer(quantity) {
		if (this._elAddToCart) {
			this._elAddToCart.remove();
			this._elAddToCart = null;
		}

		this._elQtyContainer = document.createElement('div');
		this._elQtyContainer.classList.add('card-qty-container');

		this._elQty = document.createElement('p');
		this._elQty.classList.add('card-qty');
		this.qty = quantity;

		this._elIncQty = document.createElement('button');
		this._elIncQty.classList.add('card-qty-btn');
		this._elIncQty.innerHTML = '+';
		this._elIncQty.addEventListener('click', () => {
			Carts.Add('ACTIVE', this._productId).then(r => {
				this.qty = (this.qty + 1);
			}).catch(e => Status.ShowError(e));
		});

		this._elDecQty = document.createElement('button');
		this._elDecQty.classList.add('card-qty-btn');
		this._elDecQty.innerHTML = '-';
		this._elDecQty.addEventListener('click', () => {
			if (this.qty < 2) return;

			Carts.Dec('ACTIVE', this._productId).then(r => {
				this.qty = (this.qty - 1);
			}).catch(e => Status.ShowError(e));
		});

		this._elRemove = document.createElement('button');
		this._elRemove.classList.add('card-qty-btn', 'red-bg');
		this._elRemove.innerHTML = 'x';
		this._elRemove.addEventListener('click', () => {
			Carts.RemoveItem('ACTIVE', this._productId).then(r => {
				this.addElAddToCart(this.qty);
			});
		});

		this._elQtyContainer.appendChild(this._elQty);
		this._elQtyContainer.appendChild(this._elIncQty);
		this._elQtyContainer.appendChild(this._elDecQty);
		this._elQtyContainer.appendChild(this._elRemove);
		
		this._base.appendChild(this._elQtyContainer);
	}
};
