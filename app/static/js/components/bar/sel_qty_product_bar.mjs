

export default class SelQtyProductBar {
	constructor(name, price, qty, productId, onClickCallback) {
		this._base = document.createElement('div');
		this._base.classList.add('hcont', 'sel-qty-product-bar');

		this._id = productId;

		this._elName = document.createElement('p');
		this._elName.classList.add('sel-qty-product-bar-name');
		this._elName.style.fontWeight = 'bold';
		this.name = name;

		this._elPrice = document.createElement('p');
		this._elPrice.classList.add('sel-qty-product-bar-price');
		this._elPrice.style.color = '#21c800';
		this.price = price;

		this._elQtyContainer = document.createElement('div');
		this._elQtyContainer.classList.add('hcont', 'sel-qty-product-bar-qty-container');
		
		this._elQty = document.createElement('p');
		this._elQty.classList.add('sel-qty-product-bar-price');
		this.qty = qty;

		this._elIncQty = document.createElement('button');
		this._elIncQty.innerHTML = '+';
		this._elIncQty.addEventListener('click', () => {
			this.qty = this.qty + 1;
			onClickCallback(this._id, true, this.qty);
		});

		this._elDecQty = document.createElement('button');
		this._elDecQty.innerHTML = '-';
		this._elDecQty.addEventListener('click', () => {
			if (this.qty > 0) {
				this.qty = this.qty - 1;
				onClickCallback(this._id, false, this.qty);
			}
		});

		this._elQtyContainer.appendChild(this._elQty);
		this._elQtyContainer.appendChild(this._elIncQty);
		this._elQtyContainer.appendChild(this._elDecQty);

		this._base.appendChild(this._elName);
		this._base.appendChild(this._elPrice);
		this._base.appendChild(this._elQtyContainer);
	}

	get id() {return this._id;}

	get base() {return this._base;}

	get name() {return this._elName.innerHTML;}
	set name(name) {this._elName.innerHTML = name;}

	get price() {return this._elPrice.innerHTML.split(' ')[0];}
	set price(price) {this._elPrice.innerHTML = `${price} ₽/шт`;}

	get qty() {return parseInt(this._elQty.innerHTML.split(' ')[0]);}
	set qty(qty) {
		this._elQty.innerHTML = `${qty} шт`;

		if (qty > 0) this._base.style.background = '#c5f3ff';
		else this._base.style.background = 'inherit';
	}
};
