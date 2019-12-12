
from utils.file_type import *

success_count = 0

class ReadFlies(object):
    """读取导入文件"""

    def __init__(self, file_obj):
        self.file_obj = file_obj

    def handle_files(self):
        """读取/判断/处理/存储文件内容"""
        file_type = FileType(self.file_obj, self.storage)
        Suffix = "_" + self.file_obj.name.rsplit('.', 1)[1]
        func = getattr(file_type, Suffix)
        success_count, file_fail_list = func()
        return success_count, file_fail_list

    def storage(self, data_list):
        """持久化"""
        import time
        global success_count
        start = time.time()
        models.DataFile.objects.bulk_create(data_list)
        end = time.time()
        print('存储耗时%s秒' % (end-start))
        success_count += len(data_list)
        return success_count



