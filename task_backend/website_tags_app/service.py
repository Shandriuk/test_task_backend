import requests
import re
import random

def random_6_chars():
    ascii = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'

    result = ""
    for i in range(6):
        result += ascii[round(random.random() * (len(ascii)-1))]
    return result

def html_tag_searching(url):
    result = {}
    if 'http' in url:
        return None
    try:
        link = "https://" + url
        req = requests.get(link, timeout=0.1)
    except :
        link = "http://" + url
        req = requests.get(link)
    if req.status_code == 200:
        content = req.text
        find = re.findall(r"<(\w+) ?", content)
        for elem in find:
            if elem is not result.keys():
                result[elem] = find.count(elem)
        return result
    return None

def parcing_phone(query_string):
    parcing_phone = re.search(r"phone=([^&]+)", query_string)
    if parcing_phone != None:
        parcing_phone = parcing_phone.group(1)
    else:
        parcing_phone = None

    return parcing_phone

def parcing_qs(query_string):
    link = re.search(r"link=([^&]+)", query_string)
    if link !=None:
        link = link.group(1)
    else:
        link = None

    tags = re.search(r"tags=([^&]+)", query_string)
    if tags!=None:
        tags = tags.group(1)
        tags = tags.split(",")
    else:
        tags = None
    return link, tags

def difference_in_dicts(dict1, dict2):
    result = {"is_correct": False}
    result["difference"] = {}
    keys1 = dict1.keys()
    keys2 =dict2.keys()
    for key in keys1:
        if key not in keys2:
            result["difference"][key] = dict1[key]
        elif dict1[key] != dict2[key]:
            result["difference"][key] = abs(dict1[key] - dict2[key])
    for key in keys2:
        if key not in keys1:
            result["difference"][key] = dict2[key]
        elif dict2[key] != dict1[key]:
            result["difference"][key] = abs(dict1[key] - dict2[key])
    return result
