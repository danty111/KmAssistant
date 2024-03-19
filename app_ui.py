from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QLineEdit, QPushButton, QComboBox, QHBoxLayout
from change_mg_helper import change_mg_helper
from common.common_file import Common
class AppUI(QWidget):
    download_clicked = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.setWindowTitle('科脉测试助手')
        self.setGeometry(100, 100, 400, 200)
        self.layout = QGridLayout()
        self.setLayout(self.layout)
        # 下载按钮
        self.download_add_UI()
        self.upload_file_UI()
        self.save_file_UI()
        self.select_product_UI()
        self.download_button_UI()
        self.xmind_label_UI()
        self.get_xmind_add_UI()
        self.update_PDA_UI()
        self.renewal_xmind_UI()

        self.url_input.installEventFilter(self)
        self.xmind_input.installEventFilter(self)
        self.wpt_product = WPT_product(self)
        self.wpt_product.sele_environment()

        self.mp_dropdown = self.wpt_product.mp_dropdown
        self.start_ass_btn = self.wpt_product.start_ass()
        self.change_ass_file_btn = self.wpt_product.change_ass()


        button_layout = QHBoxLayout()  # 按钮布局
        button_layout.addWidget(self.mp_dropdown)
        button_layout.addWidget(self.start_ass_btn)
        button_layout.addWidget(self.change_ass_file_btn)
        self.layout.addLayout(button_layout, 2, 0, 1, 3)  # 将按钮布局添加到主布局
        self.show()

    def xmind_label_UI(self):
        self.xmind_label = QLabel('xmind地址:')
        self.layout.addWidget(self.xmind_label, 6, 0)
        self.xmind_input = QLineEdit()
        self.layout.addWidget(self.xmind_input, 6, 1)

    def download_button_UI(self):
        self.download_button = QPushButton('下载')
        self.layout.addWidget(self.download_button, 3, 0, 1, 3)
        self.setAcceptDrops(True)
    def download_add_UI(self):
        # 下载地址
        url_label = QLabel('下载地址:')
        self.layout.addWidget(url_label, 0, 0)
        self.url_input = QLineEdit()
        self.layout.addWidget(self.url_input, 0, 1)

    def upload_file_UI(self):
        # 上传文件
        self.upload_button = QPushButton('上传文件')
        self.layout.addWidget(self.upload_button, 0, 2)

    def save_file_UI(self):
        # 保存文件夹
        folder_label = QLabel('保存文件夹:')
        self.layout.addWidget(folder_label, 1, 0)
        self.folder_input = QLineEdit()
        self.layout.addWidget(self.folder_input, 1, 1)

    def select_product_UI(self):
        self.dropdown = QComboBox()
        self.dropdown.addItem('请选择地址')
        self.dropdown.addItem('云商测试环境')
        self.dropdown.addItem('%s' % '微平台助手')
        self.layout.addWidget(self.dropdown, 1, 2)

    def update_PDA_UI(self):
        self.renewal_but = QPushButton('更新PDA')
        self.layout.addWidget(self.renewal_but, 5, 0, 1, 3)

    def get_xmind_add_UI(self):
        self.xmind_add = QComboBox()
        self.xmind_add.addItem('同xmind地址')
        self.xmind_add.addItem('excel配置地址')
        self.layout.addWidget(self.xmind_add, 6, 2)
        self.excel_path = ''

    def renewal_xmind_UI(self):
        self.change_button = QPushButton('更新xmind')
        self.layout.addWidget(self.change_button, 7, 0, 1, 3)

class WPT_product():
    def __init__(self,obj):
        self.__dict__.update(obj.__dict__)
        self.mp_dropdown = QComboBox()

    def sele_environment(self):
        # 选择微平台环境地址
        self.mp_dropdown.addItem('测试环境')
        self.mp_dropdown.addItem('预发布环境')
        self.mp_dropdown.currentIndexChanged.connect(self.change_mg_path)
        self.mp_dropdown.setVisible(False)

    def change_mg_path(self):
        if self.mp_dropdown.currentText() == '测试环境':
            dir_path = ('mp_helper', 'sit_dir_path')
        elif self.mp_dropdown.currentText() == '预发布环境':
            dir_path = ('mp_helper', 'pet_dir_path')
        else:
            raise Exception("为获取到环境地址")
        save_folder = Common().config.get(*dir_path)
        self.folder_input.setText(save_folder)

    def start_ass(self):
        self.start_ass_btn = QPushButton("启动助手文件")
        self.start_ass_btn.clicked.connect(lambda: change_mg_helper().open_exe(self.folder_input.text()))
        self.start_ass_btn.setVisible(False)  # 初始时隐藏按钮
        return self.start_ass_btn

    def change_ass(self):
        self.change_ass_file_btn = QPushButton("替换助手文件")
        self.change_ass_file_btn.clicked.connect(lambda: change_mg_helper().change(self.url_input.text(), self.folder_input.text()))
        self.change_ass_file_btn.setVisible(False)  # 初始时隐藏按钮
        return self.change_ass_file_btn