#	Checked source files
+	##	Models
	-	### Db
		|       Model       | Complete |
		| :---------------- | :------: |
		|                   |          |
	-	###	Public
		|       Model       | Complete |
		| :---------------- | :------: |
		| Role              | +        |
		| RolePermission    | +        |
		| EmployeeRole      | +        |
		| Employee          | +        |
		| Permission        | +        |
		| DbUser            | +        |
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
+	##	Services
	|          Service          | Complete |
	| :------------------------ | :------: |
	| BaseService               | +        |
	| EmployeesService          | +        |
	| RolesService              | +        |
	| PermissionsService        | +        |
	| UsersService              | +        |
