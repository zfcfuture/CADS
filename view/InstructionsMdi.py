import sys
import re
from types import FrameType

from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import QBrush, QColor
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from ClientConfView import ClientConfView

class ISDUTsub(QMdiSubWindow):
    """
    DUT Instructions View
    """

    def __init__(self):

        super().__init__()

        self.clientView = ClientConfView()

        #isDUT_sub = QMdiSubWindow(self)
        is_dutlable = QLabel()
        is_dutlable.setText('View mode:')
        is_dutradio1 = QRadioButton()
        is_dutradio1.setText('Binary')
        is_dutradio2 = QRadioButton()
        is_dutradio2.setText('Disassembler')
        is_dutHlayout = QHBoxLayout()
        is_dutHlayout.addItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))  #水平弹簧
        is_dutHlayout.addWidget(is_dutlable)
        is_dutHlayout.addWidget(is_dutradio1)
        is_dutHlayout.addWidget(is_dutradio2)
        is_dut_hwg = QWidget()
        is_dut_hwg.setLayout(is_dutHlayout)

        #message
        table_layout1 = QHBoxLayout()
        self.is_dut_message = QTableWidget(31, 2)
        self.is_dut_message.setHorizontalHeaderLabels(["PC", "Instruction"])
        self.is_dut_message.horizontalHeader().setStretchLastSection(True)
        self.is_dut_message.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.is_dut_message.verticalHeader().setVisible(False)
        # self.is_dut_message.horizontalHeader().setVisible(False)
        self.is_dut_message.setShowGrid(False)
        table_widget1 = QWidget()
        table_layout1.addWidget(self.is_dut_message)
        table_widget1.setLayout(table_layout1)

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

        is_titlelable1 = QLabel('DUT')
        title_Hlayout1 = QHBoxLayout()
        title_Hlayout1.addWidget(is_titlelable1)
        title_Hlayout1.addItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        title_Hlayout1.addWidget(min_button1)
        title_Hlayout1.addWidget(max_button1)
        titile_widget1 = QWidget()
        titile_widget1.setLayout(title_Hlayout1)

        is_dutVlayout = QVBoxLayout()
        is_dutVlayout.addWidget(titile_widget1)
        is_dutVlayout.addWidget(is_dut_hwg)
        is_dutVlayout.addWidget(table_widget1)
        is_dut_scroll = QScrollArea()
        is_dut_scroll.setLayout(is_dutVlayout)
        self.setWidget(is_dut_scroll)

        is_dutVlayout.setContentsMargins(9,0,0,0)
        title_Hlayout1.setContentsMargins(0,2,4,0)
        table_layout1.setContentsMargins(0,0,9,9)
        is_dutHlayout.setContentsMargins(0,5,9,5)
        
        max_button1.pressed.connect(self.maxshow)
        min_button1.pressed.connect(self.minshow)

    def maxshow(self):
        self.showMaximized()

    def minshow(self):
        self.showNormal()

    def display(self, pc):
        pc = pc[2:]

        # handle data
        filePath = self.clientView.settings.value("CLIENT/RefELF") + "/cputest.bare.haps.dis"
        with open(filePath) as f:
            content = f.read()
        content = content.split("\n")
        for i in range(len(content)):
            if i >= len(content):
                break
            content[i] = content[i].strip()
            content[i].replace(" ", "").replace("\t", "").replace("\r", "").replace("\n", "")
            if len(content[i]) == 0:
                del content[i]
        
        for i in range(len(content)):
            if i >= len(content):
                break
            content[i] = content[i].strip(" \n\t\r")
            if len(content[i]) > 0 and (not content[i][0].isdigit()):
                del content[i]

        middleList = []
        for i in range(len(content)):
            content[i] = [x for x in re.split(" |\t|\n|\r", content[i].strip())]
            content[i] = list(filter(None, content[i]))
            if len(content[i]) != 0 and content[i][0][0].isdigit():
                middleList.append(content[i])

        # get key information
        keyList = []
        for i in range(len(middleList)):
            if len(middleList[i][0][:-1]) == 8:
                if pc == middleList[i][0][:-1]:
                    keyList = middleList[i-10:i] + [middleList[i]] + middleList[i:i+21]
        
        # display on the instruction table
        for i in range(31):
            self.item_pc = QTableWidgetItem(keyList[i][0][:-1])
            self.item_pc.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.is_dut_message.setItem(i, 0, self.item_pc)
            self.item_ins = QTableWidgetItem(keyList[i][2]+"  "+keyList[i][3])
            self.item_ins.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.is_dut_message.setItem(i, 1, self.item_ins)
            if i == 10:
                self.is_dut_message.item(10, 0).setBackground(QBrush(QColor(240, 128, 128)))
                self.is_dut_message.item(10, 1).setBackground(QBrush(QColor(240, 128, 128)))


