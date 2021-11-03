import sys

from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHeaderView

class MemoryREFView:
    """
    Reference Memory View
    """

    def __init__(self):
        self.MemREF_ui = uic.loadUi("ui/Mem_REF.ui")
        self.MemREF_ui.hide()
        self.MemREF_ui.Mem_REF_tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

class MemoryDUTView:
    """
    DUT Memory View
    """

    def __init__(self):
        self.MemDUT_ui = uic.loadUi("ui/Mem_DUT.ui")
        self.MemDUT_ui.hide()
        self.MemDUT_ui.Mem_DUT_tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
