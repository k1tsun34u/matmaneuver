import Fetch from '../../fetch.mjs';
import Cookies from '../../cookies.mjs';


export default class Categories {
	static URL_PREFIX = "/api/employee/categories";

	static Create(name, parentCategoryId=null) {
		return Fetch.PostJson(
			`${Categories.URL_PREFIX}/create`,
			{name, parent_category_id: parentCategoryId},
			Cookies.Get('session')
		);
	}

	static SetParentCategory(categoryId, parentCategoryId) {
		return Fetch.PostJson(
			`${Categories.URL_PREFIX}/set-parent-category/${categoryId}`,
			{parent_category_id: parentCategoryId},
			Cookies.Get('session')
		);
	}

	static Deactivate(categoryId) {
		return Fetch.PostJson(`${Categories.URL_PREFIX}/deactivate/${categoryId}`, null, Cookies.Get('session'));
	}

	static Restore(categoryId) {
		return Fetch.PostJson(`${Categories.URL_PREFIX}/restore/${categoryId}`, null, Cookies.Get('session'));
	}

	static Get(categoryId) {
		return Fetch.GetJson(`${Categories.URL_PREFIX}/${categoryId}`, null, Cookies.Get('session'));
	}

	static ByName(name) {
		return Fetch.GetJson(`${Categories.URL_PREFIX}/by-name/${name}`, null, Cookies.Get('session'));
	}

	static Search(search, page=0, excludeDeactivated=true) {
		return Fetch.GetJson(
			`${Categories.URL_PREFIX}/search`,
			{
				search, page,
				exclude_deactivated: excludeDeactivated
			},
			Cookies.Get('session')
		);
	}
}
