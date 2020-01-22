from  mysql.connector import connect
from consts import TableNames, ColumnNames, Values
from dbConnectionData import DB_USER, DB_PASS, DB_NAME

class ExpensesHandler:

	def __init__(self):

		self.connection = connect(user=DB_USER, passwd=DB_PASS,
									  host='localhost', db=DB_NAME)
		self.cursor = self.connection.cursor()

	def get_all_expenses_from_dad(self):
		expense_ids = self._get_all_expense_ids_matching_income_type(Values.FROM_DAD)
		self.cursor.execute(operation=f"SELECT * FROM {TableNames.EXPENSES} "
									  f"WHERE {ColumnNames.EXPENSE_ID} IN ({', '.join(expense_ids)});")
		return self.cursor.fetchall()

	def _get_all_expense_ids_matching_income_type(self, income_type):
		self.cursor.execute(operation=f"SELECT "
									  f"exp.{ColumnNames.EXPENSE_ID} "
									  f"FROM {TableNames.EXPENSE_DETAILS} exp "
									  f"INNER JOIN {TableNames.INCOME_DETAILS} inc "
									  f"ON inc.{ColumnNames.INCOME_NAME} = '{income_type}';")

		return list(map(lambda x:str(x[0]), self.cursor.fetchall()))

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
			self.connection.close()
		if hasattr(self, 'cursor'):
			self.cursor.close()


if __name__ == "__main__":

	print(ExpensesHandler().get_all_expenses_from_dad())