import Users from "../../api/employee/users.mjs";
import Pagination from "../../components/pagination.mjs";
import UserBar from "../../components/bar/user_bar.mjs";


let elSearch = document.getElementById('search');
let elSearchBtn = document.getElementById('search_btn');
let elExcludeBlocked = document.getElementById('exclude_blocked');
let elExcludeDeleted = document.getElementById('exclude_deleted');
let elTgt = document.getElementById('tgt');
let elPrevPg = document.getElementById('prev_pg');
let elPageNumber = document.getElementById('page_number');
let elNextPg = document.getElementById('next_pg');

let pagination = new Pagination(
	() => (page) => Users.Search(
		elSearch.value,
		page,
		elExcludeDeleted.checked,
		elExcludeBlocked.checked
	),
	(page, r) => {
		elPageNumber.innerHTML = `Страница: ${page + 1}`;

		if (r['users'].length < 1) elTgt.innerHTML = '<p>Пусто...</p>';
		else {
			elTgt.innerHTML = '';
			r['users'].forEach(user => {
				let userBar = new UserBar(
					user['full_name'],
					user['phone'],
					user['email'],
					user['id']
				);

				elTgt.appendChild(userBar.base);
			});
		}
	}
);

elSearchBtn.addEventListener('click', () => pagination.select(0));
elPrevPg.addEventListener('click', e => pagination.prev());
elNextPg.addEventListener('click', e => pagination.next());
