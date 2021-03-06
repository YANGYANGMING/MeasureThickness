from django.shortcuts import render, HttpResponse
from apscheduler.schedulers.background import BackgroundScheduler
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from MeasureThickness.settings import Base_img_path
from django.utils.safestring import mark_safe
from django.db.models import Q
from django.http import JsonResponse
from django.core.cache import cache
from decimal import Decimal
from utils.handel_data import *
from utils import readfiles
from utils import file_type
from utils import auth
from utils.readfiles import *
from django.views import View
from thickness import models
import random
import json

scheduler = BackgroundScheduler()
handledataset = HandleDataSet()
handleimgs = HandleImgs()
file_count = 0


@login_required
@csrf_exempt
def tag_manage(request):
    """
    标签管理
    :param request:
    :return:
    """
    file_tag_obj = models.DataTag.objects.values('id', 'file_name', 'tag_content', 'create_time').all().order_by('-id')
    count = file_tag_obj.count()
    try:
        version = select_version()
        for item in file_tag_obj:
            file_id = item['id']
            true_thickness = get_most_true_thickness(file_id)
            item['true_thickness'] = true_thickness
            item['create_time'] = str(item['create_time']).split('.')[0]
            if item['tag_content']:
                tag_content_dict = eval(item['tag_content'])
                item['file_explain'] = tag_content_dict['file_explain']
                item['img_path'] = tag_content_dict['img_path']
    except:
        pass
    if request.method == "GET":
        return render(request, "thickness/tag_manage.html", locals())

    if request.method == "POST":
        # 分页
        result = pager(request, file_tag_obj)
        result['data_list'] = result['data_list']
        return HttpResponse(json.dumps(result))


@csrf_exempt
def tag_manage_save_ajax(request):
    """
    退出保存
    :param request:
    :return:
    """
    result = {'status': False, 'message': None}
    try:
        file_explain = request.POST.get('file-explain')
        file_id = request.POST.get('nid')
        true_thickness = request.POST.get('true-thickness')
        if true_thickness == 'null' or true_thickness == '':
            pass
        else:
            # 重跑算法
            restart_run_alg(file_id, true_thickness)

        img_obj = request.FILES.get('img_obj')
        tag_content = models.DataTag.objects.values('tag_content').filter(id=file_id)[0]['tag_content']
        if tag_content:
            tag_content = eval(tag_content)
            old_img_path = tag_content['img_path']
        else:
            tag_content = {}
            old_img_path = ''
        if img_obj:
            # 写 && 压缩 图片
            with open(Base_img_path + img_obj.name, 'wb') as f:
                f.write(img_obj.read())
            handleimgs.compress_image(Base_img_path + img_obj.name)

            tag_content['file_explain'] = file_explain
            tag_content['img_path'] = '/' + Base_img_path + img_obj.name
        else:
            tag_content['file_explain'] = file_explain
            tag_content['img_path'] = old_img_path

        models.DataTag.objects.filter(id=file_id).update(tag_content=tag_content)
        result = {'status': True, 'message': tag_content['img_path']}
    except Exception as e:
        print(e, '上传失败')

    return HttpResponse(json.dumps(result))


@login_required
def restart_run_alg(file_id, true_thickness):
    """
    修改整个文件的手测厚度值后，每个版本算法来重跑算法
    :param file_id: 文件ID
    :param true_thickness: 手测厚度值
    :return:
    """
    prev_true_thickness = get_most_true_thickness(file_id)
    # 如果true_thickness更改，需要重跑算法
    if prev_true_thickness != float(true_thickness):
        models.DataFile.objects.filter(file_name_id=file_id).update(true_thickness=true_thickness)
        version_obj = models.Version.objects.values('version').all().order_by('-id')[:5]
        version_list = [version['version'] for version in version_obj]
        data_id_list = models.DataFile.objects.values('nid').filter(file_name_id=file_id)
        data_id_list = [item['nid'] for item in data_id_list]   # int
        handle_alg_process(data_id_list, version_list, only_run_alg=False)


@csrf_exempt
def generate_dataset_by_file_ajax(request):
    """
    通过文件生成数据集
    :param request:
    :return:
    """
    try:
        time_and_id = []
        data_set_id = []
        selected_data_id_list = eval(request.POST.get('selected_data_id_list'))
        if selected_data_id_list:
            for file_id in selected_data_id_list:
                create_time = str(
                    models.DataFile.objects.values('create_time').filter(file_name_id=file_id)[0]['create_time'])
                temp_id = models.DataFile.objects.values('nid').filter(file_name_id=file_id)
                first_id = temp_id.first()['nid']
                last_id = temp_id.last()['nid']
                time_and_id_temp = [create_time, first_id, last_id]
                time_and_id.append(time_and_id_temp)
                for item in temp_id:
                    data_set_id.append(item['nid'])
            # 存储数据集条件
            models.DataSetCondition.objects.create(time_and_id=time_and_id, data_set_id=data_set_id)

            result = {'status': True, 'message': '成功生成数据集'}
        else:
            result = {'status': False, 'message': '生成数据集失败'}
    except Exception as e:
        result = {'status': False, 'message': '生成数据集失败'}
        print(e)

    return HttpResponse(json.dumps(result))


