from PyQt5 import QtGui
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import QWidget, QToolTip, QPushButton, QApplication, QMessageBox, QDesktopWidget


class MainWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        QToolTip.setFont(QFont("SansSerif",10))

        self.setToolTip("This is a <b>QWidget</b> widget")

        btn = QPushButton("Quit", self)
        btn.clicked.connect(self.close)
        btn.setToolTip("This <b>closes</b> the window")
        btn.resize(btn.sizeHint())
        btn.move(50, 50)

        self.setGeometry(300, 300, 300, 220)
        self.center()
        self.setWindowTitle("LReg IClassifier")
        self.setWindowIcon(QIcon("windowicon.png"))

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        reply = QMessageBox.question(
            self,
            "Message",
            "Are you sure to quit?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            a0.accept()
        else:
            a0.ignore()
