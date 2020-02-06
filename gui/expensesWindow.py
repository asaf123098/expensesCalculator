from datetime import datetime

from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QVBoxLayout, QTabWidget, QTableWidget, QTableWidgetItem, QHBoxLayout, QComboBox, \
    QPushButton, QDialogButtonBox

from consts import ColumnNames
from expenseshandler import ExpensesHandler


class ExpensesWindow(QtWidgets.QMainWindow):

    def __init__(self, parent, all_expenses, all_incomes, expenses_handler):
        """
        :type expenses_handler ExpensesHandler
        :param parent:
        :param all_expenses:
        :param expenses_handler:
        """
        super(ExpensesWindow, self).__init__(parent)
        uic.loadUi(r"C:\Users\Asaf\Desktop\expensesCalculator\gui\expensesWindow.ui", self)
        self.expenses_handler = expenses_handler
        self.main_layout = self._find_widget(QVBoxLayout, 'verticalLayout')

        self._init_all_expenses_tab(all_expenses)
        self._init_all_incomes_tab(all_incomes)
        self._init_add_expense_area()

    def _init_all_expenses_tab(self, all_expenses):
        self._set_expenses_table(all_expenses)
        self._set_expense_types_combo()

    def _set_expenses_table(self, all_expenses):
        table = self._find_widget(QTableWidget, "expenses_table")
        table.setRowCount(len(all_expenses))
        table.setColumnCount(6)
        table.setHorizontalHeaderItem(0, QTableWidgetItem("Name"))
        table.setHorizontalHeaderItem(1, QTableWidgetItem("Year"))
        table.setHorizontalHeaderItem(2, QTableWidgetItem("Month"))
        table.setHorizontalHeaderItem(3, QTableWidgetItem("Day"))
        table.setHorizontalHeaderItem(4, QTableWidgetItem("Price"))
        table.setHorizontalHeaderItem(5, QTableWidgetItem("Description"))

        for row_index, expense in enumerate(all_expenses):
            expense_name = self.expenses_handler._get_expense_name_by_id(expense[ColumnNames.EXPENSE_ID])
            expense_date = datetime.strptime(expense[ColumnNames.DATE_STR], "%d-%m-%Y")
            expense_price = expense[ColumnNames.PRICE]
            expense_description = expense[ColumnNames.DESCRIPTION]

            table.setItem(row_index, 0, QTableWidgetItem(expense_name))
            table.setItem(row_index, 1, QTableWidgetItem(str(expense_date.year)))
            table.setItem(row_index, 2, QTableWidgetItem(str(expense_date.month)))
            table.setItem(row_index, 3, QTableWidgetItem(str(expense_date.day)))
            table.setItem(row_index, 4, QTableWidgetItem(str(expense_price)))
            table.setItem(row_index, 5, QTableWidgetItem(expense_description))

    def _set_expense_types_combo(self):
        all_types = self.expenses_handler.get_all_expense_types()
        combo_box = self._find_widget(QComboBox, "new_expense_type_combo")
        combo_box.addItems(all_types)

    def _init_all_incomes_tab(self, all_incomes):
        self._set_incomes_table(all_incomes)

    def _set_incomes_table(self, all_incomes):
        table = self._find_widget(QTableWidget, "incomes_table")
        table.setRowCount(len(all_incomes))
        table.setColumnCount(5)
        table.setHorizontalHeaderItem(0, QTableWidgetItem("Year"))
        table.setHorizontalHeaderItem(1, QTableWidgetItem("Month"))
        table.setHorizontalHeaderItem(2, QTableWidgetItem("Day"))
        table.setHorizontalHeaderItem(3, QTableWidgetItem("Amount"))
        table.setHorizontalHeaderItem(4, QTableWidgetItem("Description"))

        for row_index, expense in enumerate(all_incomes):
            income_date = datetime.strptime(expense[ColumnNames.DATE_STR], "%d-%m-%Y")
            income_amount = expense[ColumnNames.AMOUNT]
            income_description = expense[ColumnNames.DESCRIPTION]

            table.setItem(row_index, 0, QTableWidgetItem(str(income_date.year)))
            table.setItem(row_index, 1, QTableWidgetItem(str(income_date.month)))
            table.setItem(row_index, 2, QTableWidgetItem(str(income_date.day)))
            table.setItem(row_index, 3, QTableWidgetItem(str(income_amount)))
            table.setItem(row_index, 4, QTableWidgetItem(income_description))

    def _init_add_expense_area(self):

        box_buttons = self._find_widget(QDialogButtonBox, 'new_expense_dialog_box')
        box_buttons.addButton("Apply", QDialogButtonBox.AcceptRole)
        box_buttons.addButton("Reset", QDialogButtonBox.RejectRole)
        box_buttons.accepted.connect(self._add_new_expesnse)
        box_buttons.rejected.connect(self._reset_new_expense_area)

    def _add_new_expesnse(self):
        pass
        # self.expenses_handler.add_expense(id=, date=, price=)

    def _reset_new_expense_area(self):
        print ("Reset clicked")

    def _find_widget(self, type, name):
        widget = self.findChild(type, name)
        assert widget is not None, f"Failed to find {name} object!!"
        return widget