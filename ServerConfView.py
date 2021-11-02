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
        self.settings = QSettings("config.ini", QSettings.IniFormat)
        self.remoteHost = self.settings.value("SERVER/RemoteHost")
        self.port = self.settings.value("SERVER/Port")
        self.hostname = self.settings.value("SERVER/Hostname")
        self.password = self.settings.value("SERVER/Password")

        self.init()
    
    def init(self):
        # load server configuration ui and settings
        self.server_ui = uic.loadUi("ui/serverConf.ui")
        self.server_ui.setWindowTitle("Server Configuration")
        self.server_ui.move(800, 400)
        self.server_ui.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.server_ui.IPComboBox.setCurrentText(self.remoteHost)
        self.server_ui.PortSpinBox.setValue(int(self.port))
        self.server_ui.HostnameEdit.setText(self.hostname)
        self.server_ui.PasswdEdit.setText(self.password)

        # signal and slot for server ui
        self.server_ui.IPComboBox.activated.connect(self.handleIPActivated)
        self.server_ui.PortSpinBox.valueChanged.connect(self.handleChangedPort)
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
        self.settings.setValue("SERVER/RemoteHost", self.remoteHost)
        self.settings.setValue("SERVER/Port", self.port)
        self.settings.setValue("SERVER/Hostname", self.server_ui.HostnameEdit.text())
        self.settings.setValue("SERVER/Password", self.server_ui.PasswdEdit.text())
        QMessageBox.information(self.server_ui, '提示', '配置保存成功!', QMessageBox.Yes)
        self.server_ui.close()

    def handleIPActivated(self, index):
        if self.server_ui.IPComboBox.itemText(index) == 'HAPS01':
            self.remoteHost = "HAPS01"
        else:
            self.remoteHost = "Host"

    def handleChangedPort(self):
        self.port = self.server_ui.PortSpinBox.value()