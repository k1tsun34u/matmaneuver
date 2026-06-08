import WarehouseProductCard from '../../components/card/warehouse_product_card.mjs';
import ProductImages from '../../api/employee/product_images.mjs';
import Warehouses from '../../api/employee/warehouses.mjs';
import Pagination from '../../components/pagination.mjs';
import Products from '../../api/employee/products.mjs';
import Status from '../../status.mjs';


let elAddress = document.getElementById('address');
let elDescription = document.getElementById('description');
let elSetDescription = document.getElementById('set_description');
let elSupplies = document.getElementById('supplies');
let elWriteOffs = document.getElementById('write_offs');
let elTgt = document.getElementById('tgt');
let elPrevPg = document.getElementById('prev_pg');
let elPageNumber = document.getElementById('page_number');
let elNextPg = document.getElementById('next_pg');

const pathName = window.location.pathname;
const sepPos = pathName.lastIndexOf('/');
if (sepPos != -1) {
	const warehouseId = parseInt(pathName.substring(sepPos + 1));
	Warehouses.Get(warehouseId).then(r => {
		elAddress.innerHTML = `Адрес: ${r['warehouse']['address']}`;
		elDescription.value = r['warehouse']['description'];

		elSetDescription.addEventListener('click', () => {
			Warehouses.SetDescription(warehouseId, elDescription.value).then(r2 => {
				window.location.href = `/employee/warehouse/${warehouseId}`;
			}).catch(e => Status.ShowError(e));
		});

		elSupplies.href = `/employee/warehouse/${warehouseId}/supplies`
		elWriteOffs.href = `/employee/warehouse/${warehouseId}/write-offs`
	}).catch(e => Status.ShowError(e));

	let pagination = new Pagination(
		() => (page) => Warehouses.GetProductsByWarehouse(
			warehouseId,
			page
		),
		(page, r) => {
			elPageNumber.innerHTML = `Страница: ${page + 1}`;

			if (r['products'].length < 1) elTgt.innerHTML = '<p>Пусто...</p>';
			else {
				elTgt.innerHTML = '';
				r['products'].forEach(product => {
					console.log(product);
					let warehouseProductCard = new WarehouseProductCard(
						`/employee/product/${product['product_id']}`,
						null,
						'?',
						'?',
						product['quantity'],
						product['product_id']
					);

					Products.Get(product['product_id']).then(r2 => {
						product = r2['product'];
						warehouseProductCard.name = product['name'];
						warehouseProductCard.price = product['price'];
					}).catch(e => Status.ShowError(e));

					ProductImages.ByProduct(product['product_id']).then(r2 => {
						const images = r2['images'];
						if (images.length > 0) warehouseProductCard.storageKey = images[0]['storage_key'];
					}).catch(e => Status.ShowError(e));
					elTgt.appendChild(warehouseProductCard.base);
				});
			}
		}
	);

	elPrevPg.addEventListener('click', e => pagination.prev());
	elNextPg.addEventListener('click', e => pagination.next());
}
