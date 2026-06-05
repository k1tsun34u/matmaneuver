export default class BaseBar {
	constructor(redirectUrl, imgStorageKey, name, price) {
		this._redirectUrl = redirectUrl;
		this._redirectFunction = () => {window.location.href = this.redirectUrl;};

		this._base = document.createElement('div');
		this._base.classList.add('hcont');
		this._base.style.cursor = 'pointer';
		// this._base.addEventListener('click', () => {this._redirectFunction();});

		// this._elImg = document.createElement('img');
		// this._elImg.classList.add('card-img');
		// this.setImg(imgStorageKey);
		// this._elImg.style.cursor = 'pointer';
		// this._elImg.addEventListener('click', () => {this._redirectFunction();});

		// this._elName = document.createElement('p');
		// this._elName.innerHTML = name;
		// this._elName.style.fontWeight = 'bold';
		// this._elName.style.cursor = 'pointer';
		// this._elName.addEventListener('click', () => {this._redirectFunction();});

		// this._elPrice = document.createElement('p');
		// this._elPrice.innerHTML = `${price}₽/шт`;
		// this._elPrice.style.color = '#21c800';
		// this._elPrice.style.cursor = 'pointer';
		// this._elPrice.addEventListener('click', () => {this._redirectFunction();});

		// this.appendChild(this._elImg);
		// this.appendChild(this._elName);
		// this.appendChild(this._elPrice);
	}

	get base() {return this._base;}
	// get elImg() {return this._elImg;}
	// get elName() {return this._elName;}
	// get elPrice() {return this._elPrice;}
	get redirectUrl() {return this._redirectUrl;}
	set redirectUrl(redirectUrl) {this._redirectUrl = redirectUrl;}
	
	childNodes() {return this._base.childNodes;}
	appendChild(node) {this._base.appendChild(node);}
	prepend(node) {this._base.prepend(node);}

	// setImg(storageKey) {
	// 	let imgPath = `/image/${!storageKey || storageKey == '?' ? 'question.svg' : storageKey}`;
	// 	this._elImg.src = imgPath;
	// }
};
