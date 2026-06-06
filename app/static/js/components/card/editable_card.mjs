import Carts from '../../api/client/carts.mjs';
import Status from '../../status.mjs';


export default class EditableCard {
	constructor(redirectUrl, storageKey, name, price, productId) {
		this._redirectUrl = redirectUrl;
		this._redirectFunction = () => {window.location.href = this._redirectUrl;};

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

		this._elEdit = document.createElement('button');
		this._elEdit.classList.add('card-edit');
		this._elEdit.innerHTML = 'Редактировать';
		this._elEdit.addEventListener('click', () => {this._redirectFunction();});

		this._base.appendChild(this._elImg);
		this._base.appendChild(this._elName);
		this._base.appendChild(this._elPrice);
		this._base.appendChild(this._elEdit);
	}

	get base() {return this._base;}

	set storageKey(storageKey) {
		const fileName = storageKey && storageKey != '?' ? storageKey : 'question.svg';
		this._elImg.src = `/image/${fileName}`;
	}

	set price(totalPrice) {
		this._elPrice.innerHTML = `Цена: ${totalPrice} ₽/шт`;
	}
};
