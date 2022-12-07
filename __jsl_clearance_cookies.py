import hashlib
import re

import execjs
import requests


def get_cookie_value(js_params):
    """
        {'bts': ['1605668535.767|0|ZPy', 'wxR2KAnBdg7jW019YOsQGw%3D'], 'chars': 'YIHOVyegSIohjLTLmknBhl',
        'tn': '__jsl_clearance_s', 'wt': '1500', 'vt': '3600', 'ha': 'sha256',
        'ct': 'a0c4568766285c3b1fb83f40ed7503cd27e474f9a4c8539a6ff8a85a79884177'}
        :param bts:
        :param chars:
        :param tn:
        :param wt:
        :param vt:
        :param ha:
        :param ct:
        :return:
    """
    cl = js_params['chars']
    for i in cl:
        for j in cl:
            ij = js_params['bts'][0] + i + j + js_params['bts'][1]
            encrypts = eval("hashlib.{}(ij.encode('utf-8')).hexdigest()".format(js_params['ha']))
            if encrypts == js_params['ct']:
                __jsl_clearance = ij
    return __jsl_clearance

def _get_cookie_params():
    try:
        session = requests.Session()
        url = 'http://www.hfyaohai.gov.cn/index.html'
        response = session.get(url=url)
        cookies_dict = session.cookies.get_dict()
        cookie_text = re.findall("document\.cookie\=(.*);location", response.text)[0]
        js_code = """function getCookie(){{return {}}}""".format(cookie_text)
        ctx = execjs.compile(js_code)
        cookies = ctx.call('getCookie')
        k, v = cookies.split(";")[0].split("=")
        cookies_dict.update({k: v})
        session.cookies.update(cookies_dict)
        response = session.get(url=url)
        js_params = eval(re.findall(u";go\((.*?)\)</script", response.text)[0])
        __jsl_clearance = get_cookie_value(js_params)
        cookies_dict.update({"__jsl_clearance": __jsl_clearance})
        session.cookies.update(cookies_dict)
        response = session.get(url=url,cookies={"__jsl_clearance": __jsl_clearance})
        print(response.text)
    except Exception as e:
        print(e)
        pass
