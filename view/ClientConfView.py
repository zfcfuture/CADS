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
        self.settings = QSettings("view/config.ini", QSettings.IniFormat)
        self.snapshotPath = self.settings.value("CLIENT/Snapshot")
        self.snapshotComPath = self.settings.value("CLIENT/Compare")
        self.healthPath = self.settings.value("CLIENT/Health")
        self.RefELF = self.settings.value("CLIENT/RefELF")
        self.DUTELF = self.settings.value("CLIENT/DUTELF")

        self.init()
    
    def init(self):
        # load client configuration ui and settings
        self.client_ui = uic.loadUi("ui/ClientConf.ui")
        self.client_ui.setWindowTitle("Client Configuration")
        self.client_ui.move(800, 400)
        self.client_ui.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.client_ui.lineEdit_1.setText(self.snapshotPath)
        self.client_ui.lineEdit_2.setText(self.snapshotComPath)
        self.client_ui.lineEdit_3.setText(self.healthPath)
        self.client_ui.lineEdit_4.setText(self.RefELF)
        self.client_ui.lineEdit_5.setText(self.DUTELF)
        
        # signal and slot for client ui
        self.client_ui.selectButton_1.clicked.connect(self.selectSnapshotPath)
        self.client_ui.selectButton_2.clicked.connect(self.selectSnapshotReportPath)
        self.client_ui.selectButton_3.clicked.connect(self.selectHealthReportPath)
        self.client_ui.selectButton_4.clicked.connect(self.RefElfFilePath)
        self.client_ui.saveConfButton.clicked.connect(self.handleSaveClientConf)

    def selectSnapshotPath(self):
        self.snapshotPath = QFileDialog.getExistingDirectory(self.client_ui, "选择文件夹")
        self.client_ui.lineEdit_1.setText(self.snapshotPath)
        # print(self.client_ui.lineEdit_1.text())

    def selectSnapshotReportPath(self):
        """ select snapshot saved path """
        self.snapshotComPath = QFileDialog.getExistingDirectory(self.client_ui, "选择文件夹")
        self.client_ui.lineEdit_2.setText(self.snapshotComPath)

    def selectHealthReportPath(self):
        self.healthPath = QFileDialog.getExistingDirectory(self.client_ui, "选择文件夹")
        self.client_ui.lineEdit_3.setText(self.healthPath)

    def RefElfFilePath(self):
        self.RefELF = QFileDialog.getExistingDirectory(self.client_ui, "选择文件夹")
        self.client_ui.lineEdit_4.setText(self.RefELF)

    def handleSaveClientConf(self):
        """
        save client configuration
        """
        self.settings.setValue("CLIENT/Snapshot", self.snapshotPath)
        self.settings.setValue("CLIENT/Compare", self.snapshotComPath)
        self.settings.setValue("CLIENT/Health", self.healthPath)
        self.settings.setValue("CLIENT/RefELF", self.RefELF)
        self.settings.setValue("CLIENT/DUTELF", self.client_ui.lineEdit_5.text())
        QMessageBox.information(self.client_ui, '提示', '配置保存成功!', QMessageBox.Yes)
        self.client_ui.close()