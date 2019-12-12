from django.shortcuts import render, redirect, HttpResponse
from apscheduler.schedulers.background import BackgroundScheduler
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.utils.safestring import mark_safe
from MeasureThickness.settings import Base_img_path
from utils.handel_data import *
from utils.layui_pager import LayuiPager
from utils import readfiles, file_type
from utils.readfiles import *
from django.views import View
from thickness import models
import json

handledataset = HandleDataSet()
handleimgs = HandleImgs()
file_count = 0


class TagManageView(View):
    """标签管理"""
    @method_decorator(csrf_exempt)  # CSRF Token相关装饰器在CBV只能加到dispatch方法上
    def dispatch(self, request, *args, **kwargs):
        return super(TagManageView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        file_tag_obj = models.DataTag.objects.values('id', 'file_name', 'tag_content').all().order_by('-id')

        for item in file_tag_obj:
            if item['tag_content']:
                tag_content_dict = eval(item['tag_content'])
                item['file_explain'] = tag_content_dict['file_explain']
                item['img_path'] = tag_content_dict['img_path']

        return render(request, "thickness/tag_manage.html", locals())

    def post(self, request, *args, **kwargs):
        result = {'status': False, 'message': None}
        try:
            inputValue = request.POST.get('inputValue')
            nid = request.POST.get('nid')
            img_obj = request.FILES.get('img_obj')
            tag_content = models.DataTag.objects.values('tag_content').filter(id=nid)[0]['tag_content']
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

                tag_content['file_explain'] = inputValue
                tag_content['img_path'] = '/' + Base_img_path + img_obj.name
            else:
                tag_content['file_explain'] = inputValue
                tag_content['img_path'] = old_img_path
            models.DataTag.objects.filter(id=nid).update(tag_content=tag_content)
            result = {'status': True, 'message': tag_content['img_path']}
        except Exception as e:
            print(e, '上传失败')

        return HttpResponse(json.dumps(result))

@csrf_exempt
def single_file_data(request, nid):
    """单个文件内的数据"""
    single_file_obj = models.DataFile.objects.values('nid', 'run_alg_thickness').filter(file_name_id=nid).all().order_by('nid')
    count = len(single_file_obj)
    file_obj = models.DataFile.objects.values('file_name_id', 'file_name__file_name').filter(file_name_id=nid).first()
    file_name = file_obj['file_name__file_name']
    file_id = file_obj['file_name_id']

    if request.method == "GET":
        return render(request, "thickness/single_file_list.html", locals())

    else:
        # 分页
        layui_pager = LayuiPager(request, single_file_obj)
        result = layui_pager.pager()

        return HttpResponse(json.dumps(result))


class UploadFileView(View):
    """上传文件"""

    @method_decorator(csrf_exempt)  # CSRF Token相关装饰器在CBV只能加到dispatch方法上
    def dispatch(self, request, *args, **kwargs):
        return super(UploadFileView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(request, "thickness/upload_file.html")

    def post(self, request, *args, **kwargs):
        result = {'status': False, 'code': 1, 'percent': 0, 'success_count': 0, 'file_fail_list': [], 'done_status': False}

        try:
            import time
            start = time.time()
            file_num = int(request.POST['file_num'])
            print('file_num', file_num)
            file = request.FILES['file']
            read_file = ReadFlies(file)
            success_count, file_fail_list = read_file.handle_files()
            print(success_count, file_fail_list)
            global file_count
            file_count += 1
            print('file_count', file_count)
            percent = round(file_count/file_num*100)
            print('percent', percent)
            done_status = False
            if file_count >= file_num:
                done_status = True

            result = {'status': True, 'code': 0, 'percent': percent, 'success_count': success_count, 'file_fail_list': file_fail_list, 'done_status': done_status}
            end = time.time()
            print('总用时%s' % (end-start))

        except Exception as e:
            print(e, '上传失败')

        return HttpResponse(json.dumps(result))


def callback_zero(request):
    """上传文件的回调清零"""
    global file_count
    file_count = 0
    readfiles.success_count = 0
    file_type.file_fail_list = []
    result = {'status': True, 'message': 'success'}
    return HttpResponse(json.dumps(result))


class GenerateDataSetView(View):
    """生成数据集"""

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(GenerateDataSetView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        i = 0
        data_time_list = []
        data_time_temp = []
        #{"value": "1", "title": "2019-09-20"}

        time_list = models.DataFile.objects.all().values('create_time').distinct()
        for item in time_list:
            data_time_temp.append(str(item['create_time']))
        data_time_temp = sorted(data_time_temp)    #['2019-09-20', '2019-09-21', '2019-09-22', '2019-09-23']
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
        """生成数据集html代码"""
        ele = ''
        script = """layui.use('slider', function(){
                      var slider = layui.slider;"""
        selected_data = json.loads(request.POST.get('selected_data'))
        # print('selected_data', selected_data)
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
                    """ % (item['title'], item['title'], item['title'],  item['title'], item['title'])

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
                              });""" % (item['title'], start_id, end_id, item['title'], item['title'], )
            script += "});"
                # param_list.append({'time': item['title'], 'start_id': start_id, 'end_id': end_id})
            result = {'status': True, 'message': mark_safe(ele), 'script': mark_safe(script)}

        return HttpResponse(json.dumps(result))


@csrf_exempt
def generate_dataset_ajax(request):
    """取出选中数据的时间和id范围，去数据库中取出数据id,并把数据id持久化"""
    result = {'status': False, 'message': '生成id数据集失败'}
    try:
        import time
        result_list = []
        input_list = json.loads(request.POST.get('input_list'))  #['2019-09-18', '', '', '2019-09-08', '', '', '2019-09-19', '', '', '2019-09-17', '', '']
        for i in range(0, len(input_list), 3):
            result_list.append(input_list[i: i+3])
        # print(result_list)  #[['2019-09-20', '5', '7'], ]        range(4,12)   choose(5,7)
        #取出已选中的数据id
        choose_dataset_id_list = handledataset.get_selected_data(result_list)    #[5, 6, 7, 20, 21]
        #存入数据库
        if choose_dataset_id_list:
            start = time.time()
            models.DataSetCondition.objects.create(time_and_id=result_list, data_set_id=choose_dataset_id_list)
            end = time.time()
            print('use time:', end - start)
            result = {'status': True, 'message': '生成id数据集成功'}

    except Exception as e:
        print(e, "def(generate_dataset_ajax)出错")

    return HttpResponse(json.dumps(result))

@csrf_exempt
def dataset_condition_list(request):
    """数据集条件列表"""
    all_dataset = models.DataSetCondition.objects.all().values('id', 'time_and_id').order_by('-id')
    count = len(all_dataset)
    if request.method == "GET":
        return render(request, 'thickness/dataset_condition_list.html', locals())
    else:
        # 分页
        layui_pager = LayuiPager(request, all_dataset)
        result = layui_pager.pager()

        return HttpResponse(json.dumps(result))


@csrf_exempt
def single_dataset_list(request, nid):
    """单个数据集列表"""
    data_time_condition_obj = models.DataSetCondition.objects.filter(id=nid).values('time_and_id', 'data_set_id', 'thickness')[0]
    data_set_id = eval(data_time_condition_obj['data_set_id'])
    data_time = eval(data_time_condition_obj['time_and_id'])  # [['2019-09-20', '10', '11'], ['2019-09-21', '13', '15']]
    thickness_dict = data_time_condition_obj['thickness']       # str  {1: 40.058, 2: 40.058, 3: 40.058}

    if thickness_dict == None:  # 如果该数据集暂未计算厚度值
        thickness_dict = "{}"
    else:
        thickness_dict = eval(thickness_dict)  # {1: 40.058, 2: 40.058, 3: 40.058}

    # 填充列表
    data_list = []
    for item in data_time:
        for i in range(int(item[1]), int(item[2])+1):  # 数据集中单个日期的数据id范围
            if thickness_dict != "{}":
                thickness = thickness_dict[i]
            else:
                thickness = ''
            time = item[0]
            data_id = i
            data_list.append({'time': time, 'data_id': data_id, 'thickness': thickness})  #[{'time': '2019-09-20', 'data_id': 4, 'thickness': 39.028}, {'time': '2019-09-20', 'data_id': 5, 'thickness': 40.058}, {'time': '2019-09-20', 'data_id': 6, 'thickness': 38.012}]

    count = len(data_list)

    if request.method == "GET":
        return render(request, 'thickness/single_dataset_list.html', locals())
    else:
        # 分页
        layui_pager = LayuiPager(request, data_list)
        result = layui_pager.pager()

        return HttpResponse(json.dumps(result))


@csrf_exempt
def dataset_run_alg_ajax(request):
    """跑算法算出 数据集 厚度值"""
    result = {'status': False, 'message': '算法执行失败'}
    try:
        import time
        start = time.time()
        nid = request.POST.get('nid')
        data_set_id_obj = models.DataSetCondition.objects.filter(id=nid).values('data_set_id')
        data_set_id_list = eval(data_set_id_obj[0]['data_set_id'])
        thickness_dict = handledataset.handle_data_and_run_alg(data_set_id_list)  # 处理数据集数据并跑算法
        models.DataSetCondition.objects.filter(id=nid).update(thickness=thickness_dict)
        result = {'status': True, 'message': '算法执行成功'}
        end = time.time()
        print('alg use time:', (end - start))
    except Exception as e:
        print(e, "跑算法出错！")
    return HttpResponse(json.dumps(result))\


@csrf_exempt
def single_file_run_alg_ajax(request):
    """单个文件跑算法得出厚度值"""
    result = {'status': False, 'message': '算法执行失败'}
    try:
        data_id_list = []
        file_id = request.POST.get('file_id')
        data_id_dict = models.DataFile.objects.values('nid').filter(file_name_id=file_id)
        for item in data_id_dict:
            data_id_list.append(item['nid'])
        thickness_dict = handledataset.handle_data_and_run_alg(data_id_list)  # 处理单个文件数据并跑算法
        for k, v in thickness_dict.items():
            models.DataFile.objects.filter(nid=k).update(run_alg_thickness=v)

        result = {'status': True, 'message': '算法执行成功'}

    except Exception as e:
        print(e, "跑算法出错！")
    return HttpResponse(json.dumps(result))


@csrf_exempt
def remove_dataset_ajax(request):
    """删除数据集"""
    result = {'status': False, 'message': '删除数据集失败'}
    try:
        nid = request.POST.get('nid')
        models.DataSetCondition.objects.filter(id=nid).delete()
        result = {'status': True, 'message': '删除数据集成功'}
    except Exception as e:
        print(e, "删除数据集出错！")
    return HttpResponse(json.dumps(result))


def data_2048_chart(request, nid, thickness):
    """单条数据波形图和详细信息"""
    data_obj = models.DataFile.objects.filter(nid=nid).values('message_body_data', 'message_head', 'create_time', 'message_body_param', 'file_name_id')[0]
    #处理数据
    message_head = eval(data_obj['message_head'])
    data_len = int(message_head.get('Range', '2048').strip('\n').split(',')[-1])  # ' 3X,6144'
    message_body_data = data_obj['message_body_data'].tobytes()
    data = list(struct.unpack("<%sh" % data_len, message_body_data))
    if data_obj['message_body_param']:
        message_body_param = eval(data_obj['message_body_param'])
    else:
        message_body_param = ""
    #传给前端的数据
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


def clear_repeat_imgs():
    """清理重复图片"""
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

try:
    """定时初始化"""
    scheduler = BackgroundScheduler()
    scheduler.add_job(clear_repeat_imgs, 'cron', day_of_week='0,2,4', hour='10', id='cron_time')
    scheduler.start()

except Exception as e:
    print('err:', e)
    scheduler.shutdown()


@csrf_exempt
def test(request):
    # if request.method == 'POST':
    #     file = request.FILES.getlist('fd')
    #     print(file.name)
    #     print(file.size)
    # return HttpResponse('...')
    return render(request, 'test.html')