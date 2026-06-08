import QtyProductBar from '../../components/bar/qty_product_bar.mjs';
import ProductImages from '../../api/employee/product_images.mjs';
import Pagination from '../../components/pagination.mjs';
import Supplies from '../../api/employee/supplies.mjs';
import Products from '../../api/employee/products.mjs';
import Status from '../../status.mjs';


let elSupplierFullName = document.getElementById('supplier_full_name');
let elWarehouseAddress = document.getElementById('warehouse_address');
let elPlannedDeliveryDate = document.getElementById('planned_delivery_date');
let elCreatedAt = document.getElementById('created_at');
let elSelStatus = document.getElementById('sel_status');
let elSetStatus = document.getElementById('set_status');
let elTgt = document.getElementById('tgt');
let elPrevPg = document.getElementById('prev_pg');
let elPageNumber = document.getElementById('page_number');
let elNextPg = document.getElementById('next_pg');

const pathName = window.location.pathname;
const sepPos = pathName.lastIndexOf('/');
if (sepPos != -1) {
	const supplyId = parseInt(pathName.substring(sepPos + 1));
	Supplies.Get(supplyId).then(r => {
		const fnStrToDate = (str) => {
			return new Date(str).toISOString().split('T')[0];
		};

		elSupplierFullName.innerHTML = `Поставщик: ${r['supply']['supplier_full_name']}`;
		elWarehouseAddress.innerHTML = `Склад: ${r['supply']['warehouse_address']}`;
		elPlannedDeliveryDate.innerHTML = `Планируемая дата доставки: ${fnStrToDate(r['supply']['planned_delivery_date'])}`;
		elCreatedAt.innerHTML = `Создана: ${fnStrToDate(r['supply']['created_at'])}`;
		elSelStatus.value = r['supply']['current_status'];
		elSetStatus.addEventListener('click', () => {
			Supplies.SetStatus(supplyId, elSelStatus.value).then(r2 => {
				window.location.href = `/employee/supply/${supplyId}`;
			}).catch(e => Status.ShowError(e));
		});

		let pagination = new Pagination(
			() => (page) => Supplies.GetItemsBySupply(supplyId, page),
			(page, r) => {
				elPageNumber.innerHTML = `Страница: ${page + 1}`;

				if (r['items'].length < 1) elTgt.innerHTML = '<p>Пусто...</p>';
				else {
					elTgt.innerHTML = '';

					r['items'].forEach(item => {
						let qtyProductBar = new QtyProductBar(
							'?',
							'?',
							item['quantity'],
							item['product_id']
						);
						
						Products.Get(item['product_id']).then(r2 => {
							let product = r2['product'];
							qtyProductBar.name = product['name'];
						}).catch(e => Status.ShowError(e));
	
						ProductImages.ByProduct(item['product_id']).then(r2 => {
							const images = r2['images'];
							if (images.length > 0) qtyProductBar.storageKey = images[0]['storage_key'];
						}).catch(e => Status.ShowError(e));
						elTgt.appendChild(qtyProductBar.base);
					});
				}
			}
		);
	}).catch(e => Status.ShowError(e));
}