class ISREFsub(QMdiSubWindow):
    """
    Reference Instructions View
    """
    
    def __init__(self):

        super().__init__()

        self.clientView = ClientConfView()

        #isREF_sub = QMdiSubWindow(self)
        is_reflable = QLabel()
        is_reflable.setText('View mode:')
        is_refradio1 = QRadioButton()
        is_refradio1.setText('Binary')
        is_refradio2 = QRadioButton()
        is_refradio2.setText('Disassembler')
        is_refHlayout = QHBoxLayout()
        is_refHlayout.addItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))  #水平弹簧
        is_refHlayout.addWidget(is_reflable)
        is_refHlayout.addWidget(is_refradio1)
        is_refHlayout.addWidget(is_refradio2)
        is_ref_hwg = QWidget()
        is_ref_hwg.setLayout(is_refHlayout)

        #message
        table_layout2 = QHBoxLayout()
        self.is_ref_message = QTableWidget(31, 2)
        self.is_ref_message.setHorizontalHeaderLabels(["PC", "Instruction"])
        self.is_ref_message.horizontalHeader().setStretchLastSection(True)
        self.is_ref_message.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.is_ref_message.verticalHeader().setVisible(False)
        # self.is_dut_message.horizontalHeader().setVisible(False)
        self.is_ref_message.setShowGrid(False)
        table_widget2 = QWidget()
        table_layout2.addWidget(self.is_ref_message)
        table_widget2.setLayout(table_layout2)

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

        is_titlelable2 = QLabel('Reference')
        title_Hlayout2 = QHBoxLayout()
        title_Hlayout2.addWidget(is_titlelable2)
        title_Hlayout2.addItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        title_Hlayout2.addWidget(min_button2)
        title_Hlayout2.addWidget(max_button2)
        titile_widget2 = QWidget()
        titile_widget2.setLayout(title_Hlayout2)

        is_refVlayout = QVBoxLayout()
        is_refVlayout.addWidget(titile_widget2)
        is_refVlayout.addWidget(is_ref_hwg)
        is_refVlayout.addWidget(table_widget2)
        is_ref_scroll = QScrollArea()
        is_ref_scroll.setLayout(is_refVlayout)
        self.setWidget(is_ref_scroll)

        is_refVlayout.setContentsMargins(9,0,0,0)
        title_Hlayout2.setContentsMargins(0,2,4,0)
        table_layout2.setContentsMargins(0,0,9,9)
        is_refHlayout.setContentsMargins(0,5,9,5)
        
        max_button2.pressed.connect(self.maxshow)
        min_button2.pressed.connect(self.minshow)

    def maxshow(self):
        self.showMaximized()

    def minshow(self):
        self.showNormal()

    def display(self, pc):
        pc = pc[2:]

        # handle data
        filePath = self.clientView.settings.value("CLIENT/RefELF") + "/cputest.bare.haps.dis"
        with open(filePath) as f:
            content = f.read()
        content = content.split("\n")
        for i in range(len(content)):
            if i >= len(content):
                break
            content[i] = content[i].strip()
            content[i].replace(" ", "").replace("\t", "").replace("\r", "").replace("\n", "")
            if len(content[i]) == 0:
                del content[i]
        
        for i in range(len(content)):
            if i >= len(content):
                break
            content[i] = content[i].strip(" \n\t\r")
            if len(content[i]) > 0 and (not content[i][0].isdigit()):
                del content[i]

        middleList = []
        for i in range(len(content)):
            content[i] = [x for x in re.split(" |\t|\n|\r", content[i].strip())]
            content[i] = list(filter(None, content[i]))
            if len(content[i]) != 0 and content[i][0][0].isdigit():
                middleList.append(content[i])

        # get key information
        keyList = []
        for i in range(len(middleList)):
            if len(middleList[i][0][:-1]) == 8:
                if pc == middleList[i][0][:-1]:
                    keyList = middleList[i-10:i] + [middleList[i]] + middleList[i:i+21]
        
        # display on the instruction table
        for i in range(31):
            self.item_pc = QTableWidgetItem(keyList[i][0][:-1])
            self.item_pc.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.is_ref_message.setItem(i, 0, self.item_pc)
            self.item_ins = QTableWidgetItem(keyList[i][2]+"  "+keyList[i][3])
            self.item_ins.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.is_ref_message.setItem(i, 1, self.item_ins)
            if i == 10:
                self.is_ref_message.item(10, 0).setBackground(QBrush(QColor(240, 128, 128)))
                self.is_ref_message.item(10, 1).setBackground(QBrush(QColor(240, 128, 128)))