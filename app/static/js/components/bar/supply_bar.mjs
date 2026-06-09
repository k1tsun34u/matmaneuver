import SupplyStatus from '../../supply_status.mjs';


export default class SupplyBar {
	constructor(redirectUrl, plannedDeliveryDate, totalPrice, status) {
		this._redirectUrl = redirectUrl;
		this._redirectFunction = () => {window.location.href = this._redirectUrl;};

		this._base = document.createElement('div');
		this._base.classList.add('hcont');

		this._elPlannedDeliveryDate = document.createElement('p');
		this._elPlannedDeliveryDate.classList.add('supply-bar-planned-delivery-date');
		this._elPlannedDeliveryDate.innerHTML = plannedDeliveryDate;
		this._elPlannedDeliveryDate.style.fontWeight = 'bold';
		this._elPlannedDeliveryDate.style.cursor = 'pointer';
		this._elPlannedDeliveryDate.addEventListener('click', () => {this._redirectFunction();});

		this._elTotalPrice = document.createElement('p');
		this._elTotalPrice.classList.add('supply-bar-total-price');
		this.totalPrice = totalPrice;
		this._elTotalPrice.style.color = '#21c800';
		this._elTotalPrice.style.cursor = 'pointer';
		this._elTotalPrice.addEventListener('click', () => {this._redirectFunction();});

		this._elStatus = document.createElement('p');
		this._elStatus.classList.add('supply-bar-status');
		this._elStatus.innerHTML = SupplyStatus.ValueToStr(status);
		this._elStatus.style.color = SupplyStatus.StrToColor(this._elStatus.innerHTML);
		this._elStatus.style.cursor = 'pointer';
		this._elStatus.addEventListener('click', () => {this._redirectFunction();});

		this.appendChild(this._elPlannedDeliveryDate);
		this.appendChild(this._elTotalPrice);
		this.appendChild(this._elStatus);
	}

	get base() {return this._base;}
	get redirectUrl() {return this._redirectUrl;}

	set redirectUrl(redirectUrl) {this._redirectUrl = redirectUrl;}
	set totalPrice(totalPrice) {this._elTotalPrice.innerHTML = `${totalPrice}₽`;}
	
	childNodes() {return this._base.childNodes;}
	appendChild(node) {this._base.appendChild(node);}
	prepend(node) {this._base.prepend(node);}
};
