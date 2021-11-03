import sys

from PyQt5 import uic
from PyQt5.QtCore import QSettings, Qt

class SnapshotExportView:
    """
    Snapshot Export View
    """
    
    def __init__(self) -> None:
        self.init()

    def init(self):
        # load snapshot-export ui and settings
        self.export_ui = uic.loadUi("ui/export.ui")
        self.export_ui.setWindowTitle("Export Snapshot")
        self.export_ui.move(800, 400)
        self.export_ui.setWindowFlags(Qt.WindowStaysOnTopHint)