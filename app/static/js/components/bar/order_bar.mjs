import OrderStatus from '../../order_status.mjs';


export default class OrderBar {
	constructor(redirectUrl, trackNumber, totalPrice, status) {
		this._redirectUrl = redirectUrl;
		this._redirectFunction = () => {window.location.href = this._redirectUrl;};

		this._base = document.createElement('div');
		this._base.classList.add('hcont');

		this._elTrackNumber = document.createElement('p');
		this._elTrackNumber.classList.add('order-bar-track-number');
		this._elTrackNumber.innerHTML = trackNumber;
		this._elTrackNumber.style.fontWeight = 'bold';
		this._elTrackNumber.style.cursor = 'pointer';
		this._elTrackNumber.addEventListener('click', () => {this._redirectFunction();});

		this._elTotalPrice = document.createElement('p');
		this._elTotalPrice.classList.add('order-bar-total-price');
		this.totalPrice = totalPrice;
		this._elTotalPrice.style.color = '#21c800';
		this._elTotalPrice.style.cursor = 'pointer';
		this._elTotalPrice.addEventListener('click', () => {this._redirectFunction();});

		this._elStatus = document.createElement('p');
		this._elStatus.classList.add('order-bar-status');
		this._elStatus.innerHTML = OrderStatus.ValueToStr(status);
		this._elStatus.style.color = OrderStatus.StrToColor(this._elStatus.innerHTML);
		this._elStatus.style.cursor = 'pointer';
		this._elStatus.addEventListener('click', () => {this._redirectFunction();});

		this.appendChild(this._elTrackNumber);
		this.appendChild(this._elTotalPrice);
		this.appendChild(this._elStatus);
	}

	get base() {return this._base;}
	get elTrackNumber() {return this._elTrackNumber;}
	get elTotalPrice() {return this._elTotalPrice;}
	get elStatus() {return this._elStatus;}
	get redirectUrl() {return this._redirectUrl;}

	set redirectUrl(redirectUrl) {this._redirectUrl = redirectUrl;}
	set totalPrice(totalPrice) {this._elTotalPrice.innerHTML = `${totalPrice}₽`;}
	
	childNodes() {return this._base.childNodes;}
	appendChild(node) {this._base.appendChild(node);}
	prepend(node) {this._base.prepend(node);}
};
