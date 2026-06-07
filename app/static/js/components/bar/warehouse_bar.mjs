export default class WarehouseBar {
	constructor(address, deleted, warehouseId) {
		this._redirectUrl = `/employee/warehouse/${warehouseId}`;
		this._redirectFunction = () => window.location.href = this._redirectUrl;

		this._base = document.createElement('div');
		this._base.classList.add('hcont');

		this._elAddress = document.createElement('p');
		this._elAddress.classList.add('warehouse-bar-address');
		this._elAddress.innerHTML = address;
		this._elAddress.style.cursor = 'pointer';
		this._elAddress.style.fontWeight = 'bold';
		this._elAddress.addEventListener('click', () => {this._redirectFunction();});

		this._elStatus = document.createElement('p');
		this._elStatus.classList.add('warehouse-bar-status');
		this.deleted = deleted;
		this._elStatus.style.cursor = 'pointer';
		this._elStatus.addEventListener('click', () => {this._redirectFunction();});
		
		this.appendChild(this._elAddress);
		this.appendChild(this._elStatus);
	}
	
	get base() {return this._base;}

	get deleted() {return this._elStatus.innerHTML == 'Удалён';}
	set deleted(deleted) {
		if (deleted) {
			this._elStatus.innerHTML = 'Удалён';
			this._elStatus.style.color = "red";
		}
		else {
			this._elStatus.innerHTML = 'Активен';
			this._elStatus.style.color = "lime";
		}
	}
	
	childNodes() {return this._base.childNodes;}
	appendChild(node) {this._base.appendChild(node);}
	prepend(node) {this._base.prepend(node);}
};
