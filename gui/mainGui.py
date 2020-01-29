import sys

from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtWidgets import QLineEdit, QPushButton, QScrollArea, QLabel, QApplication, QWidget, QVBoxLayout, QHBoxLayout

from consts import ColumnNames
from expenseshandler import ExpensesHandler
from gui.expnsesGui import ExpensesGui


class MainGui(QtWidgets.QMainWindow):

    def __init__(self):
        super(MainGui, self).__init__()
        self.expenses_handler = ExpensesHandler()
        uic.loadUi(r"C:\Users\Asaf\Desktop\expensesCalculator\gui\mainGui.ui", self)
        self._init_widget_objects()

    def _init_widget_objects(self):
        self.central_widget = self.centralWidget()
        self._init_total_money_text_edit()
        self._init_update_button()
        self._fill_expenses_container()

    def _fill_expenses_container(self):
        income_types = self.expenses_handler.get_all_income_types()
        self.expenses_scroll = self._find_widget(QScrollArea, 'scrollArea')
        self.widget = self._find_widget(QWidget, 'scrollAreaWidget')
        self.vbox = QVBoxLayout()

        for income in income_types:
            income_name = income[ColumnNames.INCOME_NAME]
            horizontal_layout = QHBoxLayout()
            horizontal_layout.setObjectName(income_name)
            label = QLabel(income_name)
            open_button = QPushButton("Open")
            open_button.clicked.connect(self._open_expense_window_by_income_name(income_name))
            horizontal_layout.addWidget(label)
            horizontal_layout.addWidget(open_button)

            self.vbox.addLayout(horizontal_layout)

        self.widget.setLayout(self.vbox)

        # Scroll Area Properties
        self.expenses_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.expenses_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.expenses_scroll.setWidget(self.widget)

    def _open_expense_window_by_income_name(self, income_name):
        def _open_win():
            all_expenses = self.expenses_handler.get_all_expenses_by_income_name(income_name)
            app = ExpensesGui(self, all_expenses)
            app.show()

        return _open_win

    def _init_update_button(self):
        self.update_button = self._find_widget(QPushButton, 'update_button')
        self.update_button.clicked.connect(self._update_total_money)

    def _update_total_money(self):
        pass

    def _init_total_money_text_edit(self):
        self.total_money = self._find_widget(QLineEdit, 'total_money')

    def _find_widget(self, type, name):
        widget = self.findChild(type, name)
        assert widget is not None, f"Failed to find {name} object!!"
        return widget

def _set_theme_darcula(app):
    dark_palette = QPalette()
    dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.WindowText, Qt.white)
    dark_palette.setColor(QPalette.Base, QColor(25, 25, 25))
    dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ToolTipBase, Qt.white)
    dark_palette.setColor(QPalette.ToolTipText, Qt.white)
    dark_palette.setColor(QPalette.Text, Qt.white)
    dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ButtonText, Qt.white)
    dark_palette.setColor(QPalette.BrightText, Qt.red)
    dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.HighlightedText, Qt.black)
    app.setPalette(dark_palette)
    app.setStyleSheet("QToolTip { "
                           "color: #ffffff; "
                           "background-color: #2a82da; "
                           "border: 1px solid white; }")

if __name__ == "__main__":

    app = QApplication([])
    # _set_theme_darcula(app)

    main_gui = MainGui()
    main_gui.show()

    sys.exit(app.exec_())