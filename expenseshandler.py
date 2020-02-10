from  mysql.connector import connect
from consts import TableNames, ColumnNames, IncomeTypes
from dbBackup.dbConnectionData import DB_USER, DB_PASS, DB_NAME

class ExpensesHandler:

	def __init__(self):

		self.connection = connect(user=DB_USER, passwd=DB_PASS,
									  host='localhost', db=DB_NAME)
		self.cursor = self.connection.cursor()

	def get_expense_id_by_name(self, expense_name):
		self.cursor.execute(operation=f"SELECT {ColumnNames.EXPENSE_ID} FROM {TableNames.EXPENSE_DETAILS} WHERE {ColumnNames.EXPENSE_NAME} = '{expense_name}';")
		return self.cursor.fetchall()[0][0]

	def get_income_id_by_name(self, income_name):
		self.cursor.execute(operation=f"SELECT {ColumnNames.INCOME_ID} FROM {TableNames.INCOME_DETAILS} WHERE {ColumnNames.INCOME_NAME} = '{income_name}';")
		return self.cursor.fetchall()[0][0]

	def get_all_incomes_by_income_type(self, income_type):
		self.cursor.execute(operation=f"SELECT "
									  f"incs.{ColumnNames.DATE_STR}, "
									  f"incs.{ColumnNames.AMOUNT}, "
									  f"incs.{ColumnNames.DESCRIPTION} "
									  f"FROM {TableNames.INCOMES} incs "
									  f"INNER JOIN {TableNames.INCOME_DETAILS} inc_dets "
									  f"ON inc_dets.{ColumnNames.INCOME_NAME} = '{income_type}';")

		incomes_dicts = []
		incomes_list = self.cursor.fetchall()

		for inc in incomes_list:
			dict = {}
			dict[ColumnNames.DATE_STR] = inc[0]
			dict[ColumnNames.AMOUNT] = inc[1]
			dict[ColumnNames.DESCRIPTION] = inc[2]

			incomes_dicts.append(dict)

		return incomes_dicts

	def get_all_expenses_by_income_name(self, income_name):
		expense_ids = self._get_all_expenses_ids_matching_income_type(income_name)
		self.cursor.execute(operation=f"SELECT * FROM {TableNames.EXPENSES} "
									  f"WHERE {ColumnNames.EXPENSE_ID} IN ({', '.join(expense_ids)});")

		expenses_dicts = []
		expenses_list = self.cursor.fetchall()

		for exp in expenses_list:
			dict = {}
			dict[ColumnNames.DATE_STR] = exp[0]
			dict[ColumnNames.EXPENSE_ID] = exp[1]
			dict[ColumnNames.PRICE] = exp[2]
			dict[ColumnNames.DESCRIPTION] = exp[3]

			expenses_dicts.append(dict)

		return expenses_dicts

	def get_all_income_types(self):
		self.cursor.execute(operation=f"SELECT {ColumnNames.INCOME_ID}, {ColumnNames.INCOME_NAME} FROM {TableNames.INCOME_DETAILS};")

		types_list = []
		incomes_list = self.cursor.fetchall()

		for exp in incomes_list:
			types_list.append(exp[1])

		return types_list

	def get_all_expense_types(self):
		self.cursor.execute(operation=f"SELECT {ColumnNames.EXPENSE_ID}, {ColumnNames.EXPENSE_NAME} FROM {TableNames.EXPENSE_DETAILS};")

		types_list = []
		expenses_list = self.cursor.fetchall()

		for exp in expenses_list:
			types_list.append(exp[1])

		return types_list

	def _get_all_expenses_ids_matching_income_type(self, income_type):
		self.cursor.execute(operation=f"SELECT "
									  f"exp.{ColumnNames.EXPENSE_ID} "
									  f"FROM {TableNames.EXPENSE_DETAILS} exp "
									  f"INNER JOIN {TableNames.INCOME_DETAILS} inc "
									  f"ON inc.{ColumnNames.INCOME_NAME} = '{income_type}';")

		return list(map(lambda x:str(x[0]), self.cursor.fetchall()))

	def _get_expense_name_by_id(self, id):
		self.cursor.execute(operation=f"SELECT {ColumnNames.EXPENSE_NAME} FROM {TableNames.EXPENSE_DETAILS} "
									  f"WHERE {ColumnNames.EXPENSE_ID} = {id}")
		return self.cursor.fetchall()[0][0]

	def add_expense(self, id, date, price, description=None):
		if not self._does_expense_exist(id=id, date=date, price=price):
			columns_list = [ColumnNames.DATE_STR, ColumnNames.EXPENSE_ID, ColumnNames.PRICE, ColumnNames.DESCRIPTION]
			if description is None:
				description = "NULL"

			columns_str = ", ".join(columns_list)
			self.cursor.execute(operation=f"INSERT INTO {TableNames.EXPENSES} ({columns_str})"
										  f"VALUES ('{date}', {id}, {price}, '{description}');")
			self.connection.commit()
		else:
			raise Exception("Expense already exists!!")

	def _does_expense_exist(self, id, date, price):

		self.cursor.execute(operation=f"SELECT * FROM {TableNames.EXPENSES} "
									  f"WHERE {ColumnNames.EXPENSE_ID}={id} "
									  f"and {ColumnNames.DATE_STR}='{date}'"
									  f"and {ColumnNames.PRICE}={price}")
		return len(self.cursor.fetchall()) > 0


	def add_income(self, id, date, amount, description=None):
		if not self._does_income_exist(id=id, date=date, amount=amount):
			columns_list = [ColumnNames.DATE_STR, ColumnNames.INCOME_ID, ColumnNames.AMOUNT, ColumnNames.DESCRIPTION]
			if description is None:
				description = "NULL"

			columns_str = ", ".join(columns_list)
			self.cursor.execute(operation=f"INSERT INTO {TableNames.INCOMES} ({columns_str})"
										  f"VALUES ('{date}', {id}, {amount}, {description});")
			self.connection.commit()
		else:
			raise Exception("Income already exists!!")

	def _does_income_exist(self, id, date, amount):
		self.cursor.execute(operation=f"SELECT * FROM {TableNames.INCOMES} "
									  f"WHERE {ColumnNames.INCOME_ID}={id} "
									  f"and {ColumnNames.DATE_STR}='{date}'"
									  f"and {ColumnNames.AMOUNT}={amount}")
		return len(self.cursor.fetchall()) > 0

	def __del__(self):
		if hasattr(self, 'connection'):
			if self.connection.is_connected():
				self.connection.close()

if __name__ == "__main__":

	# print(ExpensesHandler().get_all_expenses_from_dad())
	print(ExpensesHandler()._does_expense_exist(id=1, date='7-2-2020', price=3))
	# print(ExpensesHandler().get_all_incomes_by_income_type(IncomeTypes.FROM_DAD))