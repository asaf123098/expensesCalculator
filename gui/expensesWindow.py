from datetime import datetime

from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QVBoxLayout, QTabWidget, QTableWidget, QTableWidgetItem, QHBoxLayout

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
        # self._init_all_incomes_tab(all_incomes)

    # def _init_all_incomes_tab(self, all_incomes):
    #     table = self._set_expenses_table(len(all_incomes))
    #     for row_index, expense in enumerate(all_incomes):
    #         expense_name = self.expenses_handler._get_expense_name_by_id(expense[ColumnNames.EXPENSE_ID])
    #         expense_date = datetime.strptime(expense[ColumnNames.DATE_STR], "%d-%m-%Y")
    #         expense_price = expense[ColumnNames.PRICE]
    #         expense_description = expense[ColumnNames.DESCRIPTION]
    #
    #         table.setItem(row_index, 0, QTableWidgetItem(expense_name))
    #         table.setItem(row_index, 1, QTableWidgetItem(str(expense_date.year)))
    #         table.setItem(row_index, 2, QTableWidgetItem(str(expense_date.month)))
    #         table.setItem(row_index, 3, QTableWidgetItem(str(expense_date.day)))
    #         table.setItem(row_index, 4, QTableWidgetItem(str(expense_price)))
    #         table.setItem(row_index, 5, QTableWidgetItem(expense_description))
    #     layout.addWidget(table, stretch=7)
    #
    #
    #     add_expense_layout = QHBoxLayout()
    #     add_expense_layout.
    #     layout.addWidget(table, stretch=7)
    #     self.tab_widget.addTab(table, "Incomes")


    def _init_all_expenses_tab(self, all_expenses):
        table = self._set_expenses_table(len(all_expenses))
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

    def _set_expenses_table(self, rows_num):
        table = self._find_widget(QTableWidget, "expenses_table")
        table.setRowCount(rows_num)
        table.setColumnCount(6)
        table.setHorizontalHeaderItem(0, QTableWidgetItem("Name"))
        table.setHorizontalHeaderItem(1, QTableWidgetItem("Year"))
        table.setHorizontalHeaderItem(2, QTableWidgetItem("Month"))
        table.setHorizontalHeaderItem(3, QTableWidgetItem("Day"))
        table.setHorizontalHeaderItem(4, QTableWidgetItem("Price"))
        table.setHorizontalHeaderItem(5, QTableWidgetItem("Description"))
        return table

    def _find_widget(self, type, name):
        widget = self.findChild(type, name)
        assert widget is not None, f"Failed to find {name} object!!"
        return widget