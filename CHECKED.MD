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
	| SupplyItemsService        | +        |