@csrf_exempt
def remove_file_ajax(request):
    """
    删除文件
    :param request:
    :return:
    """
    try:
        selected_file_id_list = eval(request.POST.get('selected_file_id_list'))
        if selected_file_id_list:
            for file_id in selected_file_id_list:
                models.DataTag.objects.filter(id=file_id).delete()

        result = {'status': True, 'message': '删除文件成功'}

    except Exception as e:
        result = {'status': False, 'message': '删除文件失败'}
        print(e)

    return HttpResponse(json.dumps(result))


@csrf_exempt
def search_file_ajax(request):
    """
    按文件tag搜索
    :param request:
    :return:
    """
    try:
        search_value = request.POST.get('search_value')
        q = Q()
        q.connector = "OR"
        q.children.append(("tag_content__contains", search_value))
        search_obj = list(models.DataTag.objects.filter(q).values('id', 'file_name', 'tag_content', 'create_time').order_by('-id'))
        for item in search_obj:
            file_id = item['id']
            true_thickness = models.DataFile.objects.values('true_thickness').filter(file_name_id=file_id)[0][
                'true_thickness']
            item['true_thickness'] = true_thickness
            item['create_time'] = str(item['create_time']).split('.')[0]
            if item['tag_content']:
                tag_content_dict = eval(item['tag_content'])
                item['file_explain'] = tag_content_dict['file_explain']
                item['img_path'] = tag_content_dict['img_path']

        result = {'status': True, 'message': 'success', 'data_list': search_obj}

    except Exception as e:
        result = {'status': False, 'message': 'fail', 'data_list': []}
        print(e)

    return HttpResponse(json.dumps(result))


@login_required
@csrf_exempt
def single_file_data(request, file_id, version):
    """
    单个文件的数据列表
    :param request:
    :param file_id: 文件ID
    :param version: 算法版本
    :return:
    """
    # 从session中获取selected_version
    data_type = "file"
    selected_version = request.session.get('selected_version')
    if not selected_version:  # 如果没有选择版本，默认使用最新版本
        selected_version = select_version()
    version_obj = models.Version.objects.values('version').order_by('-id')
    data_obj = models.DataFile.objects.filter(file_name_id=file_id).order_by('nid')
    count = data_obj.count()
    try:
        file_obj = data_obj.values('file_name__file_name').first()
        file_name = file_obj['file_name__file_name']
        # file_id = file_obj['file_name_id']
    except:
        pass

    if request.method == "GET":
        return render(request, "thickness/single_file_list.html", locals())

    elif request.method == "POST":
        # 分页
        result = pager(request, data_obj)

        single_file_obj = []
        for item in result['data_list']:
            try:
                versionTothcikness_obj = \
                item.versiontothcikness_set.filter(version__version=selected_version).values('data_id',
                                                                                             'version__version',
                                                                                             'run_alg_thickness')[0]
            except:  # 如果该数据没有跑算法
                versionTothcikness_obj = {}
                versionTothcikness_obj['data_id'] = item.nid
                versionTothcikness_obj['version__version'] = selected_version
                versionTothcikness_obj['run_alg_thickness'] = None
            true_thickness = \
            models.DataFile.objects.values('true_thickness').filter(nid=versionTothcikness_obj['data_id'])[0][
                'true_thickness']
            versionTothcikness_obj['true_thickness'] = true_thickness
            single_file_obj.append(versionTothcikness_obj)
            result['data_list'] = single_file_obj
        return HttpResponse(json.dumps(result))


@csrf_exempt
def single_file_run_alg_ajax(request):
    """
    跑算法得出 单个文件 厚度值
    :param request:
    :return:
    """
    result = {'status': False, 'message': '算法执行失败'}
    try:
        file_id = request.POST.get('file_id')
        selected_version = request.POST.get('version')
        request.session['selected_version'] = selected_version
        version_list = [selected_version]
        data_id_dict = models.DataFile.objects.values('nid').filter(file_name_id=file_id)
        data_id_list = []
        for item in data_id_dict:
            data_id_list.append(item['nid'])
        t1 = time.time()
        # 跑算法
        print(data_id_list)
        handle_alg_process(data_id_list, version_list, only_run_alg=True)
        t2 = time.time()
        print('文件算法时间：', t2 - t1)
        result = {'status': True, 'message': '算法执行成功'}

    except Exception as e:
        print(e, "单个文件跑算法出错！")
    return HttpResponse(json.dumps(result))


