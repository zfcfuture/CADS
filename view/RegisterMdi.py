import sys
import re

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from ClientConfView import ClientConfView

class REGDUTsub(QMdiSubWindow):

    """
    DUT Registers View
    """
    def __init__(self):

        super().__init__()

        self.clientView = ClientConfView()

        reg_dutlabel = QLabel()
        reg_dutlabel.setText('Display type:')
        reg_dutcombo = QComboBox()
        reg_dutcombo.addItems(['Hex', 'Binary','ASCⅡ'])
        reg_dutHlayout = QHBoxLayout()
        reg_dutHlayout.addItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        reg_dutHlayout.addWidget(reg_dutlabel)
        reg_dutHlayout.addWidget(reg_dutcombo)
        reg_dut_hwg = QWidget()
        reg_dut_hwg.setLayout(reg_dutHlayout)

        self.reg_dut_tabWidget = QTabWidget()
        self.dut_GPR_tab = QWidget()
        self.dut_FPR_tab = QWidget()
        self.dut_CSR_tab = QWidget()
        self.reg_dut_tabWidget.addTab(self.dut_GPR_tab, "")
        self.reg_dut_tabWidget.addTab(self.dut_FPR_tab, "")
        self.reg_dut_tabWidget.addTab(self.dut_CSR_tab, "")
        self.reg_dut_tabWidget.setTabText(0, 'GPR')
        self.reg_dut_tabWidget.setTabText(1, 'FPR')
        self.reg_dut_tabWidget.setTabText(2, 'CSR')
        self.GPR_tabUI()
        self.FPR_tabUI()
        self.CSR_tabUI()

        reg_titlelable1 = QLabel()
        reg_titlelable1.setText('DUT')
        reg_dutVlayout = QVBoxLayout()
        reg_dutVlayout.addWidget(reg_titlelable1)
        reg_dutVlayout.addWidget(self.reg_dut_tabWidget)
        reg_dutVlayout.addWidget(reg_dut_hwg)
        reg_dut_vwg = QWidget()
        reg_dut_vwg.setLayout(reg_dutVlayout)
        self.setWidget(reg_dut_vwg)

    def GPR_tabUI(self):
        # add a table for GPR_tabUI
        layout = QVBoxLayout()
        self.tableGPR = QTableWidget(33, 3)
        self.tableGPR.setHorizontalHeaderLabels(["Name", "Alias", "Value"])
        self.tableGPR.horizontalHeader().setStretchLastSection(True)
        self.tableGPR.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.tableGPR.setColumnWidth(0, 50)
        self.tableGPR.setColumnWidth(1, 50)
        layout.addWidget(self.tableGPR)
        layout.setContentsMargins(0, 0, 0, 0)
        self.dut_GPR_tab.setLayout(layout)
        self.tableGPR.verticalHeader().setVisible(False)

    def FPR_tabUI(self):
        
        pass

    def CSR_tabUI(self):
        
        pass

    def display(self):
        # get data from file
        fileContent = self.getData()

        # put data to tableGPR
        GPRName = ["x{i}".format(i=i+1) for i in range(31)]
        GPRName.append("pc")
        for i in range(32):
            self.item_name = QTableWidgetItem(GPRName[i])
            self.item_name.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.tableGPR.setItem(i, 0, self.item_name)
            self.item_Alias = QTableWidgetItem(fileContent[i][0])
            self.item_Alias.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.tableGPR.setItem(i, 1, self.item_Alias)
            self.item_Value = QTableWidgetItem(fileContent[i][1])
            self.item_Value.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.tableGPR.setItem(i, 2, self.item_Value)
            

    def getData(self):
        healthPath = self.clientView.settings.value("CLIENT/DUT_Health")
        filePath = healthPath + "/cpu_status_haps"

        with open(filePath) as f:
            content = f.read()
        content = content.split("\n")
        # GPRList = []
        for i in range(33):
            # GPRList[i] = re.split(" |\t|\n|\r", content[i])
            content[i] = list(filter(None, re.split(" |\t|\n|\r", content[i])))

        return content

