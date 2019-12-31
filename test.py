import time
import requests

alg_data = {'status': True,
        'message': 'alg message',
        'data': {'alg_version': 'V-3.0',
                  'upload_time': '2020-01-01 12:00:00',
                  'address': 'www.baidu.com'},
        'error': None}

import hashlib

def auth_key():
    """
    接口认证
    :return:
    """
    key = '2990-95cc-1330-11e5-b06a-a45e-60be-c08b'
    key_name = 'auth-key'
    ha = hashlib.md5(key.encode('utf-8'))  # 加盐
    time_span = time.time()
    ha.update(bytes("%s|%f" % (key, time_span), encoding='utf-8'))
    encryption = ha.hexdigest()
    result = "%s|%f" % (encryption, time_span)
    print({key_name: result})
    return {key_name: result}


def post_alg(alg_data):
    """
    post方式向接口提交算法信息
    :param msg:
    :return:
    """
    status = True
    try:
        headers = {}
        headers.update(auth_key())
        response = requests.post(
            url='http://127.0.0.1:8000/thickness/alg-api/',
            headers=headers,
            json=alg_data,
            data={'k2': 'v2'},
            params={'k1': 'v1'},
        )
    except Exception as e:
        response = e
        status = False
    print('status', status)
    print('response', response)


def get_asset():
    """
    get方式
    """
    try:
        headers = {}
        headers.update(auth_key())
        response = requests.get(
                url='http://127.0.0.1:8000/thickness/alg-api/',
                headers=headers,
                data={'k2': 'v2'},
                params={'k1': 'v1'},

        )
    except Exception as e:
        response = e
    print(response)


if __name__ == '__main__':
    post_alg(alg_data)
    # get_asset()