@login_required
@csrf_exempt
def dataset_condition_list(request):
    """
    数据集条件列表
    :param request:
    :return:
    """
    all_dataset_obj = models.DataSetCondition.objects.all().order_by('-id')
    count = all_dataset_obj.count()
    try:
        version_obj = models.Version.objects.values('version').order_by('-id')
        # 从session中获取selected_version
        selected_version = request.session.get('selected_version')
        if not selected_version:
            selected_version = select_version()
    except:
        pass

    if request.method == "GET":
        return render(request, 'thickness/dataset_condition_list.html', locals())
    else:
        # 分页
        result = pager(request, all_dataset_obj)
        result['data_list'] = list(result['data_list'].values('id', 'time_and_id', 'dataset_tag'))
        return HttpResponse(json.dumps(result))


@csrf_exempt
def save_dataset_tag_ajax(request):
    """
    保存数据集tag
    :param request:
    :return:
    """
    result = {'status': False, 'message': ''}
    try:
        dataset_id = request.POST.get('dataset_id')
        dataset_tag = request.POST.get('dataset-tag')
        models.DataSetCondition.objects.filter(id=dataset_id).update(dataset_tag=dataset_tag)
        result = {'status': True, 'message': '数据集tag修改成功'}
    except Exception as e:
        print(e)

    return HttpResponse(json.dumps(result))


@login_required
@csrf_exempt
def single_dataset_list(request, dataset_id):
    """
    单个数据集列表
    :param request:
    :param dataset_id: 数据集ID
    :return:
    """
    data_type = "data_set"
    version_obj = models.Version.objects.values('version').order_by('-id')
    data_time_condition_obj = models.DataSetCondition.objects.filter(id=dataset_id).values('time_and_id', 'data_set_id')[0]
    data_set_id = eval(data_time_condition_obj['data_set_id'])
    data_id_list = true_data_id_list(data_set_id)
    print('data_id_list', data_id_list)
    count = len(data_id_list)
    # 从session中获取selected_version
    selected_version = request.session.get('selected_version')
    if not selected_version:
        selected_version = select_version()

    if request.method == "GET":
        return render(request, 'thickness/single_dataset_list.html', locals())
    elif request.method == "POST":
        # 分页
        result = pager(request, data_id_list)
        # 填充列表
        data_list = []
        for data_id in result['data_list']:
            try:  # 防止删除了文件中的某条数据，导致报错
                true_thickness = models.DataFile.objects.values('true_thickness').get(nid=data_id)['true_thickness']
                data_obj = models.DataFile.objects.get(nid=data_id)
                run_alg_thickness_obj = data_obj.versiontothcikness_set.filter(
                    version__version=selected_version).values('run_alg_thickness')
                if run_alg_thickness_obj:  # 如果该数据已跑算法，取出算法厚度值
                    run_alg_thickness = run_alg_thickness_obj[0]['run_alg_thickness']
                else:
                    run_alg_thickness = None
                data_list.append(
                    {'data_id': data_id, 'run_alg_thickness': run_alg_thickness, 'true_thickness': true_thickness})

            except Exception as e:
                pass
            result['data_list'] = data_list

        return HttpResponse(json.dumps(result))


def true_data_id_list(id_list):
    """
    查找所有的存在的数据id，防止删除了文件或者部分数据，已存储的数据集中的数据列表中的id不对
    :param id_list: 要查询的数据id列表
    :return:
    """
    # id_list = list(list_to_str_tuple(id_list))
    # print(id_list)
    data_id_list = []
    # data_id_list_obj = models.DataFile.objects.raw("select nid from thickness_datafile where nid in %s" % id_list)
    data_id_list_obj = models.DataFile.objects.filter(nid__in=id_list)
    for i in data_id_list_obj:
        data_id_list.append(i.nid)
    return data_id_list


@csrf_exempt
def dataset_run_alg_ajax(request):
    """
    跑算法算出 数据集 厚度值
    :param request:
    :return:
    """
    result = {'status': False, 'message': '算法执行失败'}
    try:
        import time
        tt1 = time.time()
        dataset_id = request.POST.get('dataset_id')
        selected_version = request.POST.get('selected_version')
        version_list = [selected_version]
        data_set_id_obj = models.DataSetCondition.objects.filter(id=dataset_id).values('data_set_id')
        data_id_list = eval(data_set_id_obj[0]['data_set_id'])
        handle_alg_process(data_id_list, version_list, only_run_alg=True)
        tt2 = time.time()
        print('数据集跑算法时间：', tt2 - tt1)
        result = {'status': True, 'message': '算法执行成功'}
    except Exception as e:
        print(e, "跑算法出错！")
    return HttpResponse(json.dumps(result))


def handle_alg_process(data_id_list, version_list, only_run_alg):
    """
    处理算法过程
    :param data_id_list: 要跑算法的数据id列表
    :param version_list: 选择的版本列表
    :return:
    """
    # data_id_list = list_to_str_tuple(data_id_list)
    for version_item in version_list:
        # print('version_item', version_item)
        update_data_id_set = set()
        version_id = models.Version.objects.values('id').get(version=version_item)['id']
        # data_id_list_obj = models.VersionToThcikness.objects.raw(
        #     "select id, data_id_id, run_alg_thickness from thickness_versiontothcikness where data_id_id in %s and version_id=%s order by data_id_id" % (
        #     data_id_list, version_id))
        data_id_list_obj = models.VersionToThcikness.objects.filter(data_id_id__in=data_id_list, version_id=version_id).order_by('data_id_id')
        print('data_id_list_obj', data_id_list_obj)
        # 用于update
        update_devation(data_id_list_obj, version_item, version_id, update_data_id_set, only_run_alg)
        # 需要创建的数据id列表
        create_data_id_set = set(data_id_list) - update_data_id_set
        print('create_data_id_set', create_data_id_set)
        # 用于create
        create_run_alg_thickness_and_devation(create_data_id_set, version_item, version_id)


