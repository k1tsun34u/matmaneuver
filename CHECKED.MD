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
+	##	Repositories
	-	###	Base
		*	####	Mixins
			|       Mixin       | Complete |
			| :---------------- | :------: |
			| AuditStateMixin   | +        |
			| UpdatableMixin    | +        |
			| SelectableMixin   | +        |
	-	###	Public
		|              Repository             | Complete |
		| :---------------------------------- | :------: |
		| EmployeePermissionsRepository       | +        |
		| EmployeeRolesRepository             | +        |
		| EmployeesRepository                 | +        |
+	##	Services
	|          Service          | Complete |
	| :------------------------ | :------: |
	| BaseService               | +        |
	| EmployeesService          | +        |