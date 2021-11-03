import sys

from PyQt5 import uic
from PyQt5.QtCore import QSettings, Qt
from PyQt5.QtWidgets import QMessageBox, QFileDialog

class ClientConfView:
    """
    Client Configuration View
    """

    def __init__(self):
        # load client configuration
        self.settings = QSettings("config.ini", QSettings.IniFormat)
        self.testProgramPath = self.settings.value("CLIENT/Program")
        self.snapshotPath = self.settings.value("CLIENT/Snapshot")
        self.snapshotComPath = self.settings.value("CLIENT/Compare")
        self.healthPath = self.settings.value("CLIENT/Health")

        self.init()
    
    def init(self):
        # load client configuration ui and settings
        self.client_ui = uic.loadUi("ui/ClientConf.ui")
        self.client_ui.setWindowTitle("Client Configuration")
        self.client_ui.move(800, 400)
        self.client_ui.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.client_ui.lineEdit_1.setText(self.testProgramPath)
        self.client_ui.lineEdit_2.setText(self.snapshotPath)
        self.client_ui.lineEdit_3.setText(self.snapshotComPath)
        self.client_ui.lineEdit_4.setText(self.healthPath)
        
        # signal and slot for client ui
        self.client_ui.selectButton_1.clicked.connect(self.selectTestProgramPath)
        self.client_ui.selectButton_2.clicked.connect(self.selectSnapshotPath)
        self.client_ui.selectButton_3.clicked.connect(self.selectSnapshotReportPath)
        self.client_ui.selectButton_4.clicked.connect(self.selectHealthReportPath)
        self.client_ui.saveConfButton.clicked.connect(self.handleSaveClientConf)

    def selectTestProgramPath(self):
        self.testProgramPath = QFileDialog.getExistingDirectory(self.client_ui, "选择文件夹")
        self.client_ui.lineEdit_1.setText(self.testProgramPath)
        # print(self.client_ui.lineEdit_1.text())

    def selectSnapshotPath(self):
        """ select snapshot saved path """
        self.snapshotPath = QFileDialog.getExistingDirectory(self.client_ui, "选择文件夹")
        self.client_ui.lineEdit_2.setText(self.snapshotPath)

    def selectSnapshotReportPath(self):
        self.snapshotComPath = QFileDialog.getExistingDirectory(self.client_ui, "选择文件夹")
        self.client_ui.lineEdit_3.setText(self.snapshotComPath)

    def selectHealthReportPath(self):
        self.healthPath = QFileDialog.getExistingDirectory(self.client_ui, "选择文件夹")
        self.client_ui.lineEdit_4.setText(self.healthPath)

    def handleSaveClientConf(self):
        """
        save client configuration
        """
        self.settings.setValue("CLIENT/Program", self.testProgramPath)
        self.settings.setValue("CLIENT/Snapshot", self.snapshotPath)
        self.settings.setValue("CLIENT/Compare", self.snapshotComPath)
        self.settings.setValue("CLIENT/Health", self.healthPath)
        QMessageBox.information(self.client_ui, '提示', '配置保存成功!', QMessageBox.Yes)
        self.client_ui.close()