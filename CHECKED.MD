#	Checked source files
+	##	Models
	-	### Db
		|       Model       | Complete |
		| :---------------- | :------: |
		|  DbUser           | +        |
	-	###	Public
		|       Model               | Complete |
		| :------------------------ | :------: |
		| BaseModel                 | +        |
		| Role                      | +        |
		| RolePermission            | +        |
		| EmployeeRole              | +        |
		| Employee                  | +        |
		| Permission                | +        |
		| Warehouse                 | +        |
		| WarehouseProduct          | +        |
		| Product                   | +        |
		| ProductCategory           | +        |
		| ProductImage              | +        |
		| Supplier                  | +        |
		| Supply                    | +        |
		| SupplyItem                | +        |
		| SupplyStatusHistory       | +        |
		| Order                     | +        |
		| OrderItem                 | +        |
		| OrderStatusHistory        | +        |
		| WriteOff                  | +        |
		| WriteOffItem              | +        |
		| OrderFulfillment          | +        |
		| OrderFulfillmentItem      | +        |
		| OrderPayment              | +        |
		| Cart                      | +        |
		| CartItem                  | +        |
		| ProductReview             | +        |
+	##	Repositories
	-	###	Base
		*	####	Mixins
			|       Mixin       | Complete |
			| :---------------- | :------: |
			| AuditStateMixin   | +        |
			| RelationMixin     | +        |
			| SelectableMixin   | +        |
			| UpdatableMixin    | +        |
	-	###	Public
		|              Repository             | Complete |
		| :---------------------------------- | :------: |
		| EmployeePermissionsRepository       | +        |
		| EmployeeRolesRepository             | +        |
		| EmployeesRepository                 | +        |
		| RolePermissionsRepository           | +        |
		| RolesRepository                     | +        |
		| PermissionsRepository               | +        |
		| UsersRepository                     | +        |
		| WarehousesRepository                | +-       |
		| WarehouseProductsRepository         | +-       |
		| ProductsRepository                  | +        |
		| ProductCategoriesRepository         | +        |
		| ProductImagesRepository             | +        |
		| SuppliersRepository                 | +        |
		| SuppliesRepository                  | +        |
		| SupplyItemsRepository               | +        |
		| SupplyStatusHistoryRepository       | +        |
		| OrdersRepository                    | +        |
		| OrderItemsRepository                | +        |
		| OrderStatusHistoryRepository        | +        |
		| WriteOffsRepository                 | +        |
		| WriteOffItemsRepository             | +        |
		| OrderFulfillmentsRepository         | +        |
		| OrderFulfillmentItemsRepository     | +        |
		| OrderPaymentsRepository             | +        |
		| CartsRepository                     | +        |
		| CartItemsRepository                 | +        |
		| ProductReviewsRepository            | +        |
+	##	Services
	|          Service          | Complete |
	| :------------------------ | :------: |
	| BaseService               | +        |
	| EmployeesService          | +        |
	| RolesService              | +        |
	| PermissionsService        | +        |
	| UsersService              | +        |
	| WarehousesService         | +        |
	| ProductsService           | +        |
	| ProductCategoriesService  | +        |
	| ProductImagesService      | +        |
	| SuppliersService          | +        |
	| SuppliesService           | +        |
	| OrdersService             | +        |
	| WriteOffsService          | +        |
	| OrderFulfillmentsService  | +        |
	| OrderPaymentsService      | +        |
	| CartsService              | +        |
	| ProductReviewsService     | +        |
