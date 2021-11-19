import os
import re
import sys
import time

import paramiko
from paramiko import file
from pexpect import *

from watchdog.observers import Observer
from watchdog.events import *
from threading import Thread

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

        """ load views """
        self.serverView = ServerConfView()
        self.clientView = ClientConfView()
        self.importView = SnapshotImportView()
        self.exportView = SnapshotExportView()
        self.compareView = SnapshotCompareView()

        self.init()

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
        self.link_status = QLabel('{:<15}'.format('连接状态：'))
        self.run_status = QLabel('{:<15}'.format('运行状态：'))
        self.health_status = QLabel('{:<15}'.format('当前健康状态：'))
        self.harttext_status = QLabel('当前hart：')
        self.hart_status = QComboBox()
        self.refpc_status = QLabel('PC(REF)：')
        self.dutpc_status = QLabel('PC(DUT)：')
        self.refminstret_status = QLabel('minstret(REF)：')
        self.dutminstret_status = QLabel('minstret(DUT)：')
        self.refpc_status.setMinimumWidth(50)
        self.dutpc_status.setMinimumWidth(50)
        self.refminstret_status.setMinimumWidth(60)
        self.dutminstret_status.setMinimumWidth(60)
        self.hart_status.addItems(['hart0'])
        self.statuswidget = QWidget()
        self.status_layout = QHBoxLayout()
        self.status_layout.addWidget(self.harttext_status)
        self.status_layout.addWidget(self.hart_status)
        self.status_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.statuswidget.setLayout(self.status_layout)
        self.statusbar.addPermanentWidget(self.link_status,stretch=1)
        self.statusbar.addPermanentWidget(self.run_status,stretch=1)
        self.statusbar.addPermanentWidget(self.health_status, 1)
        self.statusbar.addPermanentWidget(self.statuswidget, 1)
        self.statusbar.addPermanentWidget(self.refpc_status, 5)
        self.statusbar.addPermanentWidget(self.dutpc_status, 5)
        self.statusbar.addPermanentWidget(self.refminstret_status, 6)
        self.statusbar.addPermanentWidget(self.dutminstret_status, 6)

        # add load-table and load-button for main ui
        self.taskTable = TableWidget(3, 2)
        self.LoadLayout.addWidget(self.taskTable, 0, 0, 10, 12)
        self.spaceLable = QLabel()
        self.LoadLayout.addWidget(self.spaceLable, 10, 12, 0, 1)

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
        self.compareButton.clicked.connect(self.showCompare)
        self.comboBox.currentIndexChanged.connect(self.selectionchange)

        # self.compileButton.clicked.connect(self.handleCompile)
        self.testButton.clicked.connect(self.handleStartTest)
        # self.routeButton.clicked.connect(self.handleRouteSelect)
        self.trunButton.clicked.connect(self.handleTruncate)
        self.loadButton.clicked.connect(self.handleLoadELF)
        self.resized.connect(self.refresh)
        self.downButton.clicked.connect(self.downHide)
        self.upButton.clicked.connect(self.upper)

        self.IS_button.setCheckable(True)
        self.IS_button.setAutoExclusive(True)
        self.Reg_button.setCheckable(True)
        self.Reg_button.setAutoExclusive(True)
        self.Mem_button.setCheckable(True)
        self.Mem_button.setAutoExclusive(True)

        self.switchFlag = 0 # 0:health  1:snapshot

    def is_mdiUI(self):

        self.isDUT_sub = ISDUTsub()
        self.is_mdi.addSubWindow(self.isDUT_sub)

        self.isREF_sub = ISREFsub()
        self.is_mdi.addSubWindow(self.isREF_sub)

        self.isREF_sub.setWindowFlags(QtCore.Qt.WindowMaximizeButtonHint)
        self.isDUT_sub.setWindowFlags(QtCore.Qt.WindowMaximizeButtonHint)

        self.isREF_sub.setWindowFlags(Qt.FramelessWindowHint)
        self.isDUT_sub.setWindowFlags(Qt.FramelessWindowHint)
        
        self.is_mdi.tileSubWindows()
    
    def reg_mdiUI(self):

        self.regDUT_sub = REGDUTsub()
        self.reg_mdi.addSubWindow(self.regDUT_sub)
        
        self.regREF_sub = REGREFsub()
        self.reg_mdi.addSubWindow(self.regREF_sub)

        self.regREF_sub.setWindowFlags(QtCore.Qt.WindowMaximizeButtonHint)
        self.regDUT_sub.setWindowFlags(QtCore.Qt.WindowMaximizeButtonHint)

        self.regREF_sub.setWindowFlags(Qt.FramelessWindowHint)
        self.regDUT_sub.setWindowFlags(Qt.FramelessWindowHint)
        
        self.reg_mdi.tileSubWindows()

    def mem_mdiUI(self):
        
        self.memDUT_sub = MEMDUTsub()
        self.mem_mdi.addSubWindow(self.memDUT_sub)

        self.memREF_sub = MEMREFsub()
        self.mem_mdi.addSubWindow(self.memREF_sub)

        self.memREF_sub.setWindowFlags(QtCore.Qt.WindowMaximizeButtonHint)
        self.memDUT_sub.setWindowFlags(QtCore.Qt.WindowMaximizeButtonHint)

        self.memREF_sub.setWindowFlags(Qt.FramelessWindowHint)
        self.memDUT_sub.setWindowFlags(Qt.FramelessWindowHint)

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

    def selectionchange(self):
        if self.comboBox.currentIndex() == 0:
            self.switchFlag = 0
        elif self.comboBox.currentIndex() == 1:
            self.switchFlag = 1

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
        # if self.serverView.remoteHost == "HAPS01":
        #     ip = "10.12.208.30"
        refIP = self.serverView.ref_remoteHost
        dutIP = self.serverView.dut_remoteHost
        print(refIP, dutIP)
        
        for path in checkedFile:
            # put the checked file to server
            ref_child = spawn("scp -P{port} {localPath} {hostname}@{hostIp}:{remotePath}".format(port = self.serverView.ref_port, 
                           localPath = path, hostname = self.serverView.ref_hostname, hostIp = refIP, remotePath=refPATH))
            ref_child.expect('password:')
            ref_child.sendline(self.serverView.ref_password)
            ref_child.read()
            
            dut_child = spawn("scp -P{port} {localPath} {hostname}@{hostIp}:{remotePath}".format(port = self.serverView.dut_port, 
                           localPath = path, hostname = self.serverView.dut_hostname, hostIp = dutIP, remotePath=dutPATH))
            dut_child.expect('password:')
            dut_child.sendline(self.serverView.dut_password)
            dut_child.read()

        QMessageBox.information(self, '提示', '任务加载成功!', QMessageBox.Yes)

    def handleTruncate(self):
        self.taskTable.clearContents()

    def handleRouteSelect(self):
        snapshotPath, _ = QFileDialog.getOpenFileName(self,'选择文件')
        self.routeLineEdit.setText(snapshotPath)

    def handleStartTest(self):
        """ start execute task """
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

        # display information from files(Instruction, Register, Memory)
        p = Thread(target=self.WatchdogUDF)
        p.setDaemon(True)
        p.start()

        p2 = Thread(target=self.WatchdogUDF2)
        p2.setDaemon(True)
        p2.start()

    def WatchdogUDF(self):
        # set initial value for health information
        fileName_1 = self.clientView.ref_healthPath + "/cpu_status_spike"
        fileName_2 = self.clientView.dut_healthPath + "/cpu_status_haps"
        healthFirstFlag = 0
        file_1 = open(fileName_1, "r+")
        firstTime_1 = time.localtime(os.path.getmtime(fileName_1))
        file_2 = open(fileName_2, "r+")
        firstTime_2 = time.localtime(os.path.getmtime(fileName_2))

        while True:
            # print(self.switchFlag)
            if self.switchFlag == 0:
                view = "VIEW_0"     # VIEW_0:health VIEW_1:snapshot
                # if healthFirstFlag == 0:
                #     healthFirstFlag = 1
                #     self.regREF_sub.display(view)
                #     file_1.close()
                #     self.regDUT_sub.display(view)
                #     file_2.close()
                #     ref_pc = self.showStatus("REF", view)
                #     dut_pc = self.showStatus("DUT", view)
                #     self.isREF_sub.display(ref_pc)
                #     self.isDUT_sub.display(dut_pc)

                time.sleep(3)
                
                # compare health(REF & DUT) and send flag
                while True:
                    lastModifyTime_1 = time.localtime(os.path.getmtime(fileName_1))
                    lastModifyTime_2 = time.localtime(os.path.getmtime(fileName_2))
                    if lastModifyTime_1 != firstTime_1 and lastModifyTime_2 != firstTime_2:
                        os.popen('cd {path}/backend && ./cpu_status_file_cmp.sh'.format(path=os.getcwd()))
                        with open("{cmpPath}/cpu_status_cmp_result.txt".format(cmpPath=self.clientView.healthCompare)) as f:
                            content = f.read()
                        print(content)
                        if content == "":
                            self.sendFlag()
                        else:
                            QMessageBox.information(self, '提示', '健康信息异常，程序已停止!')
                            input()
                        f.close()
                        break

                # REF [register, instruction] display
                if firstTime_1 != lastModifyTime_1:
                    firstTime_1 = lastModifyTime_1
                    self.regREF_sub.display(view)
                    ref_pc = self.showStatus("REF", view)
                    self.isREF_sub.display(ref_pc)

                # DUT [register, instruction] display
                if firstTime_2 != lastModifyTime_2:
                    firstTime_2 = lastModifyTime_2
                    self.regDUT_sub.display(view)
                    dut_pc = self.showStatus("DUT", view)
                    self.isDUT_sub.display(dut_pc)

    def WatchdogUDF2(self):
        # set initial value for snapshot register
        refSnapshotFile = self.clientView.ref_snapshotPath + "/regsnapshot_gem5.txt"
        dutSnapshotFile = self.clientView.dut_snapshotPath + "/regsnapshot_gem5.txt"
        snapFirstFlag = 0
        file_ref = open(refSnapshotFile, "r+")
        firstTime_ref = time.localtime(os.path.getmtime(refSnapshotFile))
        file_dut = open(dutSnapshotFile, "r+")
        firstTime_dut = time.localtime(os.path.getmtime(dutSnapshotFile))

        # set initial value for snapshot memory
        refMemoryFile = self.clientView.ref_snapshotPath + "/memsnapshot_hexdump_gem5.txt"
        dutMemoryFile = self.clientView.dut_snapshotPath + "/memsnapshot_hexdump_haps.txt"
        memFirst_ref = time.localtime(os.path.getmtime(refMemoryFile))
        memFirst_dut = time.localtime(os.path.getmtime(dutMemoryFile))

        while True:
            # print(self.switchFlag)
            if self.switchFlag == 1:
                view = "VIEW_1"     # VIEW_0:health VIEW_1:snapshot
                # if snapFirstFlag == 0:
                #     snapFirstFlag = 1
                #     self.regREF_sub.display(view)
                #     file_ref.close()
                #     self.regDUT_sub.display(view)
                #     file_dut.close()
                #     ref_pc = self.showStatus("REF", view)
                #     dut_pc = self.showStatus("DUT", view)
                #     self.isREF_sub.display(ref_pc)
                #     self.isDUT_sub.display(dut_pc)

                time.sleep(3)

                lastModifyTime_ref = time.localtime(os.path.getmtime(refSnapshotFile))
                lastModifyTime_dut = time.localtime(os.path.getmtime(dutSnapshotFile))

                lastModifyTime_mem_ref = time.localtime(os.path.getmtime(refMemoryFile))
                lastModifyTime_mem_dut = time.localtime(os.path.getmtime(dutMemoryFile))

                # REF [register, instruction] display
                if firstTime_ref != lastModifyTime_ref:
                    firstTime_ref = lastModifyTime_ref
                    self.regREF_sub.display(view)
                    ref_pc = self.showStatus("REF", view)
                    self.isREF_sub.display(ref_pc)

                # DUT [register, instruction] display
                if firstTime_dut != lastModifyTime_dut:
                    firstTime_dut = lastModifyTime_dut
                    self.regDUT_sub.display(view)
                    dut_pc = self.showStatus("DUT", view)
                    self.isDUT_sub.display(dut_pc)

                # REF [memory] display
                if memFirst_ref != lastModifyTime_mem_ref:
                    memFirst_ref = lastModifyTime_mem_ref
                    self.memREF_sub.display()

                # DUT [memory] display
                if memFirst_dut != lastModifyTime_mem_dut:
                    memFirst_dut = lastModifyTime_mem_dut
                    self.memDUT_sub.display()

    def sendFlag(self):
        # write for REF
        ip = self.serverView.ref_remoteHost
        user = self.serverView.ref_hostname
        passwd = self.serverView.ref_password
        cmd = "cd ~/CADS-REF/debugToolData;echo '1'> flag.txt"
        self.serverCMD(ip, user, passwd, cmd)

        # write for DUT
        ip_2 = self.serverView.dut_remoteHost
        user_2 = self.serverView.dut_hostname
        passwd_2 = self.serverView.dut_password
        cmd_2 = "cd ~/debugToolData;echo '1'> flag.txt"
        self.serverCMD(ip_2, user_2, passwd_2, cmd_2)

    def showStatus(self, source, view):
        # get pc and minstret
        pc, minstret = self.findValue(source, view)

        # display
        if source == "REF":
            self.refpc_status.setText('PC(REF)：{0}'.format(pc))
            self.refminstret_status.setText('minstret(REF)：{0}'.format(minstret))
        else:
            self.dutpc_status.setText('PC(DUT)：{0}'.format(pc))
            self.dutminstret_status.setText('minstret(DUT)：{0}'.format(minstret))
        
        return pc

    def findValue(self, source, view):
        if source == "REF":
            curSub = self.regREF_sub
        else: 
            curSub = self.regDUT_sub
        
        data = curSub.getData(view)

        for i in range(len(data)):
            for j in range(len(data[i])):
                if "pc" == data[i][j]:
                    rowPCList = data[i]
                    pc = rowPCList[1]
                if "minstret" == data[i][j]:
                    rowList = data[i]
                    minstret = rowList[1]

        return pc, minstret

    def serverCMD(self, ip, user, passwd, command):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        if ip == "10.12.130.31":
            ssh.connect(hostname=ip, port=22017, username=user, password=passwd)
            _, stdout, _ = ssh.exec_command(command, get_pty=True)
        else:
            ssh.connect(hostname=ip, username=user, password=passwd)
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

    def downHide(self):
        self.widget.setMaximumHeight(40)
        self.downButton.setEnabled(False)
        self.upButton.setEnabled(True)
        self.is_mdi.tileSubWindows()
        self.reg_mdi.tileSubWindows()
        self.mem_mdi.tileSubWindows()

    def upper(self):
        self.widget.setMaximumHeight(16777215)
        self.upButton.setEnabled(False)
        self.downButton.setEnabled(True)
        self.is_mdi.tileSubWindows()
        self.reg_mdi.tileSubWindows()
        self.mem_mdi.tileSubWindows()


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


class FileEventHandler(FileSystemEventHandler):
    def __init__(self):
        FileSystemEventHandler.__init__(self)

    def on_moved(self, event):
        if event.is_directory:
            print("directory moved from {0} to {1}".format(
                event.src_path, event.dest_path))
        else:
            print("file moved from {0} to {1}".format(
                event.src_path, event.dest_path))

    def on_created(self, event):
        if event.is_directory:
            print("directory created:{0}".format(event.src_path))
        else:
            print("file created:{0}".format(event.src_path))

    def on_deleted(self, event):
        if event.is_directory:
            print("directory deleted:{0}".format(event.src_path))
        else:
            print("file deleted:{0}".format(event.src_path))

    def on_modified(self, event):
        if event.is_directory:
            # print("directory modified:{0}".format(event.src_path))
            pass
        else:
            print("file modified:{0}".format(event.src_path))
            # print(event.src_path, DebugManage().clientView.ref_healthPath)

if __name__ == "__main__":
    with open('view/app.qss', encoding='utf-8') as f:
        qss = f.read()
    app = QApplication(sys.argv)
    app.setStyleSheet(qss)
    gui = DebugManage()
    gui.setWindowIcon(QIcon('imgs/block.png'))
    gui.show()
    sys.exit(app.exec_())
