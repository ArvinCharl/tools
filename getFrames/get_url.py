import json
import hashlib
import traceback

import requests

requests.packages.urllib3.disable_warnings()


def get_camera_url(channel_id):
    rtspurl = ''
    # username_value = 'zhangqiubin'
    # passwd_value = 'Nihao123@'
    username_value = 'tyspjk'
    passwd_value = 'Tysp1357-'
    # s = requests.session()
    ip_port = '61.151.156.1:8282'  # 外网地址
    # ip_port = '10.200.1.71:8320'        # 内网地址
    content = {"userName": username_value, "clientType": "winpc"}
    headers = {"Content-Type": "application/json;charset=UTF-8", "User-Agent": "winpc"}
    try:
        # 第一次请求获取randomKey
        r = requests.post("https://" + ip_port + "/videoService/accounts/authorize", json=content, headers=headers,
                          timeout=10, verify=False)
        list = json.loads(r.text)
        randomKey_value = list['randomKey']
        realm_value = list['realm']
        passwd_value0 = hashlib.md5(passwd_value.encode('utf8'))
        passwd_value1 = hashlib.md5((username_value + passwd_value0.hexdigest()).encode('utf8'))
        passwd_tmp = hashlib.md5(passwd_value1.hexdigest().encode('utf8'))
        encrypted_passwd = hashlib.md5(
            (username_value + ':' + realm_value + ':' + passwd_tmp.hexdigest()).encode('utf8'))
        signature = hashlib.md5((encrypted_passwd.hexdigest() + ':' + randomKey_value).encode('utf8'))
        content2 = {"userName": username_value, "signature": signature.hexdigest(), 'randomKey': randomKey_value,
                    'encryptType': 'MD5', 'clientType': 'winpc'}

        # 第二次请求获取token
        r = requests.post("https://" + ip_port + "/videoService/accounts/authorize", json=content2, headers=headers,
                          timeout=10, verify=False)
        token = json.loads(r.text)['token']
        headers2 = {"Content-Type": "application/json;charset=UTF-8", "User-Agent": "winpc", "X-Subject-Token": token}

        # 获取分级组织
        # r = requests.get(
        #     "https://" + ip_port + "/videoService/devicesManager/deviceTree?id=&nodeType=1&typeCode=01",
        #     headers=headers2, timeout=10, verify=False)
        # print('获取分级组织: ', r.text)


        # # 获取通道信息
        # r = requests.get(
        #     "https://" + ip_port + "/videoService/devicesManager/deviceTree?id={}&nodeType=1&typeCode=01;1;ALL;ALL&page=1&pageSize=1000".format(
        #         id),
        #     headers=headers2, timeout=10, verify=False)
        # print('通道信息: ', r.text)

        # # 获取分级组织
        # r = requests.get(
        #     "https://" + ip_port + "/videoService/devicesManager/deviceTree?id=S4NbecfYB1BUD95HV6KTFO&nodeType=1&typeCode=01",
        #     headers=headers2, timeout=10, verify=False)
        # print('获取设备测试分级组织: ', r.text)
        #
        # id = json.loads(r.text)[1]['id']
        # # id = 'S4NbecfYB1CCSPHPTMVUN4'
        #
        # # 获取通道信息
        # r = requests.get(
        #     "https://" + ip_port + "/videoService/devicesManager/deviceTree?id={}&nodeType=1&typeCode=01;1;ALL;ALL&page=1&pageSize=1000".format(
        #         id),
        #     headers=headers2, timeout=10, verify=False)
        # print('通道信息: ', r.text)

        # 第三次请求获取rtspurl
        r = requests.get("https://" + ip_port + "/videoService/realmonitor/uri?channelId=" + channel_id,
                         headers=headers2, timeout=10, verify=False)
        rtspurl += json.loads(r.text)['url']
    except Exception as e:
        print('request error: ', traceback.print_exc())
        print('rtspurl: ', rtspurl)
        return rtspurl

    try:
        # 销毁本次会话
        content4 = {"token": token}
        r = requests.post("https://" + ip_port + "/videoService/accounts/unauthorize", json=content4,
                          headers=headers2,
                          timeout=10, verify=False)
        # print('销毁会话: ', r.text)
    except Exception as e:
        print('token destroy failed', e)

    print('rtspurl: ', rtspurl)
    return rtspurl


if __name__ == '__main__':
    # channel_ids = ['fMcmuLZbB1CRSOMNR07JF1', 'fMcmuLZbB1CRSOMNR1645L', 'fMcmuLZbB1CRSOMNQV9228']
    # channel_ids = ['fMcmuLZbB1CRSOMNQV9285']
    channel_ids = ['oLkDZT4BA1CIOTV0V99NKE']
    # channel_ids = ['xz46DizuB1CIOTV1C1S7U1', 'xz46DizuB1CIOTV1C1S81L', 'xz46DizuB1CIOTV1C1S86H']
    # channel_ids = ['xz46DizuB1CIOTV1C1S7U1']
    for channel_id in channel_ids:
        get_camera_url(channel_id)
