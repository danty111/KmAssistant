import os
import threading

from common.common_file import Common


class change_mg_helper:
    def change(self,file_path,save_path):
        Common().zip_Change_file(file_path,save_path)

    def open_exe(self,exe_file_path):

        exe_file_path = os.path.join(exe_file_path,Common().config.get('mp_helper','helper_name'))
        def execute_command(command):
            os.system(command)
        # 创建新线程并启动
        thread = threading.Thread(target=execute_command, args=(exe_file_path,))
        thread.start()
