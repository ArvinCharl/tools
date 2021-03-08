import json
import hashlib
import traceback

import requests


def get_camera_url(channel_id):
    rtspurl = ''
    username_value = 'zhangqiubin'
    passwd_value = 'Nihao123@'
    s = requests.session()
    content = {"userName": username_value, "clientType": "winpc"}
    headers = {"Content-Type": "application/json;charset=UTF-8", "User-Agent": "winpc"}
    try:
        # r = requests.post("https://10.200.1.71:8320/videoService/accounts/authorize", json=content, headers=headers,
        #                   timeout=10, verify=False)
        r = requests.post("https://61.151.156.1:8282/videoService/accounts/authorize", json=content, headers=headers,
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
        # r = requests.post("https://10.200.1.71:8320/videoService/accounts/authorize", json=content2, headers=headers,
        #                   timeout=10, verify=False)
        r = requests.post("https://61.151.156.1:8282/videoService/accounts/authorize", json=content2, headers=headers,
                          timeout=10, verify=False)
        token = json.loads(r.text)['token']
        headers2 = {"Content-Type": "application/json;charset=UTF-8", "User-Agent": "winpc", "X-Subject-Token": token}
        # r = requests.get("https://10.200.1.71:8320/videoService/realmonitor/uri?channelId=" + channel_id,
        #                  headers=headers2, timeout=10, verify=False)
        r = requests.get("https://61.151.156.1:8282/videoService/realmonitor/uri?channelId=" + channel_id,
                         headers=headers2, timeout=10, verify=False)
        rtspurl += json.loads(r.text)['url']
    except Exception as e:
        print('request error: ', traceback.print_exc())
        print('rtspurl: ', rtspurl)
        return rtspurl

    try:
        content4 = {"token": token}
        # r = requests.post("https://10.200.1.71:8320/videoService/accounts/unauthorize", json=content4,
        #                   headers=headers2,
        #                   timeout=10, verify=False)
        r = requests.post("https://61.151.156.1:8282/videoService/accounts/unauthorize", json=content4,
                          headers=headers2,
                          timeout=10, verify=False)
        print(r)
    except Exception as e:
        print('token destroy failed', e)

    print('rtspurl', rtspurl)
    return rtspurl


if __name__ == '__main__':
    channel_ids = ['xz46DizuB1CIOTV1C1S7U1', 'xz46DizuB1CIOTV1C1S81L', 'xz46DizuB1CIOTV1C1S86H',
                       'xz46DizuB1CIOTV1C1S870', 'xz46DizuB1CIOTV1C1S8DH', 'xz46DizuB1CIOTV1C1S8I5',
                       'xz46DizuB1CIOTV1C2QP7B', 'xz46DizuB1CIOTV1C2QP8G']
    for channel_id in channel_ids:
        get_camera_url(channel_id)
