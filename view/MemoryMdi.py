import sys
import re

from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from ClientConfView import ClientConfView

class MEMDUTsub(QMdiSubWindow):

    """
    DUT Mem Date View
    """
    def __init__(self):

        super().__init__()

        self.clientView = ClientConfView()

        #memDUT_sub = QMdiSubWindow(self)
        self.mem_dutlabel1 = QLabel()
        self.mem_dutlabel2 = QLabel()
        self.mem_dutlabel1.setText('Display type:')
        self.mem_dutlabel2.setText('Go to register:')
        self.dut_typecombo = QComboBox()
        self.dut_regcombo = QComboBox()
        self.dut_typecombo.addItems(['Hex', 'Binary', 'Unsigned', 'Signed', 'ASCⅡ', 'Float'])
        self.dut_regcombo.addItems(['Select', 'x0', 'x1(ra)', 'x2(sp)', 'x3(gp)', 'x4(tp)',\
             'x5(t0)', 'x6(t1)', 'x7(t2)','x8(s0)'])
        
        mem_dutHlayout = QHBoxLayout()
        mem_dutHlayout.addItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        mem_dutHlayout.addWidget(self.mem_dutlabel1)
        mem_dutHlayout.addWidget(self.dut_typecombo)
        mem_dutHlayout.addWidget(self.mem_dutlabel2)
        mem_dutHlayout.addWidget(self.dut_regcombo)
        mem_dut_hwg = QWidget()
        mem_dut_hwg.setLayout(mem_dutHlayout)

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

        mem_titlelable1 = QLabel('DUT')
        title_Hlayout1 = QHBoxLayout()
        title_Hlayout1.addWidget(mem_titlelable1)
        title_Hlayout1.addItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        title_Hlayout1.addWidget(min_button1)
        title_Hlayout1.addWidget(max_button1)
        titile_widget1 = QWidget()
        titile_widget1.setLayout(title_Hlayout1)

        #table widget
        table_layout1 = QHBoxLayout()
        table_widget1 = QWidget()
        self.dut_tableWidget = QTableWidget()
        table_layout1.addWidget(self.dut_tableWidget)
        table_widget1.setLayout(table_layout1)
        self.dut_tableWidget.setRowCount(12904)
        self.dut_tableWidget.setColumnCount(9)
        self.dut_tableWidget.setHorizontalHeaderLabels(['Address', 'Word0', 'Word1', 'Word2', 'Word3', \
                                                                   'Word4', 'Word5', 'Word6', 'Word7'])
        self.dut_tableWidget.setShowGrid(False)
        self.dut_tableWidget.verticalHeader().setVisible(False)
        self.dut_tableWidget.horizontalHeader().setStretchLastSection(True)
        self.dut_tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        mem_dutVlayout = QVBoxLayout()
        mem_dutVlayout.addWidget(titile_widget1)
        mem_dutVlayout.addWidget(table_widget1)
        mem_dutVlayout.addWidget(mem_dut_hwg)
        mem_dut_scroll = QScrollArea()
        mem_dut_scroll.setLayout(mem_dutVlayout)
        self.setWidget(mem_dut_scroll)

        mem_dutVlayout.setContentsMargins(9,0,0,0)
        title_Hlayout1.setContentsMargins(0,2,4,0)
        table_layout1.setContentsMargins(0,9,9,0)
        
        max_button1.pressed.connect(self.maxshow)
        min_button1.pressed.connect(self.minshow)

    def maxshow(self):
        self.showMaximized()

    def minshow(self):
        self.showNormal()

    def display(self):
        # handle data
        memoryPath = self.clientView.settings.value("CLIENT/DUT_Snapshot") + "/memsnapshot_hexdump_haps.txt"
        with open(memoryPath) as f:
            content = f.read()
        f.close()
        content = content.split("\n")

        finalData = []
        deleteNum = ['0000', '0000', '0000', '0000', '0000', '0000', '0000', '0000']
        for i in range(len(content)):
            content[i] = list(filter(None, re.split(" |\t|\n|\r", content[i])))
            if content[i] == []:
                continue
            elif content[i][0] == "*":
                continue
            elif content[i][1:] == deleteNum:
                continue
            finalData.append(content[i])

        # display
        for i in range(self.dut_tableWidget.rowCount()):
            if i == self.dut_tableWidget.rowCount()-1:
                self.item_Addres = QTableWidgetItem(finalData[i][0])
                self.item_Addres.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.dut_tableWidget.setItem(i, 0, self.item_Addres)
                break
            else:
                self.item_Addres = QTableWidgetItem(finalData[i][0])
                self.item_Addres.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.dut_tableWidget.setItem(i, 0, self.item_Addres)

            self.item_Word0 = QTableWidgetItem(finalData[i][1])
            self.item_Word0.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.dut_tableWidget.setItem(i, 1, self.item_Word0)

            self.item_Word1 = QTableWidgetItem(finalData[i][2])
            self.item_Word1.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.dut_tableWidget.setItem(i, 2, self.item_Word1)

            self.item_Word2 = QTableWidgetItem(finalData[i][3])
            self.item_Word2.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.dut_tableWidget.setItem(i, 3, self.item_Word2)

            self.item_Word3 = QTableWidgetItem(finalData[i][4])
            self.item_Word3.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.dut_tableWidget.setItem(i, 4, self.item_Word3)

            self.item_Word4 = QTableWidgetItem(finalData[i][5])
            self.item_Word4.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.dut_tableWidget.setItem(i, 5, self.item_Word4)

            self.item_Word5 = QTableWidgetItem(finalData[i][6])
            self.item_Word5.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.dut_tableWidget.setItem(i, 6, self.item_Word5)

            self.item_Word6 = QTableWidgetItem(finalData[i][7])
            self.item_Word6.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.dut_tableWidget.setItem(i, 7, self.item_Word6)

            self.item_Word7 = QTableWidgetItem(finalData[i][8])
            self.item_Word7.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.dut_tableWidget.setItem(i, 8, self.item_Word7)


