import sys
import time

from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem


from sqlBlind import Ui_Dialog
import mapper.sqli_bb as bb
import mapper.sqli_bb_widebyte as bb_widebyte
import mapper.sqli_tb as tb
import mapper.sqli_time as stime

TIME_LIMIT = 100
# 计时器
class External(QThread):
    """
    Runs a counter thread.
    """
    countChanged = pyqtSignal(int)
    count = 0

    def run(self):
        while self.count < TIME_LIMIT:
            self.count +=1
            time.sleep(0.01)
            self.countChanged.emit(self.count)

    def initCount(self,num):
        self.countChanged.emit(num)
        self.count = num


class myWindow(QMainWindow, Ui_Dialog):
    def __init__(self, parent=None):
        super(myWindow, self).__init__(parent)
        self.setupUi(self)
        self.connectSlots()
        # self.msg = "please select a method to blind"
        self.step = 0
        self.tableList = [self.tableWidget,self.tableWidget_2,self.tableWidget_3,self.tableWidget_4]
        self.blindList = [bb,bb_widebyte,tb,stime]
        self.curTable = self.tableWidget
        self.calc = External()

    # 绑定组件
    def connectSlots(self):
        # ProcessBar
        self.startButtom.clicked.connect(self.startProcess)
        # StartButtom
        self.startButtom.clicked.connect(self.sqlBlind)

    # 执行注入
    def sqlBlind(self):
        # 选择注入文件
        curBlind = self.blindList[self.tabMenu.currentIndex()]
        # 选择注入表格
        self.curTable = self.tableList[self.tabMenu.currentIndex()]
        # 选择注入方式
        self.res1,self.res2 = "",""
        if self.comboBox.currentIndex() == 0:
            # msg = "正在执行 CurrentDatabaseBool.."
            self.res1,self.res2 = curBlind.CurrentDatabaseBool()

        elif self.comboBox.currentIndex() == 1:
            # msg = "正在执行 TablesBool.."
            self.res1,self.res2 = curBlind.TablesBool()

        elif self.comboBox.currentIndex() == 2:
            # msg = "正在执行 ColumnsBool"
            self.res1,self.res2 = curBlind.ColumnsBool()
        else:
            # msg = "正在执行 "
            self.res1,self.res2 = curBlind.ContentBool()
        # 注入成功
        # self.calc.initCount(100)
        # 设置表格内容
        # self.setTableContent(self.res1,self.res2)

    # 设置表格结果
    def setTableContent(self,res1,res2):
        print(self.tabMenu.currentIndex())
        i = self.comboBox.currentIndex()
        item0 = QTableWidgetItem(self.res1)
        item1 = QTableWidgetItem(self.res2)
        self.curTable.setItem(i,0,item0)
        self.curTable.setItem(i,1,item1)

    # 开始注入线程
    def startProcess(self):
        # 初始化
        self.calc.initCount(0)
        self.progressBar.setValue(0)
        self.processLabel.setText("开始注入...")
        self.calc.countChanged.connect(self.onCountChanged)
        self.processLabel.setText("注入中...")
        self.calc.start()

    def onCountChanged(self, value):
        if value >= TIME_LIMIT:
            self.processLabel.setText("注入成功")
            self.setTableContent(self.res1, self.res2)
        self.progressBar.setValue(value)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = myWindow()
    w.show()
    sys.exit(app.exec_())







