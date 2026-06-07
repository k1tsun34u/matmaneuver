export default class QtyProductBar {
	constructor(storageKey, name, qty, productId) {
		this._redirectUrl = `/employee/product/${productId}`;
		this._redirectFunction = () => window.location.href = this._redirectUrl;

		this._base = document.createElement('div');
		this._base.classList.add('hcont');

		this._elImg = document.createElement('img');
		this._elImg.classList.add('qty-product-bar-img');
		this.storageKey = storageKey;
		this._elImg.style.cursor = 'pointer';
		this._elImg.addEventListener('click', () => this._redirectFunction());

		this._elName = document.createElement('p');
		this._elName.classList.add('qty-product-bar-name');
		this._elName.innerHTML = name;
		this._elName.style.fontWeight = 'bold';
		this._elName.style.cursor = 'pointer';
		this._elName.addEventListener('click', () => {this._redirectFunction();});

		this._elQuantity = document.createElement('p');
		this._elQuantity.classList.add('qty-product-bar-qty');
		this.qty = qty;
		this._elQuantity.style.color = '#0046c7';
		this._elQuantity.style.cursor = 'pointer';
		this._elQuantity.addEventListener('click', () => {this._redirectFunction();});
		
		this.appendChild(this._elImg);
		this.appendChild(this._elName);
		this.appendChild(this._elQuantity);
	}
	
	get base() {return this._base;}

	set name(name) {this._elName.innerHTML = name;}
	set quantity(quantity) {this._elQuantity.innerHTML = `${quantity} шт`;}

	set storageKey(storageKey) {
		const fileName = storageKey && storageKey != '?' ? storageKey : 'question.svg';
		this._elImg.src = `/image/${fileName}`;
	}
	
	childNodes() {return this._base.childNodes;}
	appendChild(node) {this._base.appendChild(node);}
	prepend(node) {this._base.prepend(node);}
};