def update_devation(data_id_list_obj, version_item, version_id, update_data_id_set, only_run_alg):
    """
    only_run_alg=False：用于更新已跑算法的厚度差
    only_run_alg=True：用于更新已跑算法的厚度差和重新计算出run_alg_thickness
    :param data_id_list_obj: 所选的所有数据对象
    :param version_id: 版本id
    :param update_data_id_set: 需要更新的数据id列表
    :return:
    """
    for data_item in data_id_list_obj:
        try:
            data_id = data_item.data_id_id
            # 如果没有跑算法，直接except-->create_data_id_set.add(data_id)，结束后会对其进行create操作
            run_alg_thickness = data_item.run_alg_thickness
            # print('run_alg_thickness', run_alg_thickness)
            update_data_id_set.add(data_id)

            true_thickness = models.DataFile.objects.values('true_thickness').get(nid=data_id)['true_thickness']
            if not true_thickness:
                true_thickness = 0

            # 如果only_run_alg==True，表示所有选中的数据都要跑一遍算法，重新计算出run_alg_thickness
            if only_run_alg:
                thickness_dict = handledataset.handle_data_and_run_alg([data_id, data_id], version_item)
                run_alg_thickness = thickness_dict[data_id]
            # 保留一位小数
            deviation = export_result(abs(Decimal(str(true_thickness)) - Decimal(str(run_alg_thickness))))
            temp_dict = {'run_alg_thickness': run_alg_thickness, 'deviation': deviation}
            models.VersionToThcikness.objects.filter(data_id=data_id, version=version_id).update(**temp_dict)
            print('update', version_item, data_id)
        except:
            pass


def create_run_alg_thickness_and_devation(data_id_list, version_item, version_id):
    """
    用于创建没有跑算法的算法厚度值和厚度差
    :param data_id_list: 需要创建的数据id列表
    :param version_item: 版本名
    :param version_id: 版本id
    :return:
    """
    # print('create_data_id_set', create_data_id_set)
    # 计算厚度差，并创建deviation和run_alg_thickness
    if data_id_list:
        thickness_dict = handledataset.handle_data_and_run_alg(list(data_id_list), version_item)  # 把没有跑算法的数据去跑算法
        # print('thickness_dict', thickness_dict)
        for data_id in data_id_list:
            try:
                true_thickness = models.DataFile.objects.values('true_thickness').get(nid=data_id)['true_thickness']
                if not true_thickness:
                    true_thickness = 0
                run_alg_thickness = thickness_dict[data_id]
                deviation = export_result(abs(Decimal(str(true_thickness)) - Decimal(str(run_alg_thickness))))  # 保留一位小数
                temp_dict = {'data_id_id': data_id, 'run_alg_thickness': run_alg_thickness,
                             'version_id': version_id, 'deviation': deviation}
                models.VersionToThcikness.objects.create(**temp_dict)
                # print('create', version_item, data_id)
            except:
                pass


@csrf_exempt
def select_version_ajax(request):
    """
    选择版本号，设置session值
    :param request:
    :return:
    """
    result = {'status': False, 'message': None}
    try:
        select_version = request.POST.get('version')
        request.session['selected_version'] = select_version
        result = {'status': True, 'message': 'success'}
    except Exception as e:
        print(e)
    return HttpResponse(json.dumps(result))


@csrf_exempt
def batch_save_true_thickness_ajax(request):
    """
    批量保存手测厚度值
    :param request:
    :return:
    """
    try:
        true_thickness = float(request.POST.get('true_thickness'))
        selected_data_id_list = eval(request.POST.get('selected_data_id_list'))

        for nid in selected_data_id_list:
            prev_true_thickness = models.DataFile.objects.values('true_thickness').filter(nid=nid)[0][
                'true_thickness']
            # 如果true_thickness更改，需要重跑算法
            if prev_true_thickness != true_thickness:
                print('重跑')
                models.DataFile.objects.filter(nid=nid).update(true_thickness=true_thickness)
                version_obj = models.Version.objects.values('version').all().order_by('-id')[:5]
                version_list = [version['version'] for version in version_obj]
                data_id_list = [int(nid), int(nid)]  # 后面用到的数据库查询语句where XX in (1,2)，不能只有一个条件
                handle_alg_process(data_id_list, version_list, only_run_alg=False)

        result = {'status': True, 'message': '批量设置成功'}
    except Exception as e:
        result = {'status': False, 'message': '厚度值类型错误，正确类型为：浮点型'}
        # print(e)
    return HttpResponse(json.dumps(result))


