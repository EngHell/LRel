import sys

from PyQt5.QtWidgets import QApplication, QLabel, QWidget


# This is a sample Python script.

# Press Mayús+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from ui.mainwindow import MainWindow
from ui.widgetexample import MainWidget


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app = QApplication(sys.argv)

    w = MainWindow()
    w.show()

    sys.exit(app.exec())

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
