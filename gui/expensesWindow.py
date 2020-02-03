from datetime import datetime

from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtWidgets import QLineEdit, QPushButton, QScrollArea, QLabel, QApplication, QWidget, QVBoxLayout, \
    QHBoxLayout, QTabWidget, QTableWidget, QTableWidgetItem

from consts import ColumnNames, IncomeTypes
from expenseshandler import ExpensesHandler


class ExpensesWindow(QtWidgets.QMainWindow):

    def __init__(self, parent, all_expenses, expenses_handler):
        """
        :type expenses_handler ExpensesHandler
        :param parent:
        :param all_expenses:
        :param expenses_handler:
        """
        super(ExpensesWindow, self).__init__(parent)
        uic.loadUi(r"C:\Users\Asaf\Desktop\expensesCalculator\gui\expensesWindow.ui", self)
        self.expenses_handler = expenses_handler
        self._init_all_expenses(all_expenses)

    def _init_all_expenses(self, all_expenses):
        expenses_layout = self._find_widget(QVBoxLayout, 'verticalLayout')
        table = self._get_new_expenses_table(len(all_expenses))
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
            expenses_layout.addWidget(table, 7)

    def _get_new_expenses_table(self, rows_num):
        table = QTableWidget()
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