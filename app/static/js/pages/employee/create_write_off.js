import Products from "../../api/employee/products.mjs";
import Warehouses from "../../api/employee/warehouses.mjs";
import SelQtyProductBar from "../../components/bar/sel_qty_product_bar.mjs";
import Pagination from "../../components/pagination.mjs";
import Status from "../../status.mjs";
import WriteOffs from '../../api/employee/write_offs.mjs';


let elTitle = document.getElementById('title');
let elSelReason = document.getElementById('sel_reason');
let elComment = document.getElementById('comment');
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
		elTitle.innerHTML = `Списать товары со склада ${r['warehouse']['address']}`;

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
			if (Object.keys(selProducts).length < 1) {
				Status.ShowError('Не выбраны товары!');
				return;
			}

			let warehouseWriteOffsData = [];
			Object.keys(selProducts).forEach(key => warehouseWriteOffsData.push([
				parseInt(key),
				selProducts[key]
			]));

			WriteOffs.Create(
				warehouseId,
				elSelReason.value,
				warehouseWriteOffsData,
				elComment.value
			).then(r2 => {
				window.location.href = `/employee/warehouse/${warehouseId}/write-offs`;
			}).catch(e => Status.ShowError(e));
		});
		
		elSearchProductBtn.addEventListener('click', () => paginationProducts.select(0));
		elPrevPgProducts.addEventListener('click', e => paginationProducts.prev());
		elNextPgProducts.addEventListener('click', e => paginationProducts.next());
	}).catch(e => Status.ShowError(e));
}
