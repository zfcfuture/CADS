import sys

from PyQt5 import uic
from PyQt5.QtCore import Qt

class RegisterREFView:
    """
    Reference Register View
    """

    def __init__(self):
        self.RegREF_ui = uic.loadUi("ui/Reg_REF.ui")
        self.RegREF_ui.hide()

    def display(self):
        # get data
        regData = []

    def getData(self):
        pass


class RegisterDUTView:
    """
    DUT Register View
    """

    def __init__(self):
        self.RegDUT_ui = uic.loadUi("ui/Reg_DUT.ui")
        self.RegDUT_ui.hide()

    def display(self):
        # get data
        regData = []

    def getData(self):
        pass