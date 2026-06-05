import OrderStatus from "../order_status.mjs";
import BaseBar from "./base_bar.mjs";


export default class OrderBar extends BaseBar {
	constructor(id, trackNumber, totalPrice, status) {
		super(`/client/order/${id}`);

		this._elId = document.createElement('p');
		this._elId.innerHTML = `#${id}`;
		this._elId.style.maxWidth = '7%';
		this._elId.style.cursor = 'pointer';
		this._elId.addEventListener('click', () => {this._redirectFunction();});

		this._elTrackNumber = document.createElement('p');
		this._elTrackNumber.classList.add('bar-track-num');
		this._elTrackNumber.innerHTML = `${trackNumber}`;
		this._elTrackNumber.style.cursor = 'pointer';
		this._elTrackNumber.addEventListener('click', () => {this._redirectFunction();});

		this._elTotalPrice = document.createElement('p');
		this._elTotalPrice.innerHTML = `${totalPrice}₽`;
		this._elTotalPrice.style.cursor = 'pointer';
		this._elTotalPrice.style.color = '#21c800';
		this._elTotalPrice.addEventListener('click', () => {this._redirectFunction();});

		this._elStatus = document.createElement('p');
		this._elStatus.innerHTML = OrderStatus.ValueToStr(status);
		this._elStatus.style.cursor = 'pointer';
		this._elStatus.style.color = OrderStatus.StrToColor(this._elStatus.innerHTML);
		this._elStatus.addEventListener('click', () => {this._redirectFunction();});

		this.appendChild(this._elId);
		this.appendChild(this._elTrackNumber);
		this.appendChild(this._elTotalPrice);
		this.appendChild(this._elStatus);
	}

	get elId() {return this._elId;}
	get elTrackNumber() {return this._elTrackNumber;}
	get elTotalPrice() {return this._elTotalPrice;}
	get elStatus() {return this._elStatus;}
};
