import sys

from PyQt5 import uic
from PyQt5.QtCore import QSettings, Qt
from PyQt5.QtWidgets import QMessageBox

class ServerConfView:
    """
    Server Configuration View
    """

    def __init__(self):
        # load server configuration
        self.settings = QSettings("view/config.ini", QSettings.IniFormat)

        self.ref_remoteHost = self.settings.value("SERVER/REF_RemoteHost")
        self.ref_port = self.settings.value("SERVER/REF_Port")
        self.ref_hostname = self.settings.value("SERVER/REF_Hostname")
        self.ref_password = self.settings.value("SERVER/REF_Password")

        self.dut_remoteHost = self.settings.value("SERVER/DUT_RemoteHost")
        self.dut_port = self.settings.value("SERVER/DUT_Port")
        self.dut_hostname = self.settings.value("SERVER/DUT_Hostname")
        self.dut_password = self.settings.value("SERVER/DUT_Password")

        self.init()
    
    def init(self):
        # load server configuration ui and settings
        self.server_ui = uic.loadUi("ui/serverConf.ui")
        self.server_ui.setWindowTitle("Server Configuration")
        self.server_ui.move(800, 400)
        self.server_ui.setWindowFlags(Qt.WindowStaysOnTopHint)

        if self.server_ui.tabWidget.currentIndex() == 0:
            self.server_ui.IPEdit.setText(self.ref_remoteHost)
            self.server_ui.PortSpinBox.setValue(int(self.ref_port))
            self.server_ui.HostnameEdit.setText(self.ref_hostname)
            self.server_ui.PasswdEdit.setText(self.ref_password)
            self.server_ui.PortSpinBox.valueChanged.connect(self.handleREFChangedPort)

        self.server_ui.tabWidget.setCurrentIndex(1)
        
        if self.server_ui.tabWidget.currentIndex() == 1:
            self.server_ui.IPEdit_2.setText(self.dut_remoteHost)
            self.server_ui.PortSpinBox_2.setValue(int(self.dut_port))
            self.server_ui.HostnameEdit_2.setText(self.dut_hostname)
            self.server_ui.PasswdEdit_2.setText(self.dut_password)
            self.server_ui.PortSpinBox_2.valueChanged.connect(self.handleDUTChangedPort)

        self.server_ui.saveConfButton.clicked.connect(self.handleSaveServerConf)

    def handleSaveServerConf(self):
        """
        save server configuration
        """
        # self.ServerConfDict = {}
        # self.ServerConfDict["ip"] = self.remoteHost
        # self.ServerConfDict["port"] = self.port
        # self.ServerConfDict["hostname"] = self.server_ui.HostnameEdit.text()
        # self.ServerConfDict["password"] = self.server_ui.PasswdEdit.text()
        # for key in self.ServerConfDict:
        #     print(key, ": ", self.ServerConfDict[key])
        self.settings.setValue("SERVER/REF_RemoteHost", self.server_ui.IPEdit.text())
        self.settings.setValue("SERVER/REF_Port", self.ref_port)
        self.settings.setValue("SERVER/REF_Hostname", self.server_ui.HostnameEdit.text())
        self.settings.setValue("SERVER/REF_Password", self.server_ui.PasswdEdit.text())

        self.settings.setValue("SERVER/DUT_RemoteHost", self.server_ui.IPEdit_2.text())
        self.settings.setValue("SERVER/DUT_Port", self.dut_port)
        self.settings.setValue("SERVER/DUT_Hostname", self.server_ui.HostnameEdit_2.text())
        self.settings.setValue("SERVER/DUT_Password", self.server_ui.PasswdEdit_2.text())

        QMessageBox.information(self.server_ui, '提示', '配置保存成功!', QMessageBox.Yes)
        self.server_ui.close()

    def handleREFChangedPort(self):
        self.ref_port = self.server_ui.PortSpinBox.value()

    def handleDUTChangedPort(self):
        self.dut_port = self.server_ui.PortSpinBox_2.value()