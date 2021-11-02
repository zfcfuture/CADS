import sys

from PyQt5 import uic
from PyQt5.QtCore import QSettings, Qt

class SnapshotImportView:
    """
    Snapshot Import View
    """

    def __init__(self):
        self.init()

    def init(self):
        # load snapshot-import ui and settings
        self.import_ui = uic.loadUi("ui/import.ui")
        self.import_ui.setWindowTitle("Import Snapshot")
        self.import_ui.move(800, 400)
        self.import_ui.setWindowFlags(Qt.WindowStaysOnTopHint)