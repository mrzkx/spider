import requests
import re
def unsbox(arg1):
    box = [15,35,29,24,33,16,1,38,10,9,19,31,40,27,22,23,25,13,6,11,39,18,20,8,14,21,32,26,2,30,7,4,17,5,3,28,34,37,12,36]
    res = list(range(0, len(arg1)))
    for i in range(0, len(arg1)):
        j = arg1[i]
        for k in range(0, 40):
            if box[k] == i + 1:
                res[k] = j
    res = "".join(res)
    return res


def hexXor(arg2):
    box = "3000176000856006061501533003690027800375"
    res = ""
    for i in range(0, 40, 2):
        arg_H = int(arg2[i : i + 2], 16)
        box_H = int(box[i : i + 2], 16)
        res += hex(arg_H ^ box_H)[2:].zfill(2)
    return res
def get_acw_sc_v2(arg1):
    return hexXor(unsbox(arg1))
response = requests.get(url='')
arg1 = re.findall("var\s*arg1=\'(.*?)\';", response.text.encode('utf-8'), re.S)[0]
acw_sc__v2 = get_acw_sc_v2(arg1)
response.cookies.update({'acw_sc__v2': acw_sc__v2})