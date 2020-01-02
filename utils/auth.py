import time
import hashlib
from MeasureThickness.settings import ALG_AUTH_KEY
from MeasureThickness.settings import ALG_AUTH_HEADER_NAME
from MeasureThickness.settings import ALG_AUTH_TIME
from django.http import JsonResponse


encrypt_list = [
    # {'encrypt': encrypt, 'time': timestamp
]


def api_auth_method(request):
    """
    接口认证
    :param request:
    :return:
    """
    auth_key = request.META.get(ALG_AUTH_HEADER_NAME)
    # print('auth_key', auth_key)
    if not auth_key:
        return False
    sp = auth_key.split('|')
    # print(sp)
    if len(sp) != 2:
        return False
    encrypt, timestamp = sp
    timestamp = float(timestamp)
    limit_timestamp = time.time() - ALG_AUTH_TIME
    # print(limit_timestamp, timestamp)
    # 检查时间是否超时
    if limit_timestamp > timestamp:
        return False
    # 验证
    ha = hashlib.md5(ALG_AUTH_KEY.encode('utf-8'))
    ha.update(bytes("%s|%f" % (ALG_AUTH_KEY, timestamp), encoding='utf-8'))
    result = ha.hexdigest()
    # print(result, encrypt)
    if encrypt != result:
        print('失败')
        return False
    # 检查列表中已经存在，并且对已经失效的列表元素进行清除
    exist = False
    del_keys = []
    for k, v in enumerate(encrypt_list):
        # print(k, v)
        m = v['time']
        n = v['encrypt']
        if m < limit_timestamp:
            del_keys.append(k)
            continue
        if n == encrypt:
            exist = True
    for k in del_keys:
        del encrypt_list[k]

    if exist:
        return False
    encrypt_list.append({'encrypt': encrypt, 'time': timestamp})
    return True


def alg_api_auth(func):
    def inner(request, *args, **kwargs):
        if not api_auth_method(request):
            return JsonResponse({'code': 1001, 'message': 'API授权失败'}, json_dumps_params={'ensure_ascii': False})
        return func(request, *args, **kwargs)

    return inner