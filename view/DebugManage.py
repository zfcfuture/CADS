import sys

from PyQt5 import uic, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QApplication, QLabel, QComboBox, QPushButton, QTableWidget, QAbstractItemView,
                             QTableWidgetItem, QHeaderView, QFileDialog)

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
        self.main_ui.move(250, 150)

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

        # add load-table and load-button for main ui
        self.taskTable = TableWidget(3, 2)
        self.main_ui.LoadLayout.addWidget(self.taskTable, 0, 0, 10, 15)
        self.spaceLable = QLabel()
        self.main_ui.LoadLayout.addWidget(self.spaceLable, 10, 15, 0, 1)
        self.loadButton = QPushButton()
        self.loadButton.setText('加载')
        self.main_ui.LoadLayout.addWidget(self.loadButton, 9, 16, 1, 1)

        self.taskTable.setHorizontalHeaderLabels(['Check', '任务名'])
        self.taskTable.horizontalHeader().setStretchLastSection(True)
        self.taskTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.taskTable.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        # self.taskTable.setColumnWidth(0, self.main_ui.groupBox_3.width()*1.8)

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

        self.main_ui.compile_Button.clicked.connect(self.handleCompile)
        self.loadButton.clicked.connect(self.handleLoadELF)

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

    def handleCompile(self):
        # Temporarily used to load local ELF-files to taskTable
        self.ELF_files_path, _ = QFileDialog.getOpenFileNames(self.main_ui,'选择文件')
        
        if len(self.ELF_files_path) == 0:
            return

        files = [x.split("/")[-1] for x in self.ELF_files_path]

        cur_rows = self.taskTable.rowCount()
        rows_flag = 0
        for file in files:
            if rows_flag >= cur_rows:
                self.taskTable.insertRow(cur_rows)
                # add contents to the new row
                # first column:check states   second column:file name
                self.item_check = QTableWidgetItem()
                self.item_check.setCheckState(QtCore.Qt.Unchecked)
                self.item_check.setText('check')
                self.taskTable.setItem(rows_flag, 0, self.item_check)
                self.item_filename = QTableWidgetItem(file)
                self.item_filename.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.taskTable.setItem(rows_flag, 1, self.item_filename)
            else:
                self.item_check = QTableWidgetItem()
                self.item_check.setCheckState(QtCore.Qt.Unchecked)
                self.item_check.setText('check')
                self.taskTable.setItem(rows_flag, 0, self.item_check)
                self.item_filename = QTableWidgetItem(file)
                self.item_filename.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.taskTable.setItem(rows_flag, 1, self.item_filename)
                rows_flag += 1

    def handleLoadELF(self):
        """ load the checked ELF-file to host PC """
        

class TableWidget(QTableWidget):
    """
    Overwrite QTableWidget
    purpose: drag and drop table to trigger the dropEvent
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.viewport().setAcceptDrops(True)
        self.setDragDropOverwriteMode(False)
        self.setDropIndicatorShown(True)

        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        # Select by unit of item
        self.setSelectionBehavior(QAbstractItemView.SelectItems)
        # Internal drag and drop is allowed
        self.setDragDropMode(QAbstractItemView.InternalMove)

    def dropEvent(self, event):
        # get mouse released positon and it's corrospond QTableWidgetItem
        item = self.itemAt(event.pos())
        self.swapTwoRow(self.currentRow(), item.row())

    def swapTwoRow(self, selectRow, targetRow):
        # lists[0]: select row  lists[1]: target row
        lists = [[] for _ in range(2)]
        # preserve two rows's content
        lists[0].append(self.item(selectRow, 1).text())
        lists[1].append(self.item(targetRow, 1).text())
        # set text
        self.lists1_item = QTableWidgetItem(lists[1][0])
        self.lists0_item = QTableWidgetItem(lists[0][0])
        self.lists1_item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.lists0_item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.setItem(selectRow, 1, self.lists1_item)
        self.setItem(targetRow, 1, self.lists0_item)

if __name__ == "__main__":
    with open('view/app.qss', encoding='utf-8') as f:
        qss = f.read()
    app = QApplication(sys.argv)
    app.setStyleSheet(qss)
    gui = DebugManage()
    gui.main_ui.setWindowIcon(QIcon('imgs/block.png'))
    gui.main_ui.show()
    sys.exit(app.exec_())