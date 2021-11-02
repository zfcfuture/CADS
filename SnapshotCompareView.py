import sys

from PyQt5 import uic
from PyQt5.QtCore import QSettings, Qt

class SnapshotCompareView:
    """
    Snapshot Compare Report View
    """
    
    def __init__(self) -> None:
        self.init()

    def init(self):
        # load snapshot compare report ui and settings
        self.compare_ui = uic.loadUi("ui/compare.ui")
        self.compare_ui.setWindowTitle("Snapshot Compare Report")
        self.compare_ui.move(800, 400)
        self.compare_ui.setWindowFlags(Qt.WindowStaysOnTopHint)