import sys

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class REGDUTsub(QMdiSubWindow):

    """
    DUT Registers View
    """
    def __init__(self):

        super().__init__()
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

        reg_dut_tabWidget = QTabWidget()
        dut_GPR_tab = QWidget()
        dut_FPR_tab = QWidget()
        dut_CSR_tab = QWidget()
        reg_dut_tabWidget.addTab(dut_GPR_tab, "")
        reg_dut_tabWidget.addTab(dut_FPR_tab, "")
        reg_dut_tabWidget.addTab(dut_CSR_tab, "")
        reg_dut_tabWidget.setTabText(0, 'GPR')
        reg_dut_tabWidget.setTabText(1, 'FPR')
        reg_dut_tabWidget.setTabText(2, 'CSR')
        self.GPR_tabUI()
        self.FPR_tabUI()
        self.CSR_tabUI()

        reg_titlelable1 = QLabel()
        reg_titlelable1.setText('DUT')
        reg_dutVlayout = QVBoxLayout()
        reg_dutVlayout.addWidget(reg_titlelable1)
        reg_dutVlayout.addWidget(reg_dut_tabWidget)
        reg_dutVlayout.addWidget(reg_dut_hwg)
        reg_dut_vwg = QWidget()
        reg_dut_vwg.setLayout(reg_dutVlayout)
        self.setWidget(reg_dut_vwg)

    def GPR_tabUI(self):
        
        pass

    def FPR_tabUI(self):
        
        pass

    def CSR_tabUI(self):
        
        pass

class REGREFsub(QMdiSubWindow):

    """
    Reference Registers View
    """
    def __init__(self):
        super().__init__()
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

        reg_ref_tabWidget = QTabWidget()
        ref_GPR_tab = QWidget()
        ref_FPR_tab = QWidget()
        ref_CSR_tab = QWidget()
        reg_ref_tabWidget.addTab(ref_GPR_tab, "")
        reg_ref_tabWidget.addTab(ref_FPR_tab, "")
        reg_ref_tabWidget.addTab(ref_CSR_tab, "")
        reg_ref_tabWidget.setTabText(0, 'GPR')
        reg_ref_tabWidget.setTabText(1, 'FPR')
        reg_ref_tabWidget.setTabText(2, 'CSR')
        self.GPR_tabUI()
        self.FPR_tabUI()
        self.CSR_tabUI()

        reg_titlelable2 = QLabel()
        reg_titlelable2.setText('Reference')
        reg_refVlayout = QVBoxLayout()
        reg_refVlayout.addWidget(reg_titlelable2)
        reg_refVlayout.addWidget(reg_ref_tabWidget)
        reg_refVlayout.addWidget(reg_ref_hwg)
        reg_ref_vwg = QWidget()
        reg_ref_vwg.setLayout(reg_refVlayout)
        self.setWidget(reg_ref_vwg)

    def GPR_tabUI(self):
        
        pass

    def FPR_tabUI(self):
        
        pass

    def CSR_tabUI(self):
        
        pass