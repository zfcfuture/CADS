import sys

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class ISDUTsub(QMdiSubWindow):
    """
    DUT Instructions View
    """

    def __init__(self):
        super().__init__()
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

        is_dut_message = QTableWidget()
        is_dutVlayout = QVBoxLayout()
        is_titlelable1 = QLabel()
        is_titlelable1.setText('DUT')
        is_dutVlayout.addWidget(is_titlelable1)
        is_dutVlayout.addWidget(is_dut_hwg)
        is_dutVlayout.addWidget(is_dut_message)
        is_dut_vwg = QWidget()
        is_dut_vwg.setLayout(is_dutVlayout)
        self.setWidget(is_dut_vwg)


class ISREFsub(QMdiSubWindow):
    """
    Reference Instructions View
    """
    
    def __init__(self):
        super().__init__()
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

        is_ref_message = QTableWidget()
        is_refVlayout = QVBoxLayout()
        is_titlelable2 = QLabel()
        is_titlelable2.setText('Reference')
        is_refVlayout.addWidget(is_titlelable2)
        is_refVlayout.addWidget(is_ref_hwg)
        is_refVlayout.addWidget(is_ref_message)
        is_ref_vwg = QWidget()
        is_ref_vwg.setLayout(is_refVlayout)
        self.setWidget(is_ref_vwg)