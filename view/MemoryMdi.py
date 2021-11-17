import sys

from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class MEMDUTsub(QMdiSubWindow):

    """
    DUT Mem Date View
    """
    def __init__(self):
        super().__init__()
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
        self.dut_tableWidget.setColumnCount(5)
        self.dut_tableWidget.setHorizontalHeaderLabels(['Address', 'Word', 'Byte0', 'Byte1', 'Byte2'])
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

class MEMREFsub(QMdiSubWindow):

    """
    Reference Mem Date View
    """
    def __init__(self):
        super().__init__()
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
        self.ref_tableWidget.setColumnCount(5)
        self.ref_tableWidget.setHorizontalHeaderLabels(['Address', 'Word', 'Byte0', 'Byte1', 'Byte2'])
        self.ref_tableWidget.horizontalHeader().setStretchLastSection(True)
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
