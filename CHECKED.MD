#	Checked source files
+	##	Models
	-	### Db
		|       Model       | Complete |
		| :---------------- | :------: |
		|  DbUser           | +        |
	-	###	Public
		|       Model               | Complete |
		| :------------------------ | :------: |
		| Role                      | +        |
		| RolePermission            | +        |
		| EmployeeRole              | +        |
		| Employee                  | +        |
		| Permission                | +        |
		| Warehouse                 | ?        |
		| WarehouseProduct          | ?        |
+	##	Repositories
	-	###	Base
		*	####	Mixins
			|       Mixin       | Complete |
			| :---------------- | :------: |
			| AuditStateMixin   | +        |
			| AssignableMixin   | +        |
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
+	##	Services
	|          Service          | Complete |
	| :------------------------ | :------: |
	| BaseService               | +        |
	| EmployeesService          | +        |
	| RolesService              | +        |
	| PermissionsService        | +        |
	| UsersService              | +        |
	| WarehousesService         | +        |
