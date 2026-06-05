import Status from "../status.mjs";

export default class Pagination {
	constructor(fnGetter, fnCallback) {
		this.fnGetter = fnGetter;
		this.fnCallback = fnCallback;

		this.page = 0;
		this.total_pages = null;
		this._loadPage(0);
	}

	_loadPage(page) {
		const fn = this.fnGetter();
		fn(page).then(response => {
			let pagination = response['pagination'];
			this.total_pages = pagination['total_pages'];
			this.page = page;
			this.fnCallback(page, response);
		}).catch(error => Status.ShowError(error));
	}

	select(page) {
		if (this.total_pages == null) return false;
		else if (page < 0 || page > this.total_pages) return false;
		this._loadPage(page);
	}

	prev() {
		if (this.total_pages == null) return false;
		else if (this.page == 0) return false;
		this.select(this.page - 1);
	}

	next() {
		if (this.total_pages == null) return false;
		else if (this.page >= this.total_pages - 1) return false;
		this.select(this.page + 1);
	}
};
