from  mysql.connector import connect
from consts import TableNames, ColumnNames, IncomeTypes
from dbConnectionData import DB_USER, DB_PASS, DB_NAME

class ExpensesHandler:

	def __init__(self):

		self.connection = connect(user=DB_USER, passwd=DB_PASS,
									  host='localhost', db=DB_NAME)
		self.cursor = self.connection.cursor()

	def get_all_incomes_by_income_name(self, income_name):
		ids = self._get_all_ids_matching_income_type(income_name)
		self.cursor.execute(operation=f"SELECT * FROM {TableNames.INCOMES} "
									  f"WHERE {ColumnNames.INCOME_ID} IN ({', '.join(ids)});")

		incomes_dicts = []
		incomes_list = self.cursor.fetchall()

		for inc in incomes_list:
			dict = {}
			dict[ColumnNames.DATE_STR] = inc[0]
			dict[ColumnNames.EXPENSE_ID] = inc[1]
			dict[ColumnNames.PRICE] = inc[2]
			dict[ColumnNames.DESCRIPTION] = inc[3]

			incomes_dicts.append(dict)

		return incomes_dicts

	def get_all_expenses_by_income_name(self, income_name):
		expense_ids = self._get_all_ids_matching_income_type(income_name)
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

		incomes_dicts = []
		incomes_list = self.cursor.fetchall()

		for exp in incomes_list:
			dict = {}
			dict[ColumnNames.INCOME_ID] = exp[0]
			dict[ColumnNames.INCOME_NAME] = exp[1]
			incomes_dicts.append(dict)

		return incomes_dicts

	def _get_all_ids_matching_income_type(self, income_type):
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
										  f"VALUES ('{date}', {id}, {price}, {description});")
			self.connection.commit()
		else:
			raise Exception("Expense already exists!!")

	def _does_expense_exist(self, id, date, price):

		self.cursor.execute(operation=f"SELECT * FROM {TableNames.EXPENSES} "
									  f"WHERE {ColumnNames.EXPENSE_ID}={id} "
									  f"and {ColumnNames.DATE_STR}='{date}'"
									  f"and {ColumnNames.PRICE}={price}")
		return len(self.cursor.fetchall()) > 0

	def __del__(self):
		if hasattr(self, 'connection'):
			if self.connection.is_connected():
				self.connection.close()

if __name__ == "__main__":

	# print(ExpensesHandler().get_all_expenses_from_dad())
	print(ExpensesHandler().get_all_income_types())