class MEMREFsub(QMdiSubWindow):

    """
    Reference Mem Date View
    """
    def __init__(self):

        super().__init__()

        self.clientView = ClientConfView()

        #memREF_sub = QMdiSubWindow(self)
        self.mem_reflabel1 = QLabel()
        self.mem_reflabel2 = QLabel()
        self.mem_reflabel1.setText('Display type:')
        self.mem_reflabel2.setText('Go to register:')
        self.ref_typecombo = QComboBox()
        self.ref_regcombo = QComboBox()
        self.ref_typecombo.addItems(['Hex', 'Binary', 'Unsigned', 'Signed', 'ASCⅡ', 'Float'])
        self.ref_regcombo.addItems(['Select', 'x0', 'x1(ra)', 'x2(sp)', 'x3(gp)', 'x4(tp)',\
             'x5(t0)', 'x6(t1)', 'x7(t2)','x8(s0)'])
        
        mem_refHlayout = QHBoxLayout()
        mem_refHlayout.addItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        mem_refHlayout.addWidget(self.mem_reflabel1)
        mem_refHlayout.addWidget(self.ref_typecombo)
        mem_refHlayout.addWidget(self.mem_reflabel2)
        mem_refHlayout.addWidget(self.ref_regcombo)
        mem_ref_hwg = QWidget()
        mem_ref_hwg.setLayout(mem_refHlayout)

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

        mem_titlelable2 = QLabel('Reference')
        title_Hlayout2 = QHBoxLayout()
        title_Hlayout2.addWidget(mem_titlelable2)
        title_Hlayout2.addItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        title_Hlayout2.addWidget(min_button2)
        title_Hlayout2.addWidget(max_button2)
        titile_widget2 = QWidget()
        titile_widget2.setLayout(title_Hlayout2)

        #table widget
        table_layout2 = QHBoxLayout()
        table_widget2 = QWidget()
        self.ref_tableWidget = QTableWidget()
        table_layout2.addWidget(self.ref_tableWidget)
        table_widget2.setLayout(table_layout2)
        self.ref_tableWidget.setRowCount(12904)
        self.ref_tableWidget.setColumnCount(9)
        self.ref_tableWidget.setHorizontalHeaderLabels(['Address', 'Word0', 'Word1', 'Word2', 'Word3', \
                                                                   'Word4', 'Word5', 'Word6', 'Word7'])
        self.ref_tableWidget.horizontalHeader().setStretchLastSection(True)
        self.ref_tableWidget.setShowGrid(False)
        self.ref_tableWidget.verticalHeader().setVisible(False)
        self.ref_tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        mem_refVlayout = QVBoxLayout()
        mem_refVlayout.addWidget(titile_widget2)
        mem_refVlayout.addWidget(table_widget2)
        mem_refVlayout.addWidget(mem_ref_hwg)
        mem_ref_scroll = QScrollArea()
        mem_ref_scroll.setLayout(mem_refVlayout)
        self.setWidget(mem_ref_scroll)

        mem_refVlayout.setContentsMargins(9,0,0,0)
        title_Hlayout2.setContentsMargins(0,2,4,0)
        table_layout2.setContentsMargins(0,9,9,0)
        
        max_button2.pressed.connect(self.maxshow)
        min_button2.pressed.connect(self.minshow)

    def maxshow(self):
        self.showMaximized()

    def minshow(self):
        self.showNormal()

    def display(self):
        # handle data
        memoryPath = self.clientView.settings.value("CLIENT/REF_Snapshot") + "/memsnapshot_hexdump_gem5.txt"

        with open(memoryPath) as f:
            content = f.read()
        f.close()
        content = content.split("\n")

        middleData = []
        deleteNum = ['0000', '0000', '0000', '0000', '0000', '0000', '0000', '0000']
        for i in range(len(content)):
            content[i] = list(filter(None, re.split(" |\t|\n|\r", content[i])))
            if content[i] == []:
                continue
            elif content[i][0] == "*":
                continue
            elif content[i][1:] == deleteNum:
                continue
            middleData.append(content[i])
        
        # display
        for i in range(self.ref_tableWidget.rowCount()):
            if i == self.ref_tableWidget.rowCount()-1:
                self.item_Addres = QTableWidgetItem(middleData[i][0])
                self.item_Addres.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.ref_tableWidget.setItem(i, 0, self.item_Addres)
                break
            else:
                self.item_Addres = QTableWidgetItem(middleData[i][0])
                self.item_Addres.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.ref_tableWidget.setItem(i, 0, self.item_Addres)

            self.item_Word0 = QTableWidgetItem(middleData[i][1])
            self.item_Word0.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.ref_tableWidget.setItem(i, 1, self.item_Word0)

            self.item_Word1 = QTableWidgetItem(middleData[i][2])
            self.item_Word1.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.ref_tableWidget.setItem(i, 2, self.item_Word1)

            self.item_Word2 = QTableWidgetItem(middleData[i][3])
            self.item_Word2.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.ref_tableWidget.setItem(i, 3, self.item_Word2)

            self.item_Word3 = QTableWidgetItem(middleData[i][4])
            self.item_Word3.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.ref_tableWidget.setItem(i, 4, self.item_Word3)

            self.item_Word4 = QTableWidgetItem(middleData[i][5])
            self.item_Word4.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.ref_tableWidget.setItem(i, 5, self.item_Word4)

            self.item_Word5 = QTableWidgetItem(middleData[i][6])
            self.item_Word5.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.ref_tableWidget.setItem(i, 6, self.item_Word5)

            self.item_Word6 = QTableWidgetItem(middleData[i][7])
            self.item_Word6.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.ref_tableWidget.setItem(i, 7, self.item_Word6)

            self.item_Word7 = QTableWidgetItem(middleData[i][8])
            self.item_Word7.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.ref_tableWidget.setItem(i, 8, self.item_Word7)
