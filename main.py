import json
from base64 import b64encode, b64decode

from sys import exit

from PySide2.QtWidgets import QCheckBox, QTableWidgetItem, QApplication, QMainWindow, QHeaderView
from PySide2.QtCore import Qt

from main_ui import Ui_MainWindow
from QuestionDao import QuestionDao, DB_FILE

questions_dao = QuestionDao(DB_FILE)

ENCODE_SAVE = True # if to b64 encode saved question lists

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("Quiz It!")

        self.ui.tableWidget.setColumnCount(4)
        self.ui.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.headers = ["Lock", "Question", "Answer", "Category", "No.", "ID"]

        self.ui.tableWidget.setColumnCount(len(self.headers))

        self.ui.tableWidget.hideColumn(self.ui.tableWidget.columnCount() - 1)  # hide last column, as this is where its id is stored

        self.ui.comboBox.addItems(questions_dao.get_categories())

        self.set_headers()

        self.ui.pushButton.clicked.connect(self.refresh_button)
        self.ui.saveButton.clicked.connect(self.save_button)
        self.ui.openButton.clicked.connect(self.open_button)

    def set_headers(self):
        for x in range(len(self.headers)):
            try:
                self.ui.tableWidget.setHorizontalHeaderItem(x, QTableWidgetItem(self.headers[x]))
            except IndexError:  # not given all of the headers, just se the defaults for the others, which are from 1-length
                continue

    def save_button(self):
        save_name = "list1"
        to_save = []
        for col in range(self.ui.tableWidget.rowCount()):
            id = int(self.ui.tableWidget.item(col, self.ui.tableWidget.columnCount()-1).text())
            to_save.append(id)

        with open("{}.quiz".format(save_name), "w") as f:
            data = json.dumps(to_save)
            if ENCODE_SAVE:
                data = b64encode(data.encode()).decode()
            f.write(data)

    def open_button(self):
        #todo validate file name
        name = "list1.quiz"

        with open(name, "r") as f:
            data = f.read()

        try:
            data = b64decode(data.encode()).decode()
        except:
            pass

        data = json.loads(data)

        questions = questions_dao.get_items(data)

        self.add_items_to_list(questions)

    def refresh_button(self):
        category = self.ui.comboBox.currentText()
        number_to_get = self.ui.spinBox.value()

        locked = []
        for col in range(self.ui.tableWidget.rowCount()):
            box: QCheckBox = self.ui.tableWidget.cellWidget(col, 0)
            if box.checkState() == Qt.CheckState.Checked:
                locked.append(int(self.ui.tableWidget.item(col, self.ui.tableWidget.columnCount() - 1).text())) # append the last value (ID) of the table, but turn it to int as it is always str

        for id, item in enumerate(locked):
            locked[id] = questions_dao.get_item(item)

        items = questions_dao.get_n_category(category, number_to_get-len(locked)) # get n items, without those checked included in the number
        if locked:
            items += locked

        self.add_items_to_list(items, locked)

    def add_item_to_list(self, id, question, answer, category, num, col, box):
        if not box: box = QCheckBox()
        self.ui.tableWidget.setCellWidget(col, 0, box) # add check box

        rows = list(map(QTableWidgetItem, map(str, [question, answer, category, num, id])))
        for row, widget in enumerate(rows):
            self.ui.tableWidget.setItem(col, row+1, widget)

    def add_items_to_list(self, items, locked=[]):
        self.ui.tableWidget.setRowCount(len(items))
        self.ui.tableWidget.clear()
        self.set_headers()

        for col, item in enumerate(items):
            box = None
            if item in locked:
                box = QCheckBox()
                box.setChecked(True)
            self.add_item_to_list(item[0], item[1], item[2], item[4], item[5], col, box)

if __name__ == "__main__":
    app = QApplication([])

    window = MainWindow()
    window.show()

    exit(app.exec_())