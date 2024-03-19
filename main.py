
import sys
from PyQt5.QtWidgets import QApplication,  QMessageBox, QWidget
from app_obj import AppModel
from app_ui import AppUI

class DownloaderApp(AppModel):
    def __init__(self,view):
        super().__init__(view)

def excepthook(exc_type, exc_value, exc_traceback):
    error_message = "程序报错：" + str(exc_value)
    print(None, "错误", error_message, QMessageBox.Ok)
    QMessageBox.critical(None, "错误", error_message, QMessageBox.Ok)


if __name__ == '__main__':
    sys.excepthook = excepthook  # 设置全局的异常处理函数
    app = QApplication(sys.argv)
    view = AppUI()
    window = AppModel(view)
    view.show()
    sys.exit(app.exec_())
