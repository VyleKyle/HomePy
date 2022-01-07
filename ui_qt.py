#!usr/bin/env python3
import sys
import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg
import PyQt5.QtCore as qtc
import main
import logging
import datetime

logger = logging.getLogger("qtui")
logger.info("Using QT UI")

winStyle = "background-color: " + main.config["WINDOW_BG"]
textStyle = "background-color: " + main.config["UI_BG"]

class main_window(qtw.QWidget):
    def __init__(self):

        # config
        super().__init__()
        self.setWindowTitle("HomePy QtUI")
        self.setStyleSheet(winStyle)
        self.setLayout(qtw.QGridLayout())

        # Build main menu
        # 1. Daily input
        self.inputBtn = qtw.QPushButton("Daily Input", self)
        self.inputBtn.clicked.connect(self.open_daily_input)
        self.layout().addWidget(self.inputBtn, 1, 1, 2, 2)

        # 2. View data
        self.viewBtn = qtw.QPushButton("View", self)
        self.viewBtn.clicked.connect(self.open_view_data)
        self.layout().addWidget(self.viewBtn, 3, 1, 2, 2,)

        # 3. Close program
        self.closeBtn = qtw.QPushButton("Close", self)
        self.closeBtn.clicked.connect(self.close)
        self.layout().addWidget(self.closeBtn, 5, 1, 2, 2)

        self.show()

    def open_daily_input(self):
        self.daily_window = daily_input()

    def open_view_data(self):
        self.data_window = view_data()

class daily_input(qtw.QWidget):
    def __init__(self):

        # init
        super().__init__()
        self.setWindowTitle("Daily Input")
        self.setStyleSheet(winStyle)
        self.mainLayout = qtw.QVBoxLayout()
        self.setLayout(self.mainLayout)

        # Check for existing data
        try:
            today = datetime.datetime.now()
            today_str = today.strftime("%Y/%m/%d")

            data = main.loadData([today_str])[0]

        except ValueError as err:
            data = None
            logger.info("Couldn't load daily data")

        # Date
        self.dateLayout = qtw.QHBoxLayout()

        self.dateLabel = qtw.QLabel("Date: ")
        self.dateLabel.setStyleSheet(textStyle)
        self.dateLayout.addWidget(self.dateLabel)

        self.dateField = qtw.QDateEdit()
        self.dateField.setStyleSheet(textStyle)
        self.dateField.setDisplayFormat("yyyy/MM/dd")
        self.dateLayout.addWidget(self.dateField)

        self.mainLayout.addLayout(self.dateLayout)

        # Dues
        self.dueList = qtw.QHBoxLayout()
        self.mainLayout.addLayout(self.dueList)

        self.dueAddBtn = qtw.QPushButton("Another due", self)
        self.dueAddBtn.clicked.connect(self.addDue)
        self.mainLayout.addWidget(self.dueAddBtn)

        # Notes
        self.notesLayout = qtw.QHBoxLayout()

        self.notesLabel = qtw.QLabel()
        self.notesLabel.setStyleSheet(textStyle)
        self.notesLayout.addWidget(self.notesLabel)

        self.notesField = qtw.QTextEdit()
        self.notesField.setStyleSheet(textStyle)
        self.notesLayout.addWidget(self.notesField)

        self.mainLayout.addLayout(self.notesLayout)

        # Fill in applicable data
        if data is not None:

            # Date
            self.dateField.setDate(qtc.QDate(
            data.date.year,
            data.date.month,
            data.date.day))

            # Dues
            for due in data.dues:
                logger.debug(due.__dict__)
                # Build a form to fill out
                task, points, completion = self.addDue()

                task.setText(due.task)

                points.setValue(due.points)

                completion.setValue(due.completion)

            self.notesField.setText("\n".join(data.notes))

        # Final user options
        self.finalLayout = qtw.QHBoxLayout()

        # 1. Ship off data
        self.finalizeBtn = qtw.QPushButton("Finalize")
        self.finalizeBtn.clicked.connect(self.finalize)
        self.finalLayout.addWidget(self.finalizeBtn)

        # 2. Nah dog we done here
        self.closeBtn = qtw.QPushButton("Close")
        self.closeBtn.clicked.connect(self.close)
        self.finalLayout.addWidget(self.closeBtn)

        self.mainLayout.addLayout(self.finalLayout)

        self.show()

    def addDue(self, data=None):
        # Required info:
        # Task; str
        # Points; int
        # Completion; float
        #
        # Return tuple of relevant references
        # (LineEdit: task, SpinBox:  points, DoubleSpinBox: completion)

        w_container = qtw.QWidget()
        container = qtw.QFormLayout()
        w_container.setLayout(container)

        task = qtw.QLineEdit()
        container.addRow("Task: ", task)

        points = qtw.QSpinBox()
        container.addRow("Points: ", points)

        completion = qtw.QDoubleSpinBox()
        completion.setMaximum(1.0)
        completion.setMinimum(0.0)
        container.addRow("Completion: ", completion)

        removeDue = qtw.QPushButton("Remove")
        removeDue.clicked.connect(w_container.close)
        container.addRow(removeDue)

        w_container.show()
        self.dueList.addWidget(w_container)

        return task, points, completion

    def finalize(self):

        # Format dues


        output = main.Day(
        date=self.dateField.date().toString("%Y/%m/%d"),
        dues=[],
        notes=self.notesField.toPlainText()
        )

class view_data(qtw.QWidget):
    def __init__(self, data=None):
        super().__init__()

        # Window config
        self.setWindowTitle("View data")
        self.setStyleSheet(winStyle)
        self.setLayout(qtw.QVBoxLayout())

        if data is None or not isinstance(data, list):
            data = ["2021/12/30"]

        self.data = main.loadData(data)

        logger.info("Data loaded")
        logger.debug(self.data)

        self.show()

if __name__ == "__main__":
    main_app = qtw.QApplication(sys.argv)
    mainw = main_window()
    sys.exit(main_app.exec())
