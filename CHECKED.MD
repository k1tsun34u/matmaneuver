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