@csrf_exempt
def remove_data_ajax(request):
    """
    删除数据
    :param request:
    :return:
    """
    try:
        selected_data_id_list = eval(request.POST.get('selected_data_id_list'))
        for nid in selected_data_id_list:
            models.DataFile.objects.filter(nid=nid).delete()
            print(nid)
        result = {'status': True, 'message': '删除成功'}
    except Exception as e:
        result = {'status': False, 'message': '删除失败'}
        # print(e)
    return HttpResponse(json.dumps(result))


@csrf_exempt
def remove_dataset_ajax(request):
    """
    删除数据集
    :param request:
    :return:
    """
    result = {'status': False, 'message': '删除数据集失败'}
    try:
        dataset_id = request.POST.get('dataset_id')
        models.DataSetCondition.objects.filter(id=dataset_id).delete()
        result = {'status': True, 'message': '删除数据集成功'}
    except Exception as e:
        print(e, "删除数据集出错！")
    return HttpResponse(json.dumps(result))


def data_2048_chart(request, data_id, thickness):
    """
    单条数据波形图和详细信息
    :param request:
    :param data_id: 数据ID
    :param thickness: 跑算法的厚度值
    :return:
    """
    data_obj = models.DataFile.objects.values('message_body_data', 'message_head', 'create_time',
                                              'message_body_param', 'file_name_id',
                                              'true_thickness').get(nid=data_id)
    # 处理数据
    message_head = eval(data_obj['message_head'])
    data_len = int(message_head.get('Range', '2048').strip('\n').split(',')[-1])  # ' 3X,6144'
    message_body_data = data_obj['message_body_data'].tobytes()
    data = list(struct.unpack("<%sh" % data_len, message_body_data))
    if data_obj['message_body_param']:
        message_body_param = eval(data_obj['message_body_param'])
    else:
        message_body_param = ""
    # 传给前端的数据
    true_thickness = data_obj['true_thickness']
    data_list = json.dumps(list(enumerate(data)))
    create_time = str(data_obj['create_time'])
    file_name_id = data_obj['file_name_id']
    data_tag_obj = models.DataTag.objects.values('tag_content', 'file_name').filter(id=file_name_id)[0]
    tag_content_obj = data_tag_obj['tag_content']
    file_name = data_tag_obj['file_name']
    if tag_content_obj:
        file_explain = eval(tag_content_obj)['file_explain']
        img_path = eval(tag_content_obj)['img_path']
    else:
        img_path = ''
        file_explain = ''

    return render(request, 'thickness/data_2048_chart.html', locals())


