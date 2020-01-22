from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QLabel, QLineEdit, QPushButton


class Ui(QtWidgets.QMainWindow):

    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi(r"C:\Users\Asaf\Desktop\expensesCalculator\gui_design.ui", self)
        self._init_widget_objects()
        self.show()

    def _init_widget_objects(self):
        self._init_total_money_text_edit()
        self._init_update_button()

    def _init_update_button(self):
        self.update_button = self._find_widget(QPushButton, 'update_button')
        self.update_button.clicked.connect(self.)

    def _init_total_money_text_edit(self):
        self.total_money = self._find_widget(QLineEdit, 'total_money')

    def _find_widget(self, type, name):
        widget = self.findChild(type, name)
        assert widget is not None, f"Failed to find {name} object!!"
        return widget
