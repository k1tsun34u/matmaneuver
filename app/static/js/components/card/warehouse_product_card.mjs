export default class WarehouseProductCard {
	constructor(redirectUrl, storageKey, name, price, qty, productId) {
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

		this._elQty = document.createElement('p');
		this._elQty.classList.add('card-qty');
		this.qty = qty;
		this._elQty.style.cursor = 'pointer';
		this._elQty.addEventListener('click', () => {this._redirectFunction();});

		this._base.appendChild(this._elImg);
		this._base.appendChild(this._elName);
		this._base.appendChild(this._elPrice);
		this._base.appendChild(this._elQty);
	}

	get base() {return this._base;}

	set storageKey(storageKey) {
		const imgPath = `/image/${storageKey && storageKey != '?' ? storageKey : 'question.svg'}`;
		this._elImg.src = imgPath;
	}

	get name() {return this._elName.innerHTML;}
	set name(name) {this._elName.innerHTML = name;}

	set price(price) {this._elPrice.innerHTML = `Цена: ${price} ₽/шт`;}

	get qty() {return this._elQty && parseFloat(this._elQty.innerHTML.split(' ')[0]);}
	set qty(quantity) {this._elQty && (this._elQty.innerHTML = `Кол-во: ${quantity} шт`);}
};