class UploadFileView(View):
    @method_decorator(csrf_exempt)  # CSRF Token相关装饰器在CBV只能加到dispatch方法上
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(UploadFileView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        """
        上传文件
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        return render(request, "thickness/upload_file.html")

    def post(self, request, *args, **kwargs):
        """
        读取文件并处理文件数据，数据库持久化，
        计算成功存储数据条数、成功存储文件个数，
        显示存储失败文件名列表
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        result = {'status': False, 'code': 1, 'percent': 0, 'success_count': 0, 'file_fail_list': [],
                  'done_status': False}
        try:
            import time
            start = time.time()
            file_num = int(request.POST['file_num'])
            # print('file_num', file_num)
            file = request.FILES['file']
            read_file = ReadFlies(file)
            success_count, file_fail_list = read_file.handle_files()
            # print(success_count, file_fail_list)
            global file_count
            file_count += 1
            # print('file_count', file_count)
            percent = round(file_count / file_num * 100)
            # print('percent', percent)
            done_status = False
            if file_count >= file_num:
                done_status = True

            result = {'status': True, 'code': 0, 'percent': percent, 'success_count': success_count,
                      'file_fail_list': file_fail_list, 'done_status': done_status}
            end = time.time()
            print('总用时%s' % (end - start))

        except Exception as e:
            print(e, '上传失败')

        return HttpResponse(json.dumps(result))


def callback_zero(request):
    """
    上传文件的回调清零
    :return:
    """
    try:
        global file_count
        file_count = 0
        readfiles.success_count = 0
        file_type.file_fail_list = []
        result = {'status': True, 'message': 'success'}
    except Exception as e:
        print(e)
        result = {'status': False, 'message': 'false'}
    return HttpResponse(json.dumps(result))


class GenerateDataSetView(View):
    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(GenerateDataSetView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        """
        生成数据集
        :param request:
        :return:
        """
        i = 0
        data_time_list = []
        data_time_temp = []
        # {"value": "1", "title": "2019-09-20"}

        time_list = models.DataFile.objects.all().values('create_time').distinct()
        for item in time_list:
            data_time_temp.append(str(item['create_time']))
        data_time_temp = sorted(data_time_temp)  # ['2019-09-20', '2019-09-21', '2019-09-22', '2019-09-23']
        data_time_temp.reverse()

        for data_time in data_time_temp:
            i += 1
            data_time_dict = {}
            data_time_dict['value'] = str(i)
            data_time_dict['title'] = data_time
            data_time_list.append(data_time_dict)
        data_time_list = json.dumps(data_time_list)
        # print(data_time_list)  #[{"value": "1", "title": "2019-09-08"}, {"value": "2", "title": "2019-09-17"}]
        choice_data_time_list = data_time_list

        return render(request, 'thickness/generate_dataset.html', locals())

    def post(self, request):
        """
        生成数据集html代码
        :param request:
        :return:
        """
        ele = ''
        script = """layui.use('slider', function(){
                      var slider = layui.slider;"""
        selected_data = json.loads(request.POST.get('selected_data'))
        print('selected_data', selected_data)
        if selected_data == []:
            result = {'status': False, 'message': ele}
        else:
            for item in selected_data:
                start_id = models.DataFile.objects.filter(create_time=item['title']).values('nid').first()['nid']
                end_id = models.DataFile.objects.filter(create_time=item['title']).values('nid').last()['nid']
                ele += """
                        <div style="width: 120px; height: 30px; margin-top: 30px; margin-left: 10px">
                            <input type="text"id="data-time" value="%s" disabled style="line-height: 30px; border: none; background-color: white">
                        </div>
                        <div style="margin-top: -15px; width:500px; margin-left: 120px">
                            <div id="slide-%s" class="demo-slider"></div>
                            <div id="slider-tips-%s" style=" left: 30px; margin-top: 10px;"></div>
                            <input type="text" style="display: none;" id="first-id-%s" value="">
                            <input type="text" style="display: none;" id="second-id-%s" value="">
                        </div>
                    """ % (item['title'], item['title'], item['title'], item['title'], item['title'])

                script += """
                          slider.render({
                            elem: '#slide-%s'
                            //,value: 40 //初始值
                            ,range: true //范围选择
                            ,min: %s
                            ,max: %s
                            ,input: true
                            ,change: function(value) {
                                  $('#first-id-%s').val(value[0]);
                                  $('#second-id-%s').val(value[1]);
                                  }
                              });""" % (item['title'], start_id, end_id, item['title'], item['title'],)
            script += "});"
            # param_list.append({'time': item['title'], 'start_id': start_id, 'end_id': end_id})
            result = {'status': True, 'message': mark_safe(ele), 'script': mark_safe(script)}

        return HttpResponse(json.dumps(result))


@csrf_exempt
def generate_dataset_ajax(request):
    """
    取出选中数据的时间和id范围，去数据库中取出数据id,并把数据id持久化
    :param request:
    :return:
    """
    result = {'status': False, 'message': '生成id数据集失败'}
    try:
        import time
        result_list = []
        input_list = json.loads(request.POST.get(
            'input_list'))  # ['2019-09-18', '', '', '2019-09-08', '', '', '2019-09-19', '', '', '2019-09-17', '', '']
        for i in range(0, len(input_list), 3):
            result_list.append(input_list[i: i + 3])
        print(result_list)  # [['2019-09-20', '5', '7'], ]        range(4,12)   choose(5,7)
        # 制作数据集时如果没有滑动滑条选取数据，默认选取当前日期的第一条数据
        for data_item in result_list:
            if data_item[1] == '' and data_item[2] == '':
                nid = int(models.DataFile.objects.filter(create_time=data_item[0]).values('nid')[0]['nid'])
                data_item[1] = data_item[2] = nid
        # 取出已选中的数据id
        choose_dataset_id_list = handledataset.get_selected_data(result_list)  # choose_dataset_id_list = [5, 6, 7, 20, 21]
        # 存入数据库
        if choose_dataset_id_list:
            start = time.time()
            models.DataSetCondition.objects.create(time_and_id=result_list, data_set_id=choose_dataset_id_list)
            end = time.time()
            print('use time:', end - start)
            result = {'status': True, 'message': '生成id数据集成功'}

    except Exception as e:
        print(e, "def(generate_dataset_ajax)出错")

    return HttpResponse(json.dumps(result))


class DeviationRate(View):
    """
    显示柱状图偏差率
    """
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(DeviationRate, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        version_obj = models.Version.objects.values('version').order_by('-id')
        nid = args[0]  # 数据集id或者文件id
        data_type = args[1]
        return render(request, 'thickness/deviation_rate.html', locals())


@csrf_exempt
def deviation_rate_ajax(request, nid, data_type):
    """
    显示数据集偏差率ajax
    :param request:
    :param nid: 数据集id或者文件id
    :return:
    """
    try:
        data_id_list = []
        selected_version_list = request.POST.get('version').split(',')
        if data_type == "data_set":
            data_id_list = eval(models.DataSetCondition.objects.values('data_set_id').get(id=nid)['data_set_id'])
            # data_id_list = list_to_str_tuple(data_id_list)
        elif data_type == "file":
            data_id_list = models.DataFile.objects.values('nid').filter(file_name_id=nid)
            data_id_list = [i['nid'] for i in data_id_list]
            # data_id_list = list_to_str_tuple(data_id_list)

        result = handle_deviation_rate(data_id_list, selected_version_list, nid)

    except Exception as e:
        result = {'status': False, 'message': 'false', 'data_list': []}

    return HttpResponse(json.dumps(result))


def handle_deviation_rate(data_id_list, selected_version_list, nid):
    """
    处理显示偏差率的数据
    :param data_id_list: 待处理的数据id列表
    :param selected_version_list: 选择待显示版本
    :param nid: 数据集id或者文件id
    :return:
    """
    data_list = []
    for version_item in selected_version_list:
        deviation_range = {0.0: 0, 0.1: 0, 0.2: 0, 0.3: 0, 0.4: 0, 0.5: 0, 0.6: 0, 0.7: 0, 0.8: 0, 0.9: 0, 1.0: 0}
        data_id_and_deviation = {}
        data_id_and_devation_dict = {}
        version_id = models.Version.objects.values('id').get(version=version_item)['id']
        try:  # 批量查找
            # dataset_id_list_obj = models.VersionToThcikness.objects.raw(
            #     "select id, data_id_id, deviation from thickness_versiontothcikness where data_id_id in %s and version_id=%s order by data_id_id" % (
            #         data_id_list, version_id))
            dataset_id_list_obj = models.VersionToThcikness.objects.filter(data_id_id__in=data_id_list, version_id=version_id).order_by('data_id_id')
            for data_item in dataset_id_list_obj:
                data_id = data_item.data_id_id
                deviation = data_item.deviation
                data_id_and_deviation[data_id] = deviation
        except:
            pass
        data_id_and_devation_dict[version_item] = data_id_and_deviation
        for k_data_id, v_deviation_item in data_id_and_devation_dict[version_item].items():
            judge_range = deviation_range.get(v_deviation_item)
            if judge_range or judge_range == 0:
                deviation_range[v_deviation_item] = deviation_range[v_deviation_item] + 1
            else:
                deviation_range[1.0] = deviation_range[1.0] + 1
        # print(deviation_range)
        cache.set('data_id_and_devation_dict_' + version_item + '_' + nid, data_id_and_devation_dict, 600)
        cache.set('deviation_range_' + version_item + '_' + nid, deviation_range, 600)
        deviation_num = [v for k, v in deviation_range.items()]
        data_list.append({'name': version_item, 'data': deviation_num})

    result = {'status': True, 'message': 'success', 'data_list': data_list}
    return result


@csrf_exempt
def column_click_event_ajax(request, nid):
    """
    柱状图点击事件
    :param request:
    :param nid: 数据集id或者文件id
    :return:
    """
    selected_data_id = []
    version = request.POST.get('version')
    deviation = request.POST.get('deviation')
    data_id_and_devation_dict = cache.get('data_id_and_devation_dict_' + version + '_' + nid)
    deviation_range = cache.get('deviation_range_' + version + '_' + nid)
    if data_id_and_devation_dict and deviation_range:  # 如果有缓存
        selected_deviation = deviation.split('-')[0]
        for k, v in data_id_and_devation_dict[version].items():
            if float(selected_deviation) == 1.0:
                if v >= 1.0:
                    selected_data_id.append(k)
            if float(selected_deviation) == v and float(selected_deviation) != 1.0:
                selected_data_id.append(k)
        # 分页
        result = pager(request, selected_data_id)
        # 填充列表
        data_list = []
        for data_id in result['data_list']:
            try:  # 防止删除了文件中的某条数据，导致报错
                true_thickness = models.DataFile.objects.values('true_thickness').get(nid=data_id)[
                    'true_thickness']
                data_obj = models.DataFile.objects.get(nid=data_id)
                run_alg_thickness_obj = data_obj.versiontothcikness_set.filter(
                    version__version=version).values('run_alg_thickness')
                if run_alg_thickness_obj:  # 如果该数据已跑算法，取出算法厚度值
                    run_alg_thickness = run_alg_thickness_obj[0]['run_alg_thickness']
                else:
                    run_alg_thickness = None
                data_list.append({'data_id': data_id, 'version': version, 'run_alg_thickness': run_alg_thickness,
                                  'true_thickness': true_thickness})

            except:
                pass

        result = {'status': True, 'message': 'have cache', 'data_list': data_list}
    else:
        result = {'status': False, 'message': 'no cache', 'data_list': []}

    return HttpResponse(json.dumps(result))


@csrf_exempt
def submit_true_thickness(request):
    """
    提交设置手测厚度
    :param request:
    :return:
    """
    try:
        true_thickness = float(request.POST.get('true_thickness'))
        data_id = request.POST.get('nid')

        prev_true_thickness = models.DataFile.objects.values('true_thickness').filter(nid=data_id)[0][
            'true_thickness']
        # 如果true_thickness更改，需要重跑算法
        if prev_true_thickness != true_thickness:
            print('重跑')
            models.DataFile.objects.filter(nid=data_id).update(true_thickness=true_thickness)
            version_obj = models.Version.objects.values('version').all().order_by('-id')[:5]
            version_list = [version['version'] for version in version_obj]
            data_id_list = [int(data_id), int(data_id)]  # 后面用到的数据库查询语句where XX in (1,2)，不能只有一个条件
            handle_alg_process(data_id_list, version_list, only_run_alg=False)

        result = {'status': True, 'message': '设置成功'}
    except Exception as e:
        result = {'status': False, 'message': '数据格式有误'}
        print(e)

    return HttpResponse(json.dumps(result))


class AlgAPI(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(AlgAPI, self).dispatch(request, *args, **kwargs)

    # def get(self, request, *args, **kwargs):
    #     print(request.GET)
    #     response = {'status': True, 'data': ['V-2.0', 'V-3.0']}
    #     return JsonResponse(response)

    @method_decorator(auth.alg_api_auth)
    def post(self, request, *args, **kwargs):
        """
        算法api：接收算法api发送过来的更新的算法信息
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        alg_info = json.loads(request.body.decode('utf-8'))
        print(alg_info)

        result = {'status': True, 'message': None}

        return JsonResponse(result)


def pager(request, data_obj):
    """
    分页
    :param request:
    :param data_obj: 要分页的数据对象
    :return:
    """
    result = {'status': False, 'data_list': []}
    limit = int(request.POST.get('limit'))  # 每页显示的条数
    curr_page = int(request.POST.get('curr_page'))
    # print(limit)
    # print(curr_page)
    if curr_page == 1:
        start_range = curr_page - 1
        end_range = curr_page * limit
    else:
        start_range = (curr_page - 1) * limit
        end_range = curr_page * limit
    result['data_list'] = data_obj[start_range: end_range]
    result['status'] = True
    return result


def page_404(request):
    """
    404页面
    :param request:
    :return:
    """
    return render(request, 'thickness/404.html')


def clear_repeat_imgs():
    """
    清理重复图片
    :return:
    """
    db_img_set = set()
    tag_content_obj = models.DataTag.objects.values('tag_content').all()
    for item in tag_content_obj:
        if item['tag_content']:
            img_path = eval(item['tag_content'])['img_path']
            if img_path != '':
                img_name = os.path.split(img_path)[1]
                db_img_set.add(img_name)
    local_img_set = set(os.listdir(Base_img_path))
    repeat_imgs = local_img_set - db_img_set
    for repeat_img in repeat_imgs:
        os.remove(Base_img_path + repeat_img)


def export_result(num):
    """
    不四舍五入保留1位小数
    :param num: 要处理的浮点数
    :return: 保留一位小数并且不丢失精度
    """
    num_x, num_y = str(num).split('.')
    num = float(num_x + '.' + num_y[0:1])
    return num


def list_to_str_tuple(id_list):
    """
    id列表转字符串形式元组
    :param id_list: 要处理的列表
    :return: 字符串形式的元组
    """
    if len(id_list) == 1:  # 只有一个查询id的情况下
        id_list = [id_list[0], id_list[0]]
    id_list = str(tuple(id_list))
    return id_list


def get_most_true_thickness(file_id):
    """
    一个文件中一般都是同一个手测的厚度值，但是也有可能有个别数据是其他手测厚度，
    所以为了显示当前文件的手测厚度值，需要找出sample_list中出现最多的手测厚度数据，
    以代表当前文件数据的手测厚度
    :param file_id: 文件id
    :return:
    """
    true_thickness_obj = models.DataFile.objects.values('true_thickness').filter(file_name_id=file_id)
    random.shuffle(list(true_thickness_obj))
    sample_list = [item['true_thickness'] for item in true_thickness_obj[:20]]
    # 找出sample_list中出现最多的数据
    true_thickness = showmax(sample_list)

    return true_thickness


def showmax(sample_list):
    """
    找出出现次数最多的手测厚度值
    :param sample_list:
    :return:
    """
    index1 = 0  # 记录出现次数最多的元素下标
    max_num = 0  # 记录最大的元素出现次数
    for i in range(len(sample_list)):
        flag = 0  # 记录每一个元素出现的次数
        for j in range(i + 1, len(sample_list)):  # 遍历i之后的元素下标
            if sample_list[j] == sample_list[i]:
                flag += 1  # 每当发现与自己相同的元素，flag+1
        if flag > max_num:  # 如果此时元素出现的次数大于最大值，记录此时元素的下标
            max_num = flag
            index1 = i
    return sample_list[index1]


def select_version():
    """
    选择版本号，并判断版本号是否存在
    :return:
    """
    selected_version_obj = models.Version.objects.values('version').last()
    if selected_version_obj:
        selected_version = selected_version_obj['version']
    else:
        selected_version = 'None'
    return selected_version


try:
    """定时初始化"""
    scheduler.add_job(clear_repeat_imgs, 'cron', day_of_week='0,2,4', hour='10', id='cron_time')
    scheduler.start()
except Exception as e:
    print('err:', e)
    scheduler.shutdown()


@csrf_exempt
def test(request):
    t1 = time.time()

    t2 = time.time()
    print(t2 - t1)
    return render(request, 'test.html')
