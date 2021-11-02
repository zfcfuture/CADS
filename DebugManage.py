import sys

from PyQt5 import uic
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSettings, Qt
from PyQt5.QtWidgets import QApplication, QLabel, QComboBox, QMessageBox, QHeaderView, QFileDialog

from ServerConfView import ServerConfView
from ClientConfView import ClientConfView
from SnapshotImportView import SnapshotImportView
from SnapshotExportView import SnapshotExportView
from SnapshotCompareView import SnapshotCompareView
from InstructionsView import ISREFView, ISDUTView
from RegisterView import RegisterREFView, RegisterDUTView
from MemoryView import MemoryREFView, MemoryDUTView

class DebugManage:
    """
    CPU Auto Debug System GUI
    """

    def __init__(self):
        """ load views """
        self.serverView = ServerConfView()
        self.clientView = ClientConfView()
        self.importView = SnapshotImportView()
        self.exportView = SnapshotExportView()
        self.compareView = SnapshotCompareView()

        self.ISREFView = ISREFView()
        self.ISDUTView = ISDUTView()
        self.RegREFView = RegisterREFView()
        self.RegDUTView = RegisterDUTView()
        self.MemREFView = MemoryREFView()
        self.MemDUTView = MemoryDUTView()

        self.init()

    def init(self):
        """ load all UI """
        # load main ui
        self.main_ui = uic.loadUi("ui/manageV0.1.ui")
        self.main_ui.setWindowTitle("CPU Auto Debug System")
        self.main_ui.move(500, 200)

        """ add widget for main ui """
        # add widget for reference and DUT [Instruction, Register, Memory]
        self.main_ui.REF_layout.addWidget(self.ISREFView.ISREF_ui)
        self.main_ui.DUT_layout.addWidget(self.ISDUTView.ISDUT_ui)
        self.main_ui.REF_layout.addWidget(self.RegREFView.RegREF_ui)
        self.main_ui.DUT_layout.addWidget(self.RegDUTView.RegDUT_ui)
        self.main_ui.REF_layout.addWidget(self.MemREFView.MemREF_ui)
        self.main_ui.DUT_layout.addWidget(self.MemDUTView.MemDUT_ui)

        # add widget for statusbar
        self.main_ui.link_status = QLabel('{:<40}'.format('链接状态：'))
        self.main_ui.run_status = QLabel('{:<40}'.format('运行状态：'))
        self.main_ui.health_status = QLabel('{:<40}'.format('当前健康状态：'))
        self.main_ui.harttext_status = QLabel('{:<0}'.format('当前hart：'))
        self.main_ui.hart_status = QComboBox()
        self.main_ui.pc_status = QLabel('{:<40}'.format('PC：'))
        self.main_ui.hart_status.addItems(['hart0'])
        self.main_ui.statusbar.addWidget(self.main_ui.link_status, 1)
        self.main_ui.statusbar.addWidget(self.main_ui.run_status, 1)
        self.main_ui.statusbar.addWidget(self.main_ui.health_status, 1)
        self.main_ui.statusbar.addWidget(self.main_ui.harttext_status)
        self.main_ui.statusbar.addWidget(self.main_ui.hart_status)
        self.main_ui.statusbar.addWidget(self.main_ui.pc_status, 1)

        """ connect signal and slot """
        # signal and slot for main ui
        self.main_ui.Main_button.clicked.connect(self.intoMainView)
        self.main_ui.IS_button.clicked.connect(self.intoInstructionView)
        self.main_ui.Reg_button.clicked.connect(self.intoRegisterView)
        self.main_ui.Mem_button.clicked.connect(self.intoMemoryView)
        self.main_ui.serviceButton.clicked.connect(self.showServer)
        self.main_ui.clientButton.clicked.connect(self.showClient)
        self.main_ui.importButton.clicked.connect(self.showImport)
        self.main_ui.exportButton.clicked.connect(self.showExport)
        self.main_ui.compareButton.clicked.connect(self.showCompare)

    def intoMainView(self):
        self.main_ui.REF_widget.show()
        self.main_ui.DUT_widget.show()
        self.ISREFView.ISREF_ui.hide()
        self.ISDUTView.ISDUT_ui.hide()
        self.RegREFView.RegREF_ui.hide()
        self.RegDUTView.RegDUT_ui.hide()
        self.MemREFView.MemREF_ui.hide()
        self.MemDUTView.MemDUT_ui.hide()

    def intoInstructionView(self):
        self.ISREFView.ISREF_ui.show()
        self.ISDUTView.ISDUT_ui.show()
        self.RegREFView.RegREF_ui.hide()
        self.RegDUTView.RegDUT_ui.hide()
        self.MemREFView.MemREF_ui.hide()
        self.MemDUTView.MemDUT_ui.hide()
        self.main_ui.REF_widget.hide()
        self.main_ui.DUT_widget.hide()

    def intoRegisterView(self):
        self.RegREFView.RegREF_ui.show()
        self.RegDUTView.RegDUT_ui.show()
        self.ISREFView.ISREF_ui.hide()
        self.ISDUTView.ISDUT_ui.hide()
        self.MemREFView.MemREF_ui.hide()
        self.MemDUTView.MemDUT_ui.hide()
        self.main_ui.REF_widget.hide()
        self.main_ui.DUT_widget.hide()

    def intoMemoryView(self):
        self.MemREFView.MemREF_ui.show()
        self.MemDUTView.MemDUT_ui.show()
        self.RegREFView.RegREF_ui.hide()
        self.RegDUTView.RegDUT_ui.hide()
        self.ISREFView.ISREF_ui.hide()
        self.ISDUTView.ISDUT_ui.hide()
        self.main_ui.REF_widget.hide()
        self.main_ui.DUT_widget.hide()

    def showServer(self):
        self.serverView.server_ui.show()

    def showClient(self):
        self.clientView.client_ui.show()

    def showImport(self):
        self.importView.import_ui.show()

    def showExport(self):
        self.exportView.export_ui.show()

    def showCompare(self):
        self.compareView.compare_ui.show()

if __name__ == "__main__":
    with open('app.qss', encoding='utf-8') as f:
        qss = f.read()
    app = QApplication(sys.argv)
    app.setStyleSheet(qss)
    gui = DebugManage()
    gui.main_ui.setWindowIcon(QIcon('imgs/block.png'))
    gui.main_ui.show()
    sys.exit(app.exec_())
