from sys import exit
import json

from PySide2.QtWidgets import QCheckBox, QTableWidgetItem, QApplication, QMainWindow, QHeaderView

from main_ui import Ui_MainWindow

DATA_FILE = "questions.json"

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("Quiz Us!")

        self.ui.tableWidget.setColumnCount(4)
        self.ui.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        questions: dict = json.load(open(DATA_FILE, "r"))
        headers = ["Lock", "Question", "Answer", "Category", "Set", "No."]

        self.add_items_to_list(questions)

        for x in range(0, self.ui.tableWidget.columnCount()):
            try:
                self.ui.tableWidget.setHorizontalHeaderItem(x, QTableWidgetItem(headers[x]))
            except IndexError:  # not given all of the headers, just se the defaults for the others, which are from 1-length
                continue

    def add_item_to_list(self, question, answer, category, set_num, num, col):
        self.ui.tableWidget.setCellWidget(col, 0, QCheckBox()) # add check box
        
        rows = list(map(QTableWidgetItem, map(str, [question, answer, category.replace("_", " ").title(), set_num, num])))
        self.ui.tableWidget.setColumnCount(len(rows)+1)
        for row, widget in enumerate(rows):
            self.ui.tableWidget.setItem(col, row+1, widget)

    def add_items_to_list(self, items):
        self.ui.tableWidget.setRowCount(len(items))

        for col, item in enumerate(items):
            self.add_item_to_list(*item, col)

if __name__ == "__main__":
    app = QApplication([])

    window = MainWindow()
    window.show()

    exit(app.exec_())