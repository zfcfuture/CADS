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

        self.ref_snapshotPath = self.settings.value("CLIENT/REF_Snapshot")
        self.dut_snapshotPath = self.settings.value("CLIENT/DUT_Snapshot")
        self.snapshotComPath = self.settings.value("CLIENT/Snap_Compare")

        self.ref_healthPath = self.settings.value("CLIENT/REF_Health")
        self.dut_healthPath = self.settings.value("CLIENT/DUT_Health")
        self.healthCompare = self.settings.value("CLIENT/heal_Compare")

        self.RefELF = self.settings.value("CLIENT/RefELF")
        self.DUTELF = self.settings.value("CLIENT/DUTELF")

        self.init()
    
    def init(self):
        # load client configuration ui and settings
        self.client_ui = uic.loadUi("ui/ClientConf.ui")
        self.client_ui.setWindowTitle("Client Configuration")
        self.client_ui.move(800, 400)
        self.client_ui.setWindowFlags(Qt.WindowStaysOnTopHint)

        self.client_ui.lineEdit_1.setText(self.ref_snapshotPath)
        self.client_ui.lineEdit_2.setText(self.dut_snapshotPath)
        self.client_ui.lineEdit_3.setText(self.snapshotComPath)
        self.client_ui.lineEdit_4.setText(self.ref_healthPath)
        self.client_ui.lineEdit_5.setText(self.dut_healthPath)
        self.client_ui.lineEdit_6.setText(self.healthCompare)
        self.client_ui.lineEdit_7.setText(self.RefELF)
        self.client_ui.lineEdit_8.setText(self.DUTELF)
        
        # signal and slot for client ui
        self.client_ui.selectButton_1.clicked.connect(self.selectREFSnapshotPath)
        self.client_ui.selectButton_2.clicked.connect(self.selectDUTSnapshotPath)
        self.client_ui.selectButton_3.clicked.connect(self.selectSnapshotReportPath)
        self.client_ui.selectButton_4.clicked.connect(self.selectREFHealthPath)
        self.client_ui.selectButton_5.clicked.connect(self.selectDUTHealthPath)
        self.client_ui.selectButton_6.clicked.connect(self.selectHealthReportPath)
        self.client_ui.saveConfButton.clicked.connect(self.handleSaveClientConf)

    def selectREFSnapshotPath(self):
        self.ref_snapshotPath = QFileDialog.getExistingDirectory(self.client_ui, "选择文件夹")
        self.client_ui.lineEdit_1.setText(self.ref_snapshotPath)
        # print(self.client_ui.lineEdit_1.text())
    
    def selectDUTSnapshotPath(self):
        self.dut_snapshotPath = QFileDialog.getExistingDirectory(self.client_ui, "选择文件夹")
        self.client_ui.lineEdit_2.setText(self.dut_snapshotPath)

    def selectSnapshotReportPath(self):
        """ select snapshot saved path """
        self.snapshotComPath = QFileDialog.getExistingDirectory(self.client_ui, "选择文件夹")
        self.client_ui.lineEdit_3.setText(self.snapshotComPath)

    def selectREFHealthPath(self):
        self.ref_healthPath = QFileDialog.getExistingDirectory(self.client_ui, "选择文件夹")
        self.client_ui.lineEdit_4.setText(self.ref_healthPath)

    def selectDUTHealthPath(self):
        self.dut_healthPath = QFileDialog.getExistingDirectory(self.client_ui, "选择文件夹")
        self.client_ui.lineEdit_5.setText(self.dut_healthPath)

    def selectHealthReportPath(self):
        self.healthCompare = QFileDialog.getExistingDirectory(self.client_ui, "选择文件夹")
        self.client_ui.lineEdit_6.setText(self.healthCompare)

    def handleSaveClientConf(self):
        """
        save client configuration
        """
        self.settings.setValue("CLIENT/REF_Snapshot", self.ref_snapshotPath)
        self.settings.setValue("CLIENT/DUT_Snapshot", self.dut_snapshotPath)
        self.settings.setValue("CLIENT/Snap_Compare", self.snapshotComPath)
        self.settings.setValue("CLIENT/REF_Health", self.ref_healthPath)
        self.settings.setValue("CLIENT/DUT_Health", self.dut_healthPath)
        self.settings.setValue("CLIENT/heal_Compare", self.healthCompare)
        self.settings.setValue("CLIENT/RefELF", self.client_ui.lineEdit_7.text())
        self.settings.setValue("CLIENT/DUTELF", self.client_ui.lineEdit_8.text())
        QMessageBox.information(self.client_ui, '提示', '配置保存成功!', QMessageBox.Yes)
        self.client_ui.close()