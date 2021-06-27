from __future__ import annotations
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QDialog

from LRel.LRel import LRel
from ui.analyze_dialog_ui import Ui_Dialog


class LRelThreadAnalyzer(QThread):
    _signal = pyqtSignal(str)

    def __init__(self, lrel: LRel()):
        super().__init__()
        self.lrel = lrel


    def __del__(self):
        self.wait()

    def run(self):
        self._signal.emit("started")
        self.lrel.process_directories(self._signal)
        self._signal.emit("finished")
        self.quit()


class AnalyzeDialog(QDialog):
    def __init__(self, lrel: LRel(), parent = None):
        super().__init__(parent)
        self.lrel = lrel
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.connect_signal_slots()
        self.thread = LRelThreadAnalyzer(self.lrel)
        self.thread._signal.connect(self.text_update)
        self.thread.finished.connect(self.close)
        self.thread.start()

    def connect_signal_slots(self):
        self.ui.okButton.clicked.connect(self.ok_button_slot)

    def ok_button_slot(self):
        self.thread.quit()
        self.close()

    def text_update(self, msg: str):
        self.ui.currentFileLabel.setText(msg)
