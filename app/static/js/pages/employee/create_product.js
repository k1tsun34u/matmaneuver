import Status from '../../status.mjs';
import Products from '../../api/employee/products.mjs';
import ProductCategories from '../../api/employee/product_categories.mjs';
import ProductImages from '../../api/employee/product_images.mjs';


let elName = document.getElementById('name');
let elDescription = document.getElementById('description');
let elPrice = document.getElementById('price');
let elCreate = document.getElementById('create');
let elAddImage = document.getElementById('add_image');

elCreate.addEventListener('click', e => {
	Products.Create(elName.value, elPrice.value, elDescription.value).then(response => {
		ProductImages.CreateMany(response['product_id'], [elAddImage.files[0]]).then(result => {
			window.location.href = '/employee/products';
		}).catch(error => {
			Products.Delete(response['product_id']);
			Status.ShowError(error);
		});
	}).catch(error => {
		Status.ShowError(error);
		window.location.href = '/login';
	});
});
