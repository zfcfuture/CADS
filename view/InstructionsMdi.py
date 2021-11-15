import sys

from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class ISDUTsub(QMdiSubWindow):
    """
    DUT Instructions View
    """

    def __init__(self):
        super().__init__()
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
        is_dut_message = QTableWidget()
        table_widget1 = QWidget()
        table_layout1.addWidget(is_dut_message)
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
        title_Hlayout1 = QHBoxLayout()
        title_Hlayout1.addItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        title_Hlayout1.addWidget(min_button1)
        title_Hlayout1.addWidget(max_button1)
        titile_widget1 = QWidget()
        titile_widget1.setLayout(title_Hlayout1)

        is_dutVlayout = QVBoxLayout()
        is_titlelable1 = QLabel()
        is_titlelable1.setText('DUT')
        is_dutVlayout.addWidget(titile_widget1)
        is_dutVlayout.addWidget(is_titlelable1)
        is_dutVlayout.addWidget(is_dut_hwg)
        is_dutVlayout.addWidget(table_widget1)
        is_dut_scroll = QScrollArea()
        is_dut_scroll.setLayout(is_dutVlayout)
        self.setWidget(is_dut_scroll)

        is_dutVlayout.setContentsMargins(9,0,0,0)
        title_Hlayout1.setContentsMargins(0,2,4,0)
        table_layout1.setContentsMargins(0,0,9,9)
        is_dutHlayout.setContentsMargins(0,0,9,0)
        
        max_button1.pressed.connect(self.maxshow)
        min_button1.pressed.connect(self.minshow)

    def maxshow(self):
        self.showMaximized()

    def minshow(self):
        self.showNormal()


class ISREFsub(QMdiSubWindow):
    """
    Reference Instructions View
    """
    
    def __init__(self):
        super().__init__()
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
        is_ref_message = QTableWidget()
        table_widget2 = QWidget()
        table_layout2.addWidget(is_ref_message)
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
        title_Hlayout2 = QHBoxLayout()
        title_Hlayout2.addItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        title_Hlayout2.addWidget(min_button2)
        title_Hlayout2.addWidget(max_button2)
        titile_widget2 = QWidget()
        titile_widget2.setLayout(title_Hlayout2)

        is_refVlayout = QVBoxLayout()
        is_titlelable1 = QLabel()
        is_titlelable1.setText('Reference')
        is_refVlayout.addWidget(titile_widget2)
        is_refVlayout.addWidget(is_titlelable1)
        is_refVlayout.addWidget(is_ref_hwg)
        is_refVlayout.addWidget(table_widget2)
        is_ref_scroll = QScrollArea()
        is_ref_scroll.setLayout(is_refVlayout)
        self.setWidget(is_ref_scroll)

        is_refVlayout.setContentsMargins(9,0,0,0)
        title_Hlayout2.setContentsMargins(0,2,4,0)
        table_layout2.setContentsMargins(0,0,9,9)
        is_refHlayout.setContentsMargins(0,0,9,0)
        
        max_button2.pressed.connect(self.maxshow)
        min_button2.pressed.connect(self.minshow)

    def maxshow(self):
        self.showMaximized()

    def minshow(self):
        self.showNormal()