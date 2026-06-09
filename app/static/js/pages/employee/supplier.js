import Suppliers from "../../api/employee/suppliers.mjs";
import DateConv from "../../date_conv.mjs";
import Status from "../../status.mjs";


let elFullName = document.getElementById('full_name');
let elPhone = document.getElementById('phone');
let elEmail = document.getElementById('email');
let elAddress = document.getElementById('address');
let elUpdate = document.getElementById('update');
let elCreatedAt = document.getElementById('created_at');
let elDeactivatedAt = document.getElementById('deactivated_at');
let elDeactivatedBy = document.getElementById('deactivated_by');
let elAction = document.getElementById('action');

const pathName = window.location.pathname;
const sepPos = pathName.lastIndexOf('/');
if (sepPos != -1) {
	const supplierId = parseInt(pathName.substring(sepPos + 1));
	Suppliers.Get(supplierId).then(r => {
		let fnDateToStr = (date) => {
			if (date) return DateConv.DateTimeToStr(date);
			return 'никогда';
		}

		console.log(r['supplier']);

		elFullName.value = r['supplier']['full_name'];
		elPhone.value = r['supplier']['phone'];
		elEmail.value = r['supplier']['email'];
		elAddress.value = r['supplier']['address'];

		elUpdate.addEventListener('click', () => {
			Suppliers.Update(
				supplierId,
				elFullName.value,
				elPhone.value,
				elEmail.value,
				elAddress.value
			).then(r2 => {
				window.location.href = `/employee/supplier/${supplierId}`;
			}).catch(e => Status.ShowError(e));
		});

		elCreatedAt.innerHTML = `Создан : ${fnDateToStr(r['supplier']['created_at'])}`;
		elDeactivatedAt.innerHTML = `Когда деактивирован: ${fnDateToStr(r['supplier']['deactivated_at'])}`;
		elDeactivatedBy.innerHTML = `Кем деактивирован: ${r['supplier']['deactivated_by_full_name'] ?? 'никем'}`;

		if (r['supplier']['deactivated_at'] != null) {
			elAction.classList.add('green-bg');
			elAction.innerHTML = 'Восстановить поставщика';
			elAction.addEventListener('click', () => {
				Suppliers.Restore(supplierId).then(r2 => {
					window.location.href = `/employee/supplier/${supplierId}`;
				}).catch(e => Status.ShowError(e));
			});
		}
		else {
			elAction.classList.add('red-bg');
			elAction.innerHTML = 'Деактивировать поставщика';
			elAction.addEventListener('click', () => {
				Suppliers.Deactivate(supplierId).then(r2 => {
					window.location.href = `/employee/supplier/${supplierId}`;
				}).catch(e => Status.ShowError(e));
			});
		}
	}).catch(e => Status.ShowError(e));
}
