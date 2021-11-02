import sys

from PyQt5 import uic
from PyQt5.QtCore import QSettings, Qt
from PyQt5.QtWidgets import QMessageBox, QFileDialog

class SnapshotImportView:
    """
    Snapshot Import View
    """

    def __init__(self):
        self.init()

    def init(self):
        # load snapshot-import ui
        self.import_ui = uic.loadUi("ui/import.ui")
        self.import_ui.setWindowTitle("Import Snapshot")
        self.import_ui.move(800, 400)
        self.import_ui.setWindowFlags(Qt.WindowStaysOnTopHint)

        # connect signal and slot
        # index = self.import_ui.tabWidget.currentIndex()
        if self.import_ui.tabWidget.currentIndex() == 0:
            self.import_ui.REFSelectButton.clicked.connect(self.handleRefSelect)
            self.import_ui.REFComboBox.activated.connect(self.handleRefComboBox)
            self.import_ui.REFImportButton.clicked.connect(self.handleRefImport)
        self.import_ui.tabWidget.setCurrentIndex(1)
        if self.import_ui.tabWidget.currentIndex() == 1:
            self.import_ui.DUTSelectButton.clicked.connect(self.handleDUTSelect)
            self.import_ui.DUTComboBox.activated.connect(self.handleDUTComboBox)
            self.import_ui.DUTImportButton.clicked.connect(self.handleDUTImport)
        # self.import_ui.tabWidget.currentChanged.connect(self.handleChanged)

    # def handleChanged(self, page):
        # if page == 1:
    #         self.import_ui.REFSelectButton.clicked.connect(self.handleRefSelect)
    #         self.import_ui.REFComboBox.activated.connect(self.handleRefComboBox)
    #         self.import_ui.REFImportButton.clicked.connect(self.handleRefImport)
    #     else:
            # self.import_ui.DUTSelectButton.clicked.connect(self.handleDUTSelect)
            # self.import_ui.DUTComboBox.activated.connect(self.handleDUTComboBox)
            # self.import_ui.DUTImportButton.clicked.connect(self.handleDUTImport)

    def handleRefSelect(self):
        self.RefImportPath, _ = QFileDialog.getOpenFileName(self.import_ui, "选择文件")
        self.import_ui.REFlLineEdit.setText(self.RefImportPath)

    def handleRefComboBox(self, index):
        self.RefEnv = self.import_ui.REFComboBox.itemText(index)
        # print(self.RefEnv)

    def handleRefImport(self):
        print("coming soon...")

    def handleDUTSelect(self):
        self.DUTImportPath, _ = QFileDialog.getOpenFileName(self.import_ui, "选择文件")
        self.import_ui.DUTLineEdit.setText(self.DUTImportPath)

    def handleDUTComboBox(self, index):
        self.DUTEnv = self.import_ui.DUTComboBox.itemText(index)
        # print(self.DUTEnv)

    def handleDUTImport(self):
        if self.import_ui.DUTComboBox.currentText() == "HAPS":
            print("hello")
        else:
            pass