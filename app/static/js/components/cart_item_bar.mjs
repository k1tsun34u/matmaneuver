import Status from '../status.mjs';
import BaseBar from "./bar/base_bar.mjs";
import Carts from '../api/client/carts.mjs';


export default class CartItemBar extends BaseBar {
	constructor(productId, imgStorageKey, productName, productPrice, quantity, cartType) {
		super(
			`/client/product/${productId}`,
			imgStorageKey,
			productName,
			productPrice
		);

		this._productId = productId;
		this._cartType = cartType;
		
		this._elRightContainer = document.createElement('div');
		this._elRightContainer.classList.add('right-container');
		if (quantity !== null) {
			this._elQuantity = document.createElement('p');
			this._elQuantity.innerHTML = `${quantity} шт`;

			this._elIncQty = document.createElement('button');
			this._elIncQty.innerHTML = '+';
			this._elIncQty.addEventListener('click', () => this.incQty());

			this._elDecQty = document.createElement('button');
			this._elDecQty.innerHTML = '-';
			this._elDecQty.addEventListener('click', () => this.decQty());

			this._elRightContainer.appendChild(this._elQuantity);
			this._elRightContainer.appendChild(this._elIncQty);
			this._elRightContainer.appendChild(this._elDecQty);
		}

		this._elRemoveFromCart = document.createElement('button');
		this._elRemoveFromCart.classList.add('red-bg');
		this._elRemoveFromCart.innerHTML = 'x';
		this._elRemoveFromCart.addEventListener('click', () => this.removeFromCart());

		this._elRightContainer.appendChild(this._elRemoveFromCart);

		this.appendChild(this._elRightContainer);
		this.appendChild(this._elRightContainer);
	}

	get elRightContainer() {return this._elRightContainer;}
	get elQuantity() {return this._elQuantity;}
	get elIncQty() {return this._elIncQty;}
	get elDecQty() {return this._elDecQty;}
	get elRemoveFromCart() {return this._elRemoveFromCart;}

	incQty() {
		Carts.Add(this._cartType, this._productId).then(r => {
			const subStr = this._elQuantity.innerHTML.substring(
				0,
				this._elQuantity.innerHTML.lastIndexOf(' ')
			);

			const curQty = parseInt(subStr);
			this._elQuantity.innerHTML = `${curQty + 1} шт`;
		}).catch(e => Status.ShowError(e));
	}

	decQty() {
		const subStr = this._elQuantity.innerHTML.substring(
			0,
			this._elQuantity.innerHTML.lastIndexOf(' ')
		);

		const curQty = parseInt(this._elQuantity.innerHTML);
		if (curQty < 2) return;

		Carts.Dec(this._cartType, this._productId).then(r => {
			this._elQuantity.innerHTML = `${curQty - 1} шт`;
		}).catch(e => Status.ShowError(e));
	}

	removeFromCart() {
		Carts.RemoveItem(this._cartType, this._productId).then(r => {
			this._base.remove();
		}).catch(e => Status.ShowError(e));
	}
};
