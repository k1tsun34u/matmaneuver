import SelQtyProductBar from '../../components/bar/sel_qty_product_bar.mjs';
import Warehouses from '../../api/employee/warehouses.mjs';
import Pagination from '../../components/pagination.mjs';
import Products from '../../api/employee/products.mjs';
import Status from '../../status.mjs';
import Supplies from '../../api/employee/supplies.mjs';
import Suppliers from '../../api/employee/suppliers.mjs';
import SelSupplierBar from '../../components/bar/sel_supplier_bar.mjs';


let elTitle = document.getElementById('title');
let elPlannedDeliveryDate = document.getElementById('planned_delivery_date');

let elSearchSuppliers = document.getElementById('search_suppliers');
let elSearchSuppliersBtn = document.getElementById('search_suppliers_btn');
let elTgtSuppliers = document.getElementById('tgt_suppliers');
let elPrevPgSuppliers = document.getElementById('prev_pg_suppliers');
let elPageNumberSuppliers = document.getElementById('page_number_suppliers');
let elNextPgSuppliers = document.getElementById('next_pg_suppliers');

let elSearchProduct = document.getElementById('search_products');
let elSearchProductBtn = document.getElementById('search_products_btn');
let elTgtProducts = document.getElementById('tgt_products');
let elPrevPgProducts = document.getElementById('prev_pg_products');
let elPageNumberProducts = document.getElementById('page_number_products');
let elNextPgProducts = document.getElementById('next_pg_products');

let elCreate = document.getElementById('create');

const pathname = window.location.pathname;
const lastSepPos = pathname.lastIndexOf('/');
const prevLastSepPos = pathname.lastIndexOf('/', lastSepPos - 1);
if (lastSepPos != -1 && prevLastSepPos != -1) {
	const warehouseId = pathname.substring(prevLastSepPos + 1, lastSepPos);

	Warehouses.Get(warehouseId).then(r => {
		elTitle.innerHTML = `Создать поставку на склад ${r['warehouse']['address']}`;

		let elSelectedSupplier = null;
		let paginationSuppliers = new Pagination(
			() => (page) => Suppliers.Search(elSearchSuppliers.value, page),
			(page, r) => {
				elPageNumberSuppliers.innerHTML = `Страница: ${page + 1}`;
				
				if (r['suppliers'].length < 1) elTgtSuppliers.innerHTML = '<p>Пусто...</p>';
				else {
					elTgtSuppliers.innerHTML = '';
					r['suppliers'].forEach(supplier => {
						let elSelSupplierBar = new SelSupplierBar(
							supplier['full_name'],
							supplier['phone'],
							supplier['email'],
							supplier['id'],
							(id) => {
								if (elSelectedSupplier != null) {
									if (elSelectedSupplier == elSelSupplierBar) return;
									elSelectedSupplier.deselect();
								}

								elSelectedSupplier = elSelSupplierBar;
							}
						);

						elTgtSuppliers.appendChild(elSelSupplierBar.base);
					});
				}
			}
		)
		
		elSearchSuppliersBtn.addEventListener('click', () => paginationSuppliers.select(0));
		elPrevPgSuppliers.addEventListener('click', e => paginationSuppliers.prev());
		elNextPgSuppliers.addEventListener('click', e => paginationSuppliers.next());

		let selProducts = {};
		let paginationProducts = new Pagination(
			() => (page) => Products.Search(elSearchProduct.value, page, null, null, true),
			(page, r) => {
				elPageNumberProducts.innerHTML = `Страница: ${page + 1}`;
				
				if (r['products'].length < 1) elTgtProducts.innerHTML = '<p>Пусто...</p>';
				else {
					elTgtProducts.innerHTML = '';
					r['products'].forEach(product => {
						let selQtyProductBar = new SelQtyProductBar(
							product['name'],
							product['price'],
							0,
							product['id'],
							(id, increased, newQty) => {
								if (increased) selProducts[product['id']] = (selProducts[product['id']] ?? 0) + 1;
								else if (product['id'] in selProducts) {
									if (newQty > 0) selProducts[product['id']] = newQty;
									else delete selProducts[product['id']];
								}
							}
						);

						if (product['id'] in selProducts) selQtyProductBar.qty = selProducts[product['id']];
						elTgtProducts.appendChild(selQtyProductBar.base);
					});
				}
			}
		);

		elCreate.addEventListener('click', () => {
			if (elSelectedSupplier == null) {
				Status.ShowError('Поставщик не выбран!');
				return;
			}
			else if (Object.keys(selProducts).length < 1) {
				Status.ShowError('Не выбраны товары!');
				return;
			}
			else if (!elPlannedDeliveryDate.value) {
				Status.ShowError('Не выбрана планируемая дата доставки!');
				return;
			}

			let warehouseSupplyData = [
				parseInt(warehouseId), new Date(
					elPlannedDeliveryDate.value
				).toISOString().slice(0, 19).replace('T', ' ')
			];

			Object.keys(selProducts).forEach(key => warehouseSupplyData.push([
				parseInt(key),
				selProducts[key]
			]));

			Supplies.Create(
				elSelectedSupplier.id,
				[warehouseSupplyData],
			).then(r2 => {
				window.location.href = `/employee/warehouse/${warehouseId}/supplies`;
			}).catch(e => Status.ShowError(e));
		});
		
		elSearchProductBtn.addEventListener('click', () => paginationProducts.select(0));
		elPrevPgProducts.addEventListener('click', e => paginationProducts.prev());
		elNextPgProducts.addEventListener('click', e => paginationProducts.next());
	}).catch(e => Status.ShowError(e));
}
