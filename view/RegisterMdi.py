import sys
import re

from PyQt5 import QtCore, QtGui
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

        #Window button
        max_button1 = QPushButton()
        max_button1.setMaximumSize(18,18)
        max_button1.setIcon(QtGui.QIcon('imgs/icon/max.png'))
        max_button1.setIconSize(QtCore.QSize(14, 14))
        max_button1.setStyleSheet("border:none;")
        min_button1 = QPushButton()
        min_button1.setMaximumSize(18,18)
        min_button1.setIcon(QtGui.QIcon('imgs/icon/min.png'))
        min_button1.setIconSize(QtCore.QSize(14, 14))
        min_button1.setStyleSheet("border:none;")
        title_Hlayout1 = QHBoxLayout()
        title_Hlayout1.addItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        title_Hlayout1.addWidget(min_button1)
        title_Hlayout1.addWidget(max_button1)
        titile_widget1 = QWidget()
        titile_widget1.setLayout(title_Hlayout1)

        tab_layout1 = QHBoxLayout()
        tab_widget1 = QWidget()
        self.reg_dut_tabWidget = QTabWidget()
        tab_layout1.addWidget(self.reg_dut_tabWidget)
        tab_widget1.setLayout(tab_layout1)
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
        reg_dutVlayout.addWidget(titile_widget1)
        reg_dutVlayout.addWidget(reg_titlelable1)
        reg_dutVlayout.addWidget(tab_widget1)
        reg_dutVlayout.addWidget(reg_dut_hwg)
        reg_dut_scroll = QScrollArea()
        reg_dut_scroll.setLayout(reg_dutVlayout)
        self.setWidget(reg_dut_scroll)

        reg_dutVlayout.setContentsMargins(9,0,0,0)
        title_Hlayout1.setContentsMargins(0,2,4,0)
        tab_layout1.setContentsMargins(0,0,9,0)

        max_button1.pressed.connect(self.maxshow)
        min_button1.pressed.connect(self.minshow)

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
        layout = QVBoxLayout()
        self.tableFPR = QTableWidget(32, 3)
        self.tableFPR.setHorizontalHeaderLabels(["Name", "Alias", "Value"])
        self.tableFPR.horizontalHeader().setStretchLastSection(True)
        # self.tableFPR.verticalHeader.setHidden(True)
        self.tableFPR.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.tableFPR.setColumnWidth(0, 50)
        self.tableFPR.setColumnWidth(1, 50)
        layout.addWidget(self.tableFPR)
        layout.setContentsMargins(0, 0, 0, 0)
        self.dut_FPR_tab.setLayout(layout)
        self.tableFPR.verticalHeader().setVisible(False)

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
        for i in range(len(content)):
            # GPRList[i] = re.split(" |\t|\n|\r", content[i])
            content[i] = list(filter(None, re.split(" |\t|\n|\r", content[i])))

        f.close()
        return content
    
    def maxshow(self):
        self.showMaximized()

    def minshow(self):
        self.showNormal()

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

        #Window button
        max_button2 = QPushButton()
        max_button2.setMaximumSize(18,18)
        max_button2.setIcon(QtGui.QIcon('imgs/icon/max.png'))
        max_button2.setIconSize(QtCore.QSize(14, 14))
        max_button2.setStyleSheet("border:none;")
        min_button2 = QPushButton()
        min_button2.setMaximumSize(18,18)
        min_button2.setIcon(QtGui.QIcon('imgs/icon/min.png'))
        min_button2.setIconSize(QtCore.QSize(14, 14))
        min_button2.setStyleSheet("border:none;")
        title_Hlayout2 = QHBoxLayout()
        title_Hlayout2.addItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        title_Hlayout2.addWidget(min_button2)
        title_Hlayout2.addWidget(max_button2)
        titile_widget2 = QWidget()
        titile_widget2.setLayout(title_Hlayout2)

        tab_layout2 = QHBoxLayout()
        tab_widget2 = QWidget()
        self.reg_ref_tabWidget = QTabWidget()
        tab_layout2.addWidget(self.reg_ref_tabWidget)
        tab_widget2.setLayout(tab_layout2)
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
        reg_refVlayout.addWidget(titile_widget2)
        reg_refVlayout.addWidget(reg_titlelable2)
        reg_refVlayout.addWidget(tab_widget2)
        reg_refVlayout.addWidget(reg_ref_hwg)
        reg_ref_scroll = QScrollArea()
        reg_ref_scroll.setLayout(reg_refVlayout)
        self.setWidget(reg_ref_scroll)

        reg_refVlayout.setContentsMargins(9,0,0,0)
        title_Hlayout2.setContentsMargins(0,2,4,0)
        tab_layout2.setContentsMargins(0,0,9,0)

        max_button2.pressed.connect(self.maxshow)
        min_button2.pressed.connect(self.minshow)

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
        layout = QVBoxLayout()
        self.tableFPR = QTableWidget(32, 3)
        self.tableFPR.setHorizontalHeaderLabels(["Name", "Alias", "Value"])
        self.tableFPR.horizontalHeader().setStretchLastSection(True)
        # self.tableFPR.verticalHeader.setHidden(True)
        self.tableFPR.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.tableFPR.setColumnWidth(0, 50)
        self.tableFPR.setColumnWidth(1, 50)
        layout.addWidget(self.tableFPR)
        layout.setContentsMargins(0, 0, 0, 0)
        self.ref_FPR_tab.setLayout(layout)
        self.tableFPR.verticalHeader().setVisible(False)

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
        for i in range(len(content)):
            # GPRList[i] = re.split(" |\t|\n|\r", content[i])
            content[i] = list(filter(None, re.split(" |\t|\n|\r", content[i])))

        f.close()
        # print(content)
        return content

    def maxshow(self):
        self.showMaximized()

    def minshow(self):
        self.showNormal()