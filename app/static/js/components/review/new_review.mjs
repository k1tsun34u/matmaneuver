export default class NewReview {
	constructor(fullName, onPost) {
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
			star.classList.add(!i ? 'review-rating-checked-star' : 'review-rating-unchecked-star');
			star.addEventListener('click', () => {this.rating = i + 1;});

			this._elRating.appendChild(star);
		}

		this._elTopContainer.appendChild(this._elFullName);
		this._elTopContainer.appendChild(this._elRating);

		this._elComment = document.createElement('textarea');
		this._elComment.classList.add('new-review-comment');
		this._elComment.value = 'Классный товар!';

		this._elPost = document.createElement('button');
		this._elPost.classList.add('review-post', 'green-bg');
		this._elPost.innerHTML = 'Опубликовать отзыв';
		this._elPost.addEventListener('click', () => {onPost(this.fullName, this.rating, this.comment);});

		this._elRemove = document.createElement('button');
		this._elRemove.classList.add('review-remove', 'red-bg');
		this._elRemove.innerHTML = 'Удалить отзыв';
		this._elRemove.addEventListener('click', () => {this._base.remove();});

		this._base.appendChild(this._elTopContainer);
		this._base.appendChild(this._elComment);
		this._base.appendChild(this._elPost);
		this._base.appendChild(this._elRemove);
	}

	get base() {return this._base;}

	get fullName() {return this._elFullName.innerHTML;}
	set fullName(fullName) {this._elFullName.innerHTML = fullName;}

	get rating() {
		let res = 0;
		for (let i = 0; i < 5; i++) if (
			this._elRating.childNodes[i].classList.contains(
				'review-rating-checked-star'
			)
		) res = i + 1;
		return res;
	}

	set rating(rating) {
		for (let i = 0; i < 5; i++) {
			if (i < rating) {
				this._elRating.childNodes[i].classList.add('review-rating-checked-star');
				this._elRating.childNodes[i].classList.remove('review-rating-unchecked-star');
			}
			else {
				this._elRating.childNodes[i].classList.add('review-rating-unchecked-star');
				this._elRating.childNodes[i].classList.remove('review-rating-checked-star');
			}
		}
	}

	get comment() {
		let value = this._elComment.value;
		return value.length > 0 ? value : '';
	}
};
