import QtyProductBar from '../../components/bar/qty_product_bar.mjs';
import ProductImages from '../../api/employee/product_images.mjs';
import WriteOffs from '../../api/employee/write_offs.mjs';
import Pagination from '../../components/pagination.mjs';
import Products from '../../api/employee/products.mjs';
import Status from '../../status.mjs';
import DateConv from '../../date_conv.mjs';
import WriteOffReason from '../../write_off_reason.mjs';


let elWarehouseAddress = document.getElementById('warehouse_address');
let elReason = document.getElementById('reason');
let elComment = document.getElementById('comment');
let elCreatedAt = document.getElementById('created_at');
let elTgt = document.getElementById('tgt');
let elPrevPg = document.getElementById('prev_pg');
let elPageNumber = document.getElementById('page_number');
let elNextPg = document.getElementById('next_pg');

const pathName = window.location.pathname;
const sepPos = pathName.lastIndexOf('/');
if (sepPos != -1) {
	const writeOffId = parseInt(pathName.substring(sepPos + 1));
	WriteOffs.Get(writeOffId).then(r => {
		elWarehouseAddress.innerHTML = `Склад: ${r['write_off']['warehouse_address']}`;
		elReason.innerHTML = `Причина: ${WriteOffReason.ValueToStr(r['write_off']['reason'])}`;

		if (r['write_off']['comment']) elComment.innerHTML = `Комментарий: ${r['write_off']['comment']}`;
		else elComment.innerHTML = 'Комментарий отсутствует';
		
		elCreatedAt.innerHTML = `Создано: ${DateConv.DateTimeToStr(r['write_off']['created_at'])}`;

		let pagination = new Pagination(
			() => (page) => WriteOffs.GetItemsByWriteOff(writeOffId, page),
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
		
		elPrevPg.addEventListener('click', e => pagination.prev());
		elNextPg.addEventListener('click', e => pagination.next());
	}).catch(e => Status.ShowError(e));
}
