from alg.emat.emat import calThickness
from thickness import models
from PIL import Image
import hashlib
import struct
import os

class HandleDataSet(object):
    def __init__(self):
        pass

    def get_selected_data(self, result_list):  #[['2019-09-20', '5', '7'], ['2019-09-21', '20', '21'], ]     range(4,12)   choose(5,7)
        """取出指定日期内指定id范围的数据，组成数据集id"""
        try:
            choose_dataset_id_list = []
            for dataset in result_list:
                id_range = [i for i in range(int(dataset[1]), int(dataset[2]) + 1)]    #[5, 6, 7]
                choose_dataset_id_list += id_range
            return choose_dataset_id_list   #[5, 6, 7, 20, 21]

        except Exception as e:
            print(e, "取出指定日期内指定id范围的数据，组成数据集时候发生错误，选择的数据ID不是有效值")

    def handle_data_and_run_alg(self, data_id_list, version):
        """跑算法前处理数据并且跑算法得出厚度值"""
        thickness_dict = {}
        for data_id_item in data_id_list:
            data_item = models.DataFile.objects.filter(nid=data_id_item).values('message_head', 'message_body_data', 'message_body_param')[0]
            message_head = eval(data_item['message_head'])
            data_len = int(message_head.get('Range', '2048').strip('\n').split(',')[-1])        #' 3X,6144'
            message_body_data = data_item['message_body_data'].tobytes()
            if data_item['message_body_param']:  #_lsa文件中，没有message_body_param部分数据，数据库中为None
                after_body_param = eval(data_item['message_body_param'])
                gain = int(after_body_param['Gain'])
            else:
                gain = 60
            data = list(struct.unpack("<%sh" % data_len, message_body_data))
            if len(data) == data_len:
                thick_mm = calThickness(data=data, gain_db=gain, nSize=data_len, version=version)
                print(thick_mm)
            else:
                thick_mm = -19.0
            thickness_dict[data_id_item] = thick_mm

        return thickness_dict

    def _MD5(self, file_obj):
            """MD5验证"""
            md_obj = hashlib.md5()
            md_obj.update(file_obj)
            md5_val = md_obj.hexdigest()
            return md5_val

class HandleImgs(object):
    """处理图片"""

    def __init__(self):
        pass

    def get_size(self, file):
        """获取文件大小：KB"""
        size = os.path.getsize(file)
        return size / 1024

    def get_outfile(self, infile, outfile):
        """拼接输出文件地址"""
        if outfile:
            return outfile
        dir, suffix = os.path.splitext(infile)
        outfile = '{}-out{}'.format(dir, suffix)
        return outfile

    def compress_image(self, infile, outfile='', mb=1024, step=10, quality=80):
        """不改变图片尺寸压缩到指定大小
        :param infile: 压缩源文件
        :param outfile: 压缩文件保存地址
        :param mb: 压缩目标，KB
        :param step: 每次调整的压缩比率
        :param quality: 初始压缩比率
        :return: 压缩文件地址，压缩文件大小
        """
        o_size = self.get_size(infile)
        if o_size <= mb:
            return infile
        outfile = self.get_outfile(infile, outfile)
        while o_size > mb:
            im = Image.open(infile)
            im.save(outfile, quality=quality)
            if quality - step < 0:
                break
            quality -= step
            o_size = self.get_size(outfile)
        # 删除原文件，修改新文件名称
        old_file_name = infile
        os.remove(infile)
        os.rename(outfile, old_file_name)

    def resize_image(self, infile, outfile='', x_s=1376):
        """修改图片尺寸
        :param infile: 图片源文件
        :param outfile: 重设尺寸文件保存地址
        :param x_s: 设置的宽度
        :return:
        """
        im = Image.open(infile)
        x, y = im.size
        y_s = int(y * x_s / x)
        out = im.resize((x_s, y_s), Image.ANTIALIAS)
        outfile = self.get_outfile(infile, outfile)
        out.save(outfile)



