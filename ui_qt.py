#!/usr/bin/env python3
import sys
import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg
import PyQt5.QtCore as qtc
import main

# I'm learning qt as I go.

class main_window(qtw.QWidget):
    def __init__(self):

        # init
        super().__init__()
        self.setWindowTitle("HomePy QtUI")
        self.setLayout(qtw.QGridLayout())

        # Build main menu
        self.input_btn = qtw.QPushButton("Daily Input", self)
        self.input_btn.clicked.connect(self.open_daily_input)
        self.layout().addWidget(self.input_btn, 1, 1, 2, 2)

        self.show()

    def open_daily_input(self):
        self.daily_window = daily_input()

class daily_input(qtw.QWidget):
    def __init__(self):

        # init
        super().__init__()
        self.setWindowTitle("Daily Input")
        self.setLayout(qtw.QFormLayout())

        # Prompt user for info
        self.dateField = qtw.QDateEdit()
        self.layout().addRow("Input date: ", self.dateField)

        self.notesField = qtw.QTextEdit()
        self.layout().addRow("Notes: ", self.notesField)

        self.finalizeBtn = qtw.QPushButton("Finalize")
        self.finalizeBtn.clicked.connect(lambda: print("Oof."))
        self.layout().addRow(self.finalizeBtn)

        self.show()

if __name__ == "__main__":
    main_app = qtw.QApplication(sys.argv)
    mainw = main_window()
    sys.exit(main_app.exec())
