
import os
import subprocess

import requests
from PyQt5.QtCore import QEvent
from PyQt5.QtWidgets import QFileDialog, QMessageBox

from common.common_file import Common
from excel import getVrs


class AppModel():
    def __init__(self,view):
        self.config = Common().config
        self.view = view
        self.view.dropdown.currentIndexChanged.connect(self.update_folder_input)
        self.view.download_button.clicked.connect(self.download_file)
        self.view.upload_button.clicked.connect(self.upload_file)
        self.view.renewal_but.clicked.connect(self.pda_clone)
        self.view.xmind_add.currentIndexChanged.connect(self.get_ximd_adr)
        self.view.change_button.clicked.connect(self.xmind_to_excel)

    # 安装事件过滤器
    def upload_file(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, '上传文件')
        if file_path:
            self.view.url_input.setText(file_path)

    def get_eventFilter(self,obj, event):
        # 获取拖入的文件地址
        if event.type() == QEvent.DragEnter and obj in [self.view.url_input, self.view.xmind_input]:
            if event.mimeData().hasUrls():
                event.accept()
            else:
                event.ignore()
            return True
        elif event.type() == QEvent.Drop and obj in [self.view.url_input, self.view.xmind_input]:
            urls = event.mimeData().urls()
            if len(urls) == 1:
                file_path = urls[0].toLocalFile()
                if obj == self.view.url_input:
                    self.view.url_input.setText(file_path)
                elif obj == self.view.xmind_input:
                    self.view.xmind_input.setText(file_path)
            else:
                QMessageBox.warning(self, '错误', '只能拖入一个文件！')
            return True

        return super().eventFilter(obj, event)

    def update_folder_input(self):
        selected_address = self.view.dropdown.currentText()
        self.view.download_button.setVisible(True)
        self.view.start_ass_btn.setVisible(False)  # 选择选项2时显示按钮
        self.view.change_ass_file_btn.setVisible(False)
        self.view.mp_dropdown.setVisible(False)
        if selected_address == '请选择地址':
            self.view.folder_input.clear()
            self.view.url_input.clear()
        elif selected_address == '云商测试环境':
            save_address = self.config.get('yunshang_tset', 'save')
            self.view.folder_input.setText(save_address)
            update_address = self.config.get('yunshang_tset', 'update')
            self.view.url_input.setText(update_address)
        elif selected_address == '微平台助手':
            self.view.url_input.clear()
            self.view.mp_dropdown.setVisible(True)
            self.view.start_ass_btn.setVisible(True)
            self.view.change_ass_file_btn.setVisible(True)
            self.view.download_button.setVisible(False)
            self.view.wpt_product.change_mg_path()

    def download_file(self):
        url = self.view.url_input.text()
        save_folder = self.view.folder_input.text()

        if not url and not save_folder:
            QMessageBox.warning(self, '错误', '请输入下载地址或选择上传文件！')
            return

        if not save_folder:
            QMessageBox.warning(self, '错误', '请输入保存文件夹！')
            return

        if self.view.dropdown.currentIndex() == 0:
            QMessageBox.warning(self, '错误', '请选择地址！')
            return

        if self.view.dropdown.currentText() == '云商测试环境':
            save_folder = self.config.get('yunshang_tset', 'save')
        elif self.view.dropdown.currentText() == '微平台助手':
            if self.view.mp_dropdown.currentText() == '测试环境':
                dir_path = ('mp_helper', 'sit_dir_path')
            elif self.view.mp_dropdown.currentText() == '预发布环境':
                dir_path = ('mp_helper', 'sit_dir_path')
            else:
                raise Exception("为获取到环境地址")
            save_folder = self.config.get(*dir_path)

        # 上传文件
        if os.path.exists(url):
            file_path = url
        else:
            # 下载文件
            try:
                response = requests.get(url, stream=True)
                response.raise_for_status()
            except requests.exceptions.RequestException as e:
                QMessageBox.warning(self, '错误', '下载文件失败：' + str(e))
                return

            # 保存下载文件
            file_path = os.path.join(save_folder, 'downloaded_files.zip')
            with open(file_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=1024):
                    file.write(chunk)

        Common().zip_Change_file(file_path, save_folder, True, True)

    def pda_clone(self):
        def clone_repository(repo_url, destination_folder):
            try:
                subprocess.check_output(['git', 'clone', repo_url, destination_folder])
                QMessageBox.information(self, '成功', '代码拉取成功！')
            except subprocess.CalledProcessError as e:
                QMessageBox.warning(self, '错误', '代码拉取失败:')

        repo_url = self.config.get('pda', 'repo_url')
        destination_folder = self.config.get('pda', 'destination_folder')
        clone_repository(repo_url, destination_folder)

    def get_ximd_adr(self):
        change_address = self.view.xmind_add.currentText()
        if change_address == '同xmind地址':
            self.excel_path = os.path.abspath(change_address)
        elif change_address == 'excel配置地址':
            self.excel_path = self.config.get('xmind_to_excel', 'excel_adr')

    def xmind_to_excel(self):
        xmind_adr = self.view.xmind_input.text()
        if self.excel_path == "":
            self.excel_path = xmind_adr.replace(".xmind", ".xlsx")
        if os.path.isfile(xmind_adr):
            _, extension = os.path.splitext(xmind_adr)
            if extension.lower() == '.xmind':
                getVrs().convert_xmind_to_excel(xmind_adr, self.excel_path)
            else:
                QMessageBox.warning(self, '错误', '传入文件非xmind格式！')
        else:
            QMessageBox.warning(self, '错误', 'xmind地址无效！')