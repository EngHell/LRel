from pathlib import Path

from PyQt5 import QtGui
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QAction, qApp, QMenu, QFileDialog, QVBoxLayout, QPushButton


class MainWindow(QMainWindow):
    q_actions = {}
    working_directory = None
    status_bar = None

    def __init__(self):
        super().__init__()

        # status bar things
        self.status_bar = self.statusBar()
        self.status_bar.showMessage("Ready")

        # menu bar files
        self.init_menu()

        # init tool bar
        self.init_toolbar()

        # init layout
        self.init_layout()

        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle("Simple menu")
        self.show()

    def init_menu(self):
        open_action = QAction(QIcon("windowicon.png"), "&Open", self)
        open_action.setShortcut("Ctrl+O")
        open_action.setStatusTip("Opens a project")
        open_action.triggered.connect(self.show_open_dialog)
        self.q_actions["open_action"] = open_action

        exit_action = QAction(QIcon('windowicon.png'), "&Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.setStatusTip("Closes the application")
        exit_action.triggered.connect(qApp.quit)

        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("&File")
        file_menu.addAction(open_action)
        file_menu.addAction(exit_action)

    def init_toolbar(self):
        toolbar = self.addToolBar("Exit")
        toolbar.addAction(self.q_actions["open_action"])

    def init_layout(self):
        # fixing this later. and at this point im thinking of using qt designer :]
        ok_button = QPushButton("Ok")
        cancel_button = QPushButton("Cancel")

        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addWidget(ok_button)
        vbox.addWidget(cancel_button)

        self.setLayout(vbox)

    def show_open_dialog(self):
        home_dir = str(Path.home())
        directory = QFileDialog.getExistingDirectory(
            self,
            "Select the project file",
            home_dir
        )

        if directory:
            self.working_directory = directory
            self.status_bar.showMessage(f"Opened directory:{directory}")

    def contextMenuEvent(self, event: QtGui.QContextMenuEvent) -> None:
        context_menu = QMenu(self)
        quit_action = context_menu.addAction("Quit")
        executed_action = context_menu.exec_(self.mapToGlobal(event.pos()))

        if executed_action == quit_action:
            self.close()