class REGREFsub(QMdiSubWindow):

    """
    Reference Registers View
    """
    def __init__(self):

        super().__init__()

        self.clientView = ClientConfView()

        reg_reflabel = QLabel()
        reg_reflabel.setText('Display type:')
        reg_refcombo = QComboBox()
        reg_refcombo.addItems(['Hex', 'Binary','ASCⅡ'])
        reg_refHlayout = QHBoxLayout()
        reg_refHlayout.addItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        reg_refHlayout.addWidget(reg_reflabel)
        reg_refHlayout.addWidget(reg_refcombo)
        reg_ref_hwg = QWidget()
        reg_ref_hwg.setLayout(reg_refHlayout)

        self.reg_ref_tabWidget = QTabWidget()
        self.ref_GPR_tab = QWidget()
        self.ref_FPR_tab = QWidget()
        self.ref_CSR_tab = QWidget()
        self.reg_ref_tabWidget.addTab(self.ref_GPR_tab, "")
        self.reg_ref_tabWidget.addTab(self.ref_FPR_tab, "")
        self.reg_ref_tabWidget.addTab(self.ref_CSR_tab, "")
        self.reg_ref_tabWidget.setTabText(0, 'GPR')
        self.reg_ref_tabWidget.setTabText(1, 'FPR')
        self.reg_ref_tabWidget.setTabText(2, 'CSR')
        self.GPR_tabUI()
        self.FPR_tabUI()
        self.CSR_tabUI()

        reg_titlelable2 = QLabel()
        reg_titlelable2.setText('Reference')
        reg_refVlayout = QVBoxLayout()
        reg_refVlayout.addWidget(reg_titlelable2)
        reg_refVlayout.addWidget(self.reg_ref_tabWidget)
        reg_refVlayout.addWidget(reg_ref_hwg)
        reg_ref_vwg = QWidget()
        reg_ref_vwg.setLayout(reg_refVlayout)
        self.setWidget(reg_ref_vwg)

    def GPR_tabUI(self):
        layout = QVBoxLayout()
        self.tableGPR = QTableWidget(32, 3)
        self.tableGPR.setHorizontalHeaderLabels(["Name", "Alias", "Value"])
        self.tableGPR.horizontalHeader().setStretchLastSection(True)
        # self.tableGPR.verticalHeader.setHidden(True)
        self.tableGPR.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.tableGPR.setColumnWidth(0, 50)
        self.tableGPR.setColumnWidth(1, 50)
        layout.addWidget(self.tableGPR)
        layout.setContentsMargins(0, 0, 0, 0)
        self.ref_GPR_tab.setLayout(layout)
        self.tableGPR.verticalHeader().setVisible(False)

    def FPR_tabUI(self):
        
        pass

    def CSR_tabUI(self):
        
        pass

    def display(self):
        # get data from file
        fileContent = self.getData()

        # put data to tableGPR
        GPRName = ["x{i}".format(i=i+1) for i in range(31)]
        GPRName.append("pc")
        for i in range(32):
            self.item_name = QTableWidgetItem(GPRName[i])
            self.item_name.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.tableGPR.setItem(i, 0, self.item_name)
            self.item_Alias = QTableWidgetItem(fileContent[i][0])
            self.item_Alias.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.tableGPR.setItem(i, 1, self.item_Alias)
            self.item_Value = QTableWidgetItem(fileContent[i][1])
            self.item_Value.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.tableGPR.setItem(i, 2, self.item_Value)
            

    def getData(self):
        healthPath = self.clientView.settings.value("CLIENT/REF_Health")
        filePath = healthPath + "/cpu_status_spike"

        with open(filePath) as f:
            content = f.read()
        content = content.split("\n")
        # GPRList = []
        for i in range(33):
            # GPRList[i] = re.split(" |\t|\n|\r", content[i])
            content[i] = list(filter(None, re.split(" |\t|\n|\r", content[i])))

        return content