from bs4 import BeautifulSoup

from xmlAttrsConsts import ExpenseAttrs, DateAttrs


class ExpensesHandler:

	def __init__(self, expenses_file_path):
		self.expenses_file_path = expenses_file_path
		with open(self.expenses_file_path, 'r') as xml_file:
			self.soup = BeautifulSoup(xml_file, features='xml')

	def add_expense_to_month(self, month, year, expense_type, expense_value, day=None, expense_description=None):
		if self._get_expense_tag(month=month, year=year, expense_type=expense_type,
								 expense_value=expense_value, day=day, expense_description=expense_description, raise_exception=False):
			raise Exception("This expense already exists in the xml")

		month_tag = self._get_month_tag(month=month, year=year)

		expense_attrs_list = {ExpenseAttrs.TYPE: expense_type, ExpenseAttrs.VALUE: expense_value}
		if expense_description is not None:
			expense_attrs_list[ExpenseAttrs.DESCRIPTION] = expense_description
		if day is not None:
			expense_attrs_list[ExpenseAttrs.DAY] = day

		expense_tag = self.soup.new_tag(name=ExpenseAttrs.EXPENSE, attrs=expense_attrs_list)
		month_tag.append(expense_tag)
		self._update_xml()

	def _get_expense_tag(self, month, year, expense_type, expense_value, day=None, expense_description=None, raise_exception=True):
		expense_attrs_list = {ExpenseAttrs.TYPE: expense_type, ExpenseAttrs.VALUE: expense_value}
		if expense_description is not None:
			expense_attrs_list[ExpenseAttrs.DESCRIPTION] = expense_description
		if day is not None:
			expense_attrs_list[ExpenseAttrs.DAY] = day

		all_expenses = self.soup.find_all(ExpenseAttrs.EXPENSE, attrs=expense_attrs_list)
		for expense in all_expenses:

			# Check month and year are the same
			expense_month = expense.find_parent()
			expense_year = expense_month.find_parent()

			if expense_month[DateAttrs.NUM] == str(month) and expense_year[DateAttrs.NUM] == str(year):
				return expense

		if raise_exception:
			raise Exception("Expense doesn't exist!!")

	def _get_month_tag(self, month, year):
		all_months = self.soup.find_all(DateAttrs.MONTH, attrs={DateAttrs.NUM: month})
		for month in all_months:
			if month.find_parent()[DateAttrs.NUM] == str(year):
				return month
		raise Exception("Month doesn't exist in the xml!! (%i.%i)" % (month, year))

	def _get_year_tag(self, year):
		all_years = self.soup.find_all(DateAttrs.YEAR, attrs={DateAttrs.NUM: year})
		for year_tag in all_years:
			if year_tag[DateAttrs.NUM] == str(year):
				return year_tag
		raise Exception("Year doesn't exist in the xml!! (%i)" % year)

	def _add_year(self, year):
		new_year = self.soup.new_tag(name=DateAttrs.YEAR, attrs={DateAttrs.NUM: year})
		self.soup.append(new_year)
		self._update_xml()

	def _add_month_to_year(self, month, year):
		year_tag = self._get_year_tag(year)
		new_month = self.soup.new_tag(name=DateAttrs.MONTH, attrs={DateAttrs.NUM: month})
		year_tag.append(new_month)
		self._update_xml()

	def _update_xml(self):
		with open(self.expenses_file_path, 'w') as xml_file:
			xml_file.write(self.soup.prettify())

if __name__ == "__main__":
	check = ExpensesHandler("expenses.xml")
	check.add_expense_to_month(day=12, month=1, year=2020, expense_type="passport_renew", expense_value=75)

