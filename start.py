import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QWidget
from smu_jwxt import Ui_Form

class Ui_MainWindow(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # 设置无边框
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        # 设置主背景透明
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        # 添加成员变量来追踪鼠标拖动
        self._dragging = False
        self._drag_position = QtCore.QPoint(0, 0)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self._dragging = True
            self._drag_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if self._dragging and event.buttons() == QtCore.Qt.LeftButton:
            self.move(event.globalPos() - self._drag_position)
            event.accept()

    def mouseReleaseEvent(self, event):
        self._dragging = False
        event.accept()


if __name__ == "__main__":
    # 窗口自适应
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QtWidgets.QApplication(sys.argv)
    first = Ui_MainWindow()
    first.show()
    sys.exit(app.exec_())