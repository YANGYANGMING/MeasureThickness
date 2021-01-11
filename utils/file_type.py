from thickness import models
from utils.handel_data import HandleDataSet
import struct, ast, json, array, time

handledataset = HandleDataSet()
file_fail_list = []

class FileType(object):
    """根据文件类型使用对应的数据处理方式"""
    def __init__(self, file_obj, storage):
        self.file_obj = file_obj
        self.storage = storage

    def _md5_verification(self):
        """
        md5验证
        :return:
        """
        # MD5校验
        self.md5_val = handledataset._MD5(self.file_obj.read())
        self.is_exist = models.DataTag.objects.filter(md5_val=self.md5_val).exists()
        self.file_obj.seek(0)  # 读取文件进行MD5后，光标移动到最后，用f.seek(0)移动光标到文件开头，以便重新读取文件
        return self.is_exist

    def _lsa(self):
        dic = {}
        data_list = []

        is_exist = self._md5_verification()

        if not is_exist:  #如果文件不存在
            models.DataTag.objects.create(file_name=self.file_obj.name, md5_val=self.md5_val)
            for i in self.file_obj.readlines():
                temp = i.decode('utf-8').strip('\n').split(':')
                if temp[0] == "Data":
                    temp_data_list = temp[1].strip("'").split(',')
                    temp_data_list = list(map(int, temp_data_list))  # 字符串转换成数字
                    dic[temp[0]] = temp_data_list
                else:
                    dic[temp[0]] = temp[1]
            data_len = len(dic['Data'])
            after_dict_data = struct.pack("<%sh" % data_len, *dic['Data'])
            del dic['Data']
            front_dict = str(dic)
            file_name_id = models.DataTag.objects.values('id').filter(md5_val=self.md5_val)[0]['id']
            data_list.append(models.DataFile(message_head=front_dict, message_body_data=after_dict_data, file_name_id=file_name_id))
        else:
            print('文件已存在')
            file_fail_list.append(self.file_obj.name)
        success_count = self.storage(data_list)
        return success_count, file_fail_list

    def _lsb(self):
        dic = {}
        data_list = []

        is_exist = self._md5_verification()

        if not is_exist:  #如果文件不存在
            models.DataTag.objects.create(file_name=self.file_obj.name, md5_val=self.md5_val)
            all = self.file_obj.read().decode('UTF-8')
            temp = all.split('------------------------------------')
            front = temp[0].strip('\n').split('\n')  #['Range: 1X,2048', 'Material: 碳钢,3254.0,0.53', 'Temperature: 25', 'Frequency: 高频', 'Average: 5', 'Gate: ', 'Detector: 射频波,0']
            after = temp[1].strip('\n').split('\n')  #['X\tY\tThickness\tGain\tData', '-5570820\t-986258681\t30.699756311475415\t60\t2225,2891,4087,1082,0,0,1877,4089,4089,4089,1761', ]
            for i in front:   #'Range: 1X,2048'
                temp_i = i.split(':')
                dic[temp_i[0]] = temp_i[1]
            front_dict = str(dic)   #{'Range': ' 1X,2048', 'Material': ' 碳钢,3254.0,0.53', 'Temperature': ' 25', 'Frequency': ' 高频', 'Average': ' 5', 'Gate': '', 'Detector': ' 射频波,0'}
            after_key_list = after[0].split('\t')   #['X', 'Y', 'Thickness', 'Gain', 'Data']
            data_len = int(dic.get('Range', '2048').strip('\n').split(',')[-1])  # ' 3X,6144'
            print(data_len)
            start2 = time.time()
            for ii in after[1:]:
                after_dict_param = {}
                after_value_list = ii.split('\t')
                after_dict = dict(zip(after_key_list, after_value_list))
                after_dict_data = after_dict.get('Data')
                # ---json---      data_len<=2048的时候，json比tuple快
                # if data_len <= 2048:
                after_dict_data = "[" + after_dict_data + "]"
                after_dict_data = json.loads(after_dict_data)
                after_dict_data = struct.pack("<%sh" % data_len, *after_dict_data)
                # ---tuple---    data_len>2048的时候，tuple比json快
                # else:
                #     after_dict['Data'] = (int(item) for item in after_dict_data.split(','))
                #     after_dict_data = struct.pack("<%sh" % data_len, *after_dict['Data'])

                # ---map---
                # after_dict_data = after_dict_data.strip("'").split(',')
                # after_dict['Data'] = list(map(int, after_dict_data))
                # after_dict_data = struct.pack("<%sh" % data_len, *after_dict['Data'])

                # ---array-tuple---
                # after_dict['Data'] = (int(item) for item in after_dict_data.split(','))
                # after_dict_data =array.array("h", after_dict['Data']).tobytes()
                # ---array-json---
                # after_dict_data = "[" + after_dict_data + "]"
                # after_dict_data = json.loads(after_dict_data)
                # after_dict_data = array.array("h", after_dict_data).tobytes()

                #SB操作
                after_dict_param['X'] = after_dict['X']
                after_dict_param['Y'] = after_dict['Y']
                after_dict_param['Thickness'] = after_dict['Thickness']
                after_dict_param['Gain'] = after_dict['Gain']
                after_dict_param = str(after_dict_param)

                file_name_id = models.DataTag.objects.values('id').filter(md5_val=self.md5_val)[0]['id']
                data_list.append(models.DataFile(message_head=front_dict, message_body_data=after_dict_data, message_body_param=after_dict_param, file_name_id=file_name_id))
            end2 = time.time()
            print('time2====', end2 - start2)
        else:
            print('文件已存在')
            file_fail_list.append(self.file_obj.name)
        success_count = self.storage(data_list)

        return success_count, file_fail_list










