import sys

from PyQt5 import uic
from PyQt5.QtCore import Qt

class ISREFView:
    """
    Reference Instructions View
    """

    def __init__(self):
        self.ISREF_ui = uic.loadUi("ui/IS_REF.ui")
        self.ISREF_ui.hide()


class ISDUTView:
    """
    Reference Instructions View
    """
    
    def __init__(self):
        self.ISDUT_ui = uic.loadUi("ui/IS_DUT.ui")
        self.ISDUT_ui.hide()