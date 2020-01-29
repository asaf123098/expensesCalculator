import sys

from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import Qt, QLine
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtWidgets import QLineEdit, QPushButton, QScrollArea, QLabel, QApplication, QWidget, QVBoxLayout, QHBoxLayout

from consts import ColumnNames, IncomeTypes
from expenseshandler import ExpensesHandler


class ExpensesGui(QtWidgets.QMainWindow):

    def __init__(self, parent, all_expenses):
        super(ExpensesGui, self).__init__(parent)
        uic.loadUi(r"C:\Users\Asaf\Desktop\expensesCalculator\gui\expensesGui.ui", self)
        # self._init_all_expenses(all_expenses)

    def _init_all_expenses(self, all_expenses):
        self.expenses_scroll = self._find_widget(QScrollArea, 'scrollAreaWidgetContents_2')
        self.widget = QWidget()  # Widget that contains the collection of Vertical Box
        self.vbox = QVBoxLayout()

        for expense in all_expenses:
            # income_name = income[ColumnNames.INCOME_NAME]
            horizontal_layout = QHBoxLayout()
            # horizontal_layout.setObjectName(income_name)
            label = QLabel(expense)
            horizontal_layout.addWidget(label)

            self.vbox.addLayout(horizontal_layout)

        self.widget.setLayout(self.vbox)

    def _find_widget(self, type, name):
        widget = self.findChild(type, name)
        assert widget is not None, f"Failed to find {name} object!!"
        return widget