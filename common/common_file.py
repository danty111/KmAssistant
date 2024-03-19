import configparser
import ctypes
import os
import shutil
import zipfile
import subprocess
from ctypes import wintypes

from PyQt5.QtCore import QEvent
from PyQt5.QtWidgets import QMessageBox, QWidget

from selenium import webdriver

class Common(QWidget):
    def __init__(self):
        super().__init__()
        # 获取 INI 文件的路径
        current_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(current_dir)
        ini_file = os.path.join(parent_dir, 'address.ini')

        # 创建 ConfigParser 对象
        self.config = configparser.ConfigParser()

        # 读取 INI 文件
        self.config.read(ini_file, encoding='utf-8')

    def zip_Change_file(self, file_path, save_folder, need_zip=False, need_bin=False):
        """
        文件替换
        :param file_path:
        :param save_folder:
        :param need_zip:
        :param need_bin:
        :return:
        """
        if need_zip:
            # 解压缩文件
            try:
                with zipfile.ZipFile(file_path, 'r') as zip_ref:
                    zip_ref.extractall(save_folder)

            except zipfile.BadZipFile as e:
                QMessageBox.warning(self, '错误', '解压缩文件失败：' + str(e))
                return
            source_folder = os.path.join(save_folder, "bin")
        else:
            source_folder = file_path
        if source_folder == '':
            QMessageBox.information(self,"下载地址为空，请填写下载地址")
        for filename in os.listdir(source_folder):
            src_file = os.path.join(source_folder, filename)
            dst_file = os.path.join(save_folder, filename)
            # 替换文件
            if os.path.isfile(src_file):
                shutil.copy2(src_file, dst_file)
        QMessageBox.information(self, '成功', '文件下载、解压缩和替换成功！')



    def open_exe_file(self,exe_file_path):
        try:
            subprocess.Popen(['runas', '/yuanhaibo:Yhb951236', exe_file_path])
        except Exception as e:
            QMessageBox.warning(self, '错误', f'打开文件失败：{str(e)}')

    import ctypes
    from ctypes import wintypes

    def input_handle_download(self,btn,singon):
        url = btn.text()
        singon.emit(url)


    def validate_admin_credentials(self,username, password):
        # 调用Windows API函数
        advapi32 = ctypes.WinDLL('advapi32')

        # 定义函数参数和返回类型
        advapi32.LogonUserW.argtypes = [
            ctypes.c_wchar_p, ctypes.c_wchar_p, ctypes.c_wchar_p,
            wintypes.DWORD, wintypes.DWORD, ctypes.POINTER(wintypes.HANDLE)
        ]
        advapi32.LogonUserW.restype = wintypes.BOOL

        # 验证用户名和密码
        token = wintypes.HANDLE()
        result = advapi32.LogonUserW(
            ctypes.c_wchar_p(username),
            None,
            ctypes.c_wchar_p(password),
            3,  # LOGON32_LOGON_NETWORK 类型
            0,  # LOGON32_PROVIDER_DEFAULT 类型
            ctypes.byref(token)
        )

        if result:
            is_valid = "管理员用户名和密码验证成功"
        else:
            is_valid = "管理员用户名和密码验证失败"

        # 返回验证结果
        return is_valid



class SeleniumWrapper:
    def __init__(self,driver_path):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        self.driver = webdriver.Chrome(executable_path=driver_path, options=options)


    def open_url(self, url):
        self.driver.get(url)

    def click_element_by_xpath(self, xpath):
        element = self.driver.find_element_by_xpath(xpath)
        element.click()

    def close(self):
        self.driver.quit()

