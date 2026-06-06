export default class Review {
	constructor(fullName, rating, commentary=null) {
		this._base = document.createElement('div');
		this._base.classList.add('review');

		this._elTopContainer = document.createElement('div');
		this._elTopContainer.classList.add('review-top-container');

		this._elFullName = document.createElement('p');
		this._elFullName.classList.add('review-full-name');
		this._elFullName.style.fontWeight = 'bold';
		this.fullName = fullName;

		this._elRating = document.createElement('div');
		this._elRating.classList.add('review-rating');

		for (let i = 0; i < 5; i++) {
			let star = document.createElement('img');
			star.classList.add(i < rating ? 'review-rating-checked-star' : 'review-rating-unchecked-star');

			this._elRating.appendChild(star);
		}

		this._elTopContainer.appendChild(this._elFullName);
		this._elTopContainer.appendChild(this._elRating);

		this._elComment = document.createElement('p');
		this._elComment.classList.add('review-comment');
		this._elComment.innerHTML = commentary;

		this._base.appendChild(this._elTopContainer);
		this._base.appendChild(this._elComment);
	}

	get base() {return this._base;}

	set fullName(fullName) {this._elFullName.innerHTML = fullName;}
};
