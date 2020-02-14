import sys

from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtWidgets import QLineEdit, QPushButton, QScrollArea, QLabel, QApplication, QWidget, QVBoxLayout, QHBoxLayout

from expenseshandler import ExpensesHandler
from gui.expensesWindow import ExpensesWindow


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.expenses_handler = ExpensesHandler()
        uic.loadUi(r"C:\Users\Asaf\Desktop\expensesCalculator\gui\mainWindow.ui", self)
        self.income_budgets = []
        self._init_widget_objects()

    def _init_widget_objects(self):
        self.central_widget = self.centralWidget()
        self._fill_expenses_container()
        self._init_total_budget_area()

    def _fill_expenses_container(self):
        income_types = self.expenses_handler.get_all_income_types()
        self.expenses_scroll = self._find_widget(QScrollArea, 'scrollArea')
        self.widget = self._find_widget(QWidget, 'scrollAreaWidget')
        self.vbox = QVBoxLayout()

        for income_type in income_types:
            horizontal_layout = QHBoxLayout()
            horizontal_layout.setObjectName(income_type)
            open_button = QPushButton("Open")
            open_button.clicked.connect(self._open_expense_window_by_income_name(income_type))

            horizontal_layout.addWidget(QLabel(income_type))
            horizontal_layout.addWidget(QLabel("Available Budget:"))
            income_type_avlbl_bdgt = ExpensesWindow(self, income_type, self.expenses_handler).get_available_budget()
            self.income_budgets.append(income_type_avlbl_bdgt)
            horizontal_layout.addWidget(QLabel(str(income_type_avlbl_bdgt)))
            horizontal_layout.addWidget(open_button)

            self.vbox.addLayout(horizontal_layout)

        self.widget.setLayout(self.vbox)

        # Scroll Area Properties
        self.expenses_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.expenses_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.expenses_scroll.setWidget(self.widget)

    def _open_expense_window_by_income_name(self, income_name):
        def _open_win():
            app = ExpensesWindow(self, income_name, self.expenses_handler)
            app.setWindowModality(Qt.WindowModal)
            app.show()

        return _open_win

    def _init_total_budget_area(self):
        update_button = self._find_widget(QPushButton, 'update_button')
        total_money_line = self._find_widget(QLineEdit, 'total_money')
        total_money_line.textChanged.connect(self._enable_update_button)
        update_button.clicked.connect(self._update_available_budget)

    def _enable_update_button(self,):
        total_money_line = self._find_widget(QLineEdit, 'total_money')
        enable_button_bool = True if total_money_line.text() else False
        update_button = self._find_widget(QPushButton, 'update_button')
        update_button.setEnabled(enable_button_bool)


    def _update_available_budget(self):
        total_money_value = self._find_widget(QLineEdit, 'total_money').text()
        total_money_label = self._find_widget(QLabel, 'available_budget_label')
        available_budget = str(int(total_money_value) - sum(self.income_budgets))
        total_money_label.setText(available_budget)

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

    main_gui = MainWindow()
    main_gui.show()

    sys.exit(app.exec_())