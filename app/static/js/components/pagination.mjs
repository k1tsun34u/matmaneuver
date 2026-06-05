import Status from "../status.mjs";

export default class Pagination {
	constructor(fnGetter, fnCallback) {
		this.fnGetter = fnGetter;
		this.fnCallback = fnCallback;

		this.page = 0;
		this.totalPages = null;
		this._loadPage(0);
	}

	update(currentPage, totalPages) {
		this.currentPage = currentPage;
		this.totalPages = totalPages;
	}

	_loadPage(page) {
		const fn = this.fnGetter();
		fn(page).then(response => {
			let pagination = response['pagination'];
			this.totalPages = pagination['total_pages'];
			this.page = page;
			this.fnCallback(page, response);
		}).catch(error => Status.ShowError(error));
	}

	select(page) {
		if (this.totalPages == null) return false;
		else if (page < 0 || page > this.totalPages) return false;
		this._loadPage(page);
	}

	prev() {
		if (this.totalPages == null) return false;
		else if (this.page == 0) return false;
		this.select(this.page - 1);
	}

	next() {
		if (this.totalPages == null) return false;
		else if (this.page >= this.totalPages - 1) return false;
		this.select(this.page + 1);
	}
};
