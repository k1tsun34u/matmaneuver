import Pagination from "../../components/pagination.mjs";
import Users from '../../api/employee/users.mjs';
import Status from "../../status.mjs";
import Employees from "../../api/employee/employees.mjs";
import SelectableUserBar from "../../components/bar/selectable_user_bar.mjs";
import DateConv from "../../date_conv.mjs";


let elHiredAt = document.getElementById('hired_at');
let elSearch = document.getElementById('search');
let elSearchBtn = document.getElementById('search_btn');
let elTgt = document.getElementById('tgt');
let elPrevPg = document.getElementById('prev_pg');
let elPageNumber = document.getElementById('page_number');
let elNextPg = document.getElementById('next_pg');
let elCreate = document.getElementById('create');

let elSelectedUserBar = null;
let pagination = new Pagination(
	() => (page) => Users.Search(elSearch.value, page, true, true),
	(page, r) => {
		elPageNumber.innerHTML = `Страница: ${page + 1}`;

		if (r['users'].length < 1) elTgt.innerHTML = '<p>Пусто...</p>';
		else {
			elTgt.innerHTML = '';
			r['users'].forEach(user => {
				let selectableUserBar = new SelectableUserBar(
					user['full_name'],
					user['phone'],
					user['email'],
					user['id'],
					(id) => {
						if (elSelectedUserBar != null) {
							if (elSelectedUserBar == selectableUserBar) return;
							elSelectedUserBar.deselect();
						}

						elSelectedUserBar = selectableUserBar;
					}
				);

				elTgt.appendChild(selectableUserBar.base);
			});
		}
	}
);

elCreate.addEventListener('click', () => {
	if (elSelectedUserBar == null) {
		Status.ShowError('Пользователь не выбран!');
		return;
	}
	else if (!elHiredAt.value) {
		Status.ShowError('Дата найма не выбрана!');
		return;
	}

	Employees.Register(
		elSelectedUserBar.id,
		DateConv.DateTimeToStr(elHiredAt.value)
	).then(r => {
		window.location.href = `/employee/employee/${r['employee_id']}`
	}).catch(e => Status.ShowError(e));
});
