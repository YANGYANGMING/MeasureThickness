from django.db import models


class DataFile(models.Model):
    """文件数据"""
    nid = models.AutoField(primary_key=True)
    create_time = models.DateField(auto_now_add=True)
    message_head = models.TextField(blank=True, null=True)
    message_body_data = models.BinaryField(blank=True, null=True)
    message_body_param = models.TextField(blank=True, null=True)
    # run_alg_thickness = models.FloatField(blank=True, null=True)
    true_thickness = models.FloatField(blank=True, null=True)
    file_name = models.ForeignKey('DataTag', on_delete=models.CASCADE)


class DataSetCondition(models.Model):
    """筛选出来的数据集"""
    create_time = models.DateField(auto_now_add=True)
    time_and_id = models.TextField(blank=True, null=True)
    data_set_id = models.TextField(blank=True, null=True)
    dataset_tag = models.TextField(blank=True, null=True)


class DataTag(models.Model):
    """数据tag"""
    file_name = models.TextField(blank=True, null=True)
    tag_content = models.TextField(blank=True, null=True, default={'file_explain': '', 'img_path': '/static/default-imgs/default.png'})
    md5_val = models.TextField(blank=True, null=True)


class VersionToThcikness(models.Model):
    """版本号对应其测出的厚度值"""
    data_id = models.ForeignKey(to='DataFile', to_field='nid', on_delete=models.CASCADE)
    version = models.ForeignKey(to='Version', to_field='id', on_delete=models.CASCADE)
    run_alg_thickness = models.FloatField(blank=True, null=True)
    deviation = models.FloatField(blank=True, null=True)


class Version(models.Model):
    """版本号"""
    version = models.CharField(max_length=64, unique=True)



