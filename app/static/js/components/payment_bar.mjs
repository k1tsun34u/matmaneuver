import OrderPayments from "../api/client/order_payments.mjs";
import PaymentMethod from "../payment_method.mjs";
import BaseBar from "./bar/base_bar.mjs";


export default class PaymentBar extends BaseBar {
	constructor(orderId, id, trackNumber, createdAt, amount, paymentMethod) {
		super(`/client/order/${orderId}`);

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

		this._elCreatedAt = document.createElement('p');
		this._elCreatedAt.innerHTML = `${new Date(createdAt).toISOString().slice(0, 19).replace('T', ' ')}`;
		this._elCreatedAt.style.cursor = 'pointer';
		this._elCreatedAt.addEventListener('click', () => {this._redirectFunction();});

		this._elAmount = document.createElement('p');
		this._elAmount.innerHTML = `${amount}₽`
		this._elAmount.style.color = '#21c800';
		this._elAmount.style.cursor = 'pointer';
		this._elAmount.addEventListener('click', () => {this._redirectFunction();});

		this._elPaymentMethod = document.createElement('p');
		this._elPaymentMethod.innerHTML = PaymentMethod.ValueToStr(paymentMethod);
		this._elPaymentMethod.style.color = PaymentMethod.StrToColor(this._elPaymentMethod.innerHTML);
		this._elPaymentMethod.style.cursor = 'pointer';
		this._elPaymentMethod.addEventListener('click', () => {this._redirectFunction();});

		this.appendChild(this._elId);
		this.appendChild(this._elTrackNumber);
		this.appendChild(this._elCreatedAt);
		this.appendChild(this._elAmount);
		this.appendChild(this._elPaymentMethod);
	}

	get elId() {return this._elId;}
	get elTrackNumber() {return this._elTrackNumber;}
	get elCreatedAt() {return this._elCreatedAt;}
	get elAmount() {return this._elAmount;}
	get elPaymentMethod() {return this._elPaymentMethod;}
};
