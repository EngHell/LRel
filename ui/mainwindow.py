from pathlib import Path

from PyQt5 import QtGui
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QAction, qApp, QMenu, QFileDialog, QVBoxLayout, QPushButton

from LRel.LRel import LRel
from .analyze_dialog import AnalyzeDialog
from .analyze_dialog_ui import Ui_Dialog
from .main_window_ui import Ui_MainWindow


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.connect_signals_slots()

        self.lrel = LRel()

    def connect_signals_slots(self):
        self.ui.actionExit.triggered.connect(self.close)
        self.ui.actionOpen.triggered.connect(self.show_open_dialog)
        self.ui.pushButton_analize.clicked.connect(self.analyze_action)
        self.ui.pushButton_preProcessImages.clicked.connect(self.preprocess_images_action)

    def show_open_dialog(self):
        home_dir = str(Path.home())
        directory = QFileDialog.getExistingDirectory(
            self,
            "Select the project folder",
            home_dir
        )

        if directory:
            self.lrel.open_directories(directory)
            self.ui.lineEdit_workingDir.setText(self.lrel.working_dir)
            self.ui.lineEdit_trainingDir.setText(self.lrel.training_dir)
            self.ui.lineEdit_validationDir.setText(self.lrel.validation_dir)
            self.statusBar().showMessage(f"Opened directory:{directory}")
            self.ui.pushButton_analize.setEnabled(True)

    def analyze_action(self):
        self.statusBar().showMessage("started")
        dialog = AnalyzeDialog(self.lrel, self)
        dialog.accepted.connect(self.accepted_analyze_dialog)
        dialog.rejected.connect(self.rejected_analyze_dialog)
        dialog.exec()

        self.ui.lineEdit_mValidation.setText(self.lrel.validation_count.__str__())
        self.ui.lineEdit_mTraining.setText(self.lrel.training_count.__str__())

    def accepted_analyze_dialog(self):
        self.statusBar().showMessage("finished analysis")
        self.ui.pushButton_preProcessImages.setEnabled(True)

    def rejected_analyze_dialog(self):
        self.statusBar().showMessage("canceled analysis")

    def preprocess_images_action(self):
        self.lrel.preprocess_images(64)



