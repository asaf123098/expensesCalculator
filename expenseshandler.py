from simplemysql import SimpleMysql

from consts import TableNames, ColumnNames, ExpenseTypes


class ExpensesHandler:

	def __init__(self):
		self.connection = SimpleMysql(user='root', passwd='089704427.Tavor',
									  host='localhost', db='financials')


	def add_expense(self):
		pass

	def _does_expense_exist(self, id, date):
		return self.connection.getOne(table=TableNames.EXPENSES,
									  where=(f"{ColumnNames.EXPENSE_ID}={id} and {ColumnNames.DATE_STR}={date}"))

	def __del__(self):
		if hasattr(self, 'connection'):
			self.connection.end()


if __name__ == "__main__":

	print(ExpensesHandler()._does_expense_exist(ExpenseTypes.SHOES, "27-09-2019"))