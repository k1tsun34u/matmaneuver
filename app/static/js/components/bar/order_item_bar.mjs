export default class OrderItemBar {
	constructor(redirectUrl, storageKey, name, price, quantity) {
		this._redirectUrl = redirectUrl;
		this._redirectFunction = () => {window.location.href = this._redirectUrl;};

		this._base = document.createElement('div');
		this._base.classList.add('hcont');

		this._elImage = document.createElement('img');
		this._elImage.classList.add('order-item-bar-img');
		this.storageKey = storageKey;
		this._elImage.style.cursor = 'pointer';
		this._elImage.addEventListener('click', () => {this._redirectFunction();});

		this._elName = document.createElement('p');
		this._elName.classList.add('order-item-bar-track-number');
		this._elName.innerHTML = name;
		this._elName.style.fontWeight = 'bold';
		this._elName.style.cursor = 'pointer';
		this._elName.addEventListener('click', () => {this._redirectFunction();});

		this._elPrice = document.createElement('p');
		this._elPrice.classList.add('order-item-bar-price');
		this.price = price;
		this._elPrice.style.color = '#21c800';
		this._elPrice.style.cursor = 'pointer';
		this._elPrice.addEventListener('click', () => {this._redirectFunction();});

		this._elQuantity = document.createElement('p');
		this._elQuantity.classList.add('order-item-bar-quantity');
		this.quantity = quantity;
		this._elQuantity.style.color = '#0046c7';
		this._elQuantity.style.cursor = 'pointer';
		this._elQuantity.addEventListener('click', () => {this._redirectFunction();});

		this.appendChild(this._elImage);
		this.appendChild(this._elName);
		this.appendChild(this._elPrice);
		this.appendChild(this._elQuantity);
	}

	get base() {return this._base;}
	get elImage() {return this._elImage;}
	get elName() {return this._elName;}
	get elPrice() {return this._elPrice;}
	get elQuantity() {return this._elQuantity;}
	get redirectUrl() {return this._redirectUrl;}

	set redirectUrl(redirectUrl) {this._redirectUrl = redirectUrl;}
	set name(name) {this._elName.innerHTML = name;}
	set price(totalPrice) {this._elPrice.innerHTML = `${totalPrice} ₽/шт`;}
	set quantity(quantity) {this._elQuantity.innerHTML = `${quantity} шт`;}

	set storageKey(storageKey) {
		const fileName = storageKey && storageKey != '?' ? storageKey : 'question.svg';
		this._elImage.src = `/image/${fileName}`;
	}
	
	childNodes() {return this._base.childNodes;}
	appendChild(node) {this._base.appendChild(node);}
	prepend(node) {this._base.prepend(node);}
};
