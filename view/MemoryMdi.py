import sys

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class MEMDUTsub(QMdiSubWindow):

    """
    DUT Mem Date View
    """
    def __init__(self):
        super().__init__()
        mem_dutlabel1 = QLabel()
        mem_dutlabel2 = QLabel()
        mem_dutlabel1.setText('Display type:')
        mem_dutlabel2.setText('Go to register:')
        dut_typecombo = QComboBox()
        dut_regcombo = QComboBox()
        dut_typecombo.addItems(['Hex', 'Binary', 'Unsigned', 'Signed', 'ASCⅡ', 'Float'])
        dut_regcombo.addItems(['Select', 'x0', 'x1(ra)', 'x2(sp)', 'x3(gp)', 'x4(tp)',\
             'x5(t0)', 'x6(t1)', 'x7(t2)','x8(s0)'])
        
        mem_dutHlayout = QHBoxLayout()
        mem_dutHlayout.addItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        mem_dutHlayout.addWidget(mem_dutlabel1)
        mem_dutHlayout.addWidget(dut_typecombo)
        mem_dutHlayout.addWidget(mem_dutlabel2)
        mem_dutHlayout.addWidget(dut_regcombo)
        mem_dut_hwg = QWidget()
        mem_dut_hwg.setLayout(mem_dutHlayout)

        mem_dut_tableWidget = QTableWidget()
        mem_dut_tableWidget.setColumnCount(5)
        mem_dut_tableWidget.setHorizontalHeaderLabels(['Address', 'Word', 'Byte0', 'Byte1', 'Byte2'])
        mem_dut_tableWidget.horizontalHeader().setStretchLastSection(True)
        mem_dut_tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        mem_titlelable1 = QLabel()
        mem_titlelable1.setText('DUT')
        mem_dutVlayout = QVBoxLayout()
        mem_dutVlayout.addWidget(mem_titlelable1)
        mem_dutVlayout.addWidget(mem_dut_tableWidget)
        mem_dutVlayout.addWidget(mem_dut_hwg)
        mem_dut_vwg = QWidget()
        mem_dut_vwg.setLayout(mem_dutVlayout)
        self.setWidget(mem_dut_vwg)

class MEMREFsub(QMdiSubWindow):

    """
    Reference Mem Date View
    """
    def __init__(self):
        super().__init__()
        mem_reflabel1 = QLabel()
        mem_reflabel2 = QLabel()
        mem_reflabel1.setText('Display type:')
        mem_reflabel2.setText('Go to register:')
        ref_typecombo = QComboBox()
        ref_regcombo = QComboBox()
        ref_typecombo.addItems(['Hex', 'Binary', 'Unsigned', 'Signed', 'ASCⅡ', 'Float'])
        ref_regcombo.addItems(['Select', 'x0', 'x1(ra)', 'x2(sp)', 'x3(gp)', 'x4(tp)',\
             'x5(t0)', 'x6(t1)', 'x7(t2)','x8(s0)'])
        
        mem_refHlayout = QHBoxLayout()
        mem_refHlayout.addItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        mem_refHlayout.addWidget(mem_reflabel1)
        mem_refHlayout.addWidget(ref_typecombo)
        mem_refHlayout.addWidget(mem_reflabel2)
        mem_refHlayout.addWidget(ref_regcombo)
        mem_ref_hwg = QWidget()
        mem_ref_hwg.setLayout(mem_refHlayout)

        mem_ref_tableWidget = QTableWidget()
        mem_ref_tableWidget.setColumnCount(5)
        mem_ref_tableWidget.setHorizontalHeaderLabels(['Address', 'Word', 'Byte0', 'Byte1', 'Byte2'])
        mem_ref_tableWidget.horizontalHeader().setStretchLastSection(True)
        mem_ref_tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        mem_titlelable2 = QLabel()
        mem_titlelable2.setText('Reference')
        mem_refVlayout = QVBoxLayout()
        mem_refVlayout.addWidget(mem_titlelable2)
        mem_refVlayout.addWidget(mem_ref_tableWidget)
        mem_refVlayout.addWidget(mem_ref_hwg)
        mem_ref_vwg = QWidget()
        mem_ref_vwg.setLayout(mem_refVlayout)
        self.setWidget(mem_ref_vwg)