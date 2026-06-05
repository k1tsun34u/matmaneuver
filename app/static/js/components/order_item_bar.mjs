import BaseBar from './bar/base_bar.mjs';


export default class OrderItemBar extends BaseBar {
	constructor(productId, productName, itemId, purchasePrice, quantity) {
		super(`/client/product/${productId}`);

		this._elId = document.createElement('p');
		this._elId.innerHTML = `#${itemId}`;
		this._elId.style.maxWidth = '7%';
		this._elId.style.cursor = 'pointer';
		this._elId.addEventListener('click', () => {this._redirectFunction();});

		this._elName = document.createElement('p');
		this._elName.classList.add('order-item-bar-name');
		this._elName.innerHTML = `${productName}`;
		this._elName.style.cursor = 'pointer';
		this._elName.addEventListener('click', () => {this._redirectFunction();});

		this._elPurchasePrice = document.createElement('p');
		this._elPurchasePrice.innerHTML = `${purchasePrice}₽/шт`;
		this._elPurchasePrice.style.cursor = 'pointer';
		this._elPurchasePrice.style.color = '#21c800';
		this._elPurchasePrice.addEventListener('click', () => {this._redirectFunction();});

		this._elQuantity = document.createElement('p');
		this._elQuantity.innerHTML = `${quantity} шт`;
		this._elQuantity.style.cursor = 'pointer';
		this._elQuantity.style.color = '#0065df';
		this._elQuantity.addEventListener('click', () => {this._redirectFunction();});

		this.appendChild(this._elId);
		this.appendChild(this._elName);
		this.appendChild(this._elPurchasePrice);
		this.appendChild(this._elQuantity);
	}

	get elId() {return this._elId;}
	get elName() {return this._elName;}
	get elPurchasePrice() {return this._elPurchasePrice;}
	get elQuantity() {return this._elQuantity;}
};
