import os
import sys

import paramiko
from pexpect import *

from PyQt5 import uic, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *

from ServerConfView import ServerConfView
from ClientConfView import ClientConfView
from SnapshotImportView import SnapshotImportView
from SnapshotExportView import SnapshotExportView
from SnapshotCompareView import SnapshotCompareView
from InstructionsMdi import ISDUTsub, ISREFsub
from RegisterMdi import REGDUTsub, REGREFsub
from MemoryMdi import MEMDUTsub, MEMREFsub
from manage import Ui_MainWindow

class DebugManage(QMainWindow, Ui_MainWindow):
    """
    CPU Auto Debug System GUI
    """

    resized = QtCore.pyqtSignal()
    
    def __init__(self, parent=None):
        super(DebugManage, self).__init__(parent=parent)
        self.setupUi(self)

        self.IS_button.clicked.connect(self.display)
        self.Reg_button.clicked.connect(self.display)
        self.Mem_button.clicked.connect(self.display)
        self.resized.connect(self.refresh)

        """ load views """
        self.serverView = ServerConfView()
        self.clientView = ClientConfView()
        self.importView = SnapshotImportView()
        self.exportView = SnapshotExportView()
        self.compareView = SnapshotCompareView()

        self.init()
        self.startFlag = 0

    def init(self):
        """ load all UI """
        # load main ui
        self.setWindowTitle("CPU Auto Debug System")
        self.move(250, 150)

        """ add widget for main ui """
        #add mdiArea and subwindow
        self.is_mdi = QMdiArea()
        self.reg_mdi = QMdiArea()
        self.mem_mdi = QMdiArea()

        self.is_mdiUI()
        self.reg_mdiUI()
        self.mem_mdiUI()

        self.stack=QStackedWidget()

        self.stack.addWidget(self.is_mdi)
        self.stack.addWidget(self.reg_mdi)
        self.stack.addWidget(self.mem_mdi)
        self.mdiLayout.addWidget(self.stack)

        # add widget for statusbar
        self.link_status = QLabel('{:<40}'.format('连接状态：'))
        self.run_status = QLabel('{:<40}'.format('运行状态：'))
        self.health_status = QLabel('{:<40}'.format('当前健康状态：'))
        self.harttext_status = QLabel('{:<0}'.format('当前hart：'))
        self.hart_status = QComboBox()
        self.pc_status = QLabel('{:<40}'.format('PC：'))
        self.hart_status.addItems(['hart0'])
        self.statusbar.addWidget(self.link_status, 1)
        self.statusbar.addWidget(self.run_status, 1)
        self.statusbar.addWidget(self.health_status, 1)
        self.statusbar.addWidget(self.harttext_status)
        self.statusbar.addWidget(self.hart_status)
        self.statusbar.addWidget(self.pc_status, 1)

        # add load-table and load-button for main ui
        self.taskTable = TableWidget(3, 2)
        self.LoadLayout.addWidget(self.taskTable, 0, 0, 10, 12)
        self.spaceLable = QLabel()
        self.LoadLayout.addWidget(self.spaceLable, 10, 12, 0, 1)
        self.loadButton = QPushButton()
        self.loadButton.setText('加载')
        self.LoadLayout.addWidget(self.loadButton, 9, 13, 1, 1)
        self.trunButton = QPushButton()
        self.trunButton.setText('清空')
        self.LoadLayout.addWidget(self.trunButton, 8, 13, 1, 1)

        self.taskTable.setHorizontalHeaderLabels(['Check', '任务名'])
        self.taskTable.horizontalHeader().setStretchLastSection(True)
        self.taskTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.taskTable.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        # self.taskTable.setColumnWidth(0, self.main_ui.groupBox_3.width()*1.8)

        """ connect signal and slot """
        # signal and slot for main ui
        self.IS_button.clicked.connect(self.display)
        self.Reg_button.clicked.connect(self.display)
        self.Mem_button.clicked.connect(self.display)
        
        self.serviceButton.clicked.connect(self.showServer)
        self.clientButton.clicked.connect(self.showClient)
        self.importButton.clicked.connect(self.showImport)
        self.exportButton.clicked.connect(self.showExport)
        self.compareButton.clicked.connect(self.showCompare)

        self.compileButton.clicked.connect(self.handleCompile)
        self.testButton.clicked.connect(self.handleStartTest)
        self.routeButton.clicked.connect(self.handleRouteSelect)
        self.trunButton.clicked.connect(self.handleTruncate)
        self.loadButton.clicked.connect(self.handleLoadELF)
        self.resized.connect(self.refresh)

    def is_mdiUI(self):

        isDUT_sub = ISDUTsub()
        self.is_mdi.addSubWindow(isDUT_sub)

        isREF_sub = ISREFsub()
        self.is_mdi.addSubWindow(isREF_sub)

        isREF_sub.setWindowFlags(QtCore.Qt.WindowMaximizeButtonHint)
        isDUT_sub.setWindowFlags(QtCore.Qt.WindowMaximizeButtonHint)
        
        self.is_mdi.tileSubWindows()
    
    def reg_mdiUI(self):

        regDUT_sub = REGDUTsub()
        self.reg_mdi.addSubWindow(regDUT_sub)
        
        regREF_sub = REGREFsub()
        self.reg_mdi.addSubWindow(regREF_sub)

        regREF_sub.setWindowFlags(QtCore.Qt.WindowMaximizeButtonHint)
        regDUT_sub.setWindowFlags(QtCore.Qt.WindowMaximizeButtonHint)
        
        self.reg_mdi.tileSubWindows()

    def mem_mdiUI(self):
        
        memDUT_sub = MEMDUTsub()
        self.mem_mdi.addSubWindow(memDUT_sub)

        memREF_sub = MEMREFsub()
        self.mem_mdi.addSubWindow(memREF_sub)

        memREF_sub.setWindowFlags(QtCore.Qt.WindowMaximizeButtonHint)
        memDUT_sub.setWindowFlags(QtCore.Qt.WindowMaximizeButtonHint)

        self.mem_mdi.tileSubWindows()
    
    def display(self):
        # set the index of the currently visible options
        sender = self.sender()
        if sender.text() == "Instructions":
            self.stack.setCurrentIndex(0)
        elif sender.text() == "Registers":
            self.stack.setCurrentIndex(1)
        elif sender.text() == "Mem Data":
            self.stack.setCurrentIndex(2)

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
        self.ELF_files_path, _ = QFileDialog.getOpenFileNames(self,'选择文件')

        # self.ELF_path = [os.path.split(x)[0] for x in self.ELF_files_path]
        self.ELF_path_dict = {}
        for i in range(len(self.ELF_files_path)):
            key = i
            self.ELF_path_dict[key] = os.path.split(self.ELF_files_path[i])[0]
        
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
        # prevent program crash
        if self.taskTable.item(0, 1) == None: return
        # get checked task from taskTable
        checkedFile = []
        for row in range(self.taskTable.rowCount()):
            if self.taskTable.item(row, 1) == None: pass
            elif self.taskTable.item(row, 0).checkState() != QtCore.Qt.Unchecked:
                checkedFile.append(self.ELF_path_dict[row] + "/" + self.taskTable.item(row, 1).text())
        # print(checkedFile)

        # get ELF path from settings
        dutPATH = self.clientView.settings.value("CLIENT/DUTELF")
        refPATH = self.clientView.settings.value("CLIENT/RefELF")

        # put the checked file to server and client
        if self.serverView.remoteHost == "HAPS01":
            ip = "10.12.208.30"
        
        for path in checkedFile:
            child = spawn("scp -P{port} {localPath} {hostname}@{hostIp}:{remotePath}".format(port = self.serverView.port, 
                           localPath = path, hostname = self.serverView.hostname, hostIp = ip, remotePath=dutPATH))
            child.expect('password:')
            child.sendline(self.serverView.password)
            child.read()
            
            os.popen("cp {sourcePath} {targetPath}".format(sourcePath=path, targetPath=refPATH))

        QMessageBox.information(self, '提示', '任务加载成功!', QMessageBox.Yes)

    def handleTruncate(self):
        self.taskTable.clearContents()

    def handleRouteSelect(self):
        snapshotPath, _ = QFileDialog.getOpenFileName(self,'选择文件')
        self.routeLineEdit.setText(snapshotPath)

    def handleStartTest(self):
        """ start execute task """
        self.startFlag = 0
        # use same snapshot to initialize REF and DUT
        # print(self.main_ui.routeLineEdit.text())

        entryPath = os.getcwd() + "/backend"

        # execute on DUT(HAPS)
        if self.cmdTextEdit.toPlainText() != "":
            content = self.cmdTextEdit.toPlainText()
            cmdSTR = ""
            for line in content.splitlines():
                cmdSTR = cmdSTR + line + ";"
            cmdSTR = cmdSTR[:-1]
            # if self.serverView.remoteHost == "HAPS01":
            #     ip = "10.12.208.30"
            # res = self.serverCMD(ip, "cd {path};{cmd}".format(path=DUT_PATH, cmd=cmdSTR))
            res = os.popen("cd {path};{cmd}".format(path=entryPath, cmd=cmdSTR)).read()
            print(res)

        # execute on REF(spike,gem5)
        if self.RefTextEdit.toPlainText() != "":
            content = self.RefTextEdit.toPlainText()
            cmdSTR = ""
            for line in content.splitlines():
                cmdSTR = cmdSTR + line + ";"
            cmdSTR = cmdSTR[:-1]
            res2 = os.popen("cd {path};{cmd}".format(path=entryPath, cmd=cmdSTR)).read()
            print(res2)

        self.startFlag = 1
    
    def serverCMD(self, ip, command):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        ssh.connect(hostname=ip, username=self.serverView.hostname, password=self.serverView.password)
        _, stdout, _ = ssh.exec_command(command, get_pty=True)

        res = ''
        lines = stdout.readlines()
        for line in lines:
            res += line
        # print(res)

        ssh.close()
        return res
    def refresh(self):
        #print('refresh')
        self.is_mdi.tileSubWindows()
        self.reg_mdi.tileSubWindows()
        self.mem_mdi.tileSubWindows()

    def resizeEvent(self, event):
        self.resized.emit()
        return super(DebugManage, self).resizeEvent(event)
        
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
    gui.setWindowIcon(QIcon('imgs/block.png'))
    gui.show()
    sys.exit(app.exec_())
