import PaymentMethod from "../../payment_method.mjs";


export default class PaymentBar {
	constructor(redirectUrl, trackNumber, amount, paymentMethod) {
		this._redirectUrl = redirectUrl;
		this._redirectFunction = () => {window.location.href = this._redirectUrl;};

		this._base = document.createElement('div');
		this._base.classList.add('hcont');

		this._elTrackNumber = document.createElement('p');
		this._elTrackNumber.classList.add('payment-bar-track-number');
		this._elTrackNumber.innerHTML = trackNumber;
		this._elTrackNumber.style.fontWeight = 'bold';
		this._elTrackNumber.style.cursor = 'pointer';
		this._elTrackNumber.addEventListener('click', () => {this._redirectFunction();});

		this._elAmount = document.createElement('p');
		this._elAmount.classList.add('payment-bar-amount');
		this._elAmount.innerHTML = `${amount}₽`;
		this._elAmount.style.color = '#21c800';
		this._elAmount.style.cursor = 'pointer';
		this._elAmount.addEventListener('click', () => {this._redirectFunction();});

		this._elPaymentMethod = document.createElement('p');
		this._elPaymentMethod.classList.add('payment-bar-payment-method');
		this._elPaymentMethod.innerHTML = PaymentMethod.ValueToStr(paymentMethod);
		this._elPaymentMethod.style.color = PaymentMethod.StrToColor(this._elPaymentMethod.innerHTML);
		this._elPaymentMethod.style.cursor = 'pointer';
		this._elPaymentMethod.addEventListener('click', () => {this._redirectFunction();});

		this.appendChild(this._elTrackNumber);
		this.appendChild(this._elAmount);
		this.appendChild(this._elPaymentMethod);
	}

	get base() {return this._base;}
	get elTrackNumber() {return this._elTrackNumber;}
	get elAmount() {return this._elAmount;}
	get elPaymentMethod() {return this._elPaymentMethod;}
	get redirectUrl() {return this._redirectUrl;}

	set redirectUrl(redirectUrl) {this._redirectUrl = redirectUrl;}
	set trackNumber(trackNumber) {this._elTrackNumber.innerHTML = trackNumber;}
	
	childNodes() {return this._base.childNodes;}
	appendChild(node) {this._base.appendChild(node);}
	prepend(node) {this._base.prepend(node);}
};
