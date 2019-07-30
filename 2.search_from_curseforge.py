# !usr/bin/env python


import os
import sys
import yaml
import csv
import urllib
import urllib.request
import urllib.error
import re


# 版本列表
VERSION_DICT = {
        '1.7.10': '2020709689:4449',
        '1.8.9': '2020709689:5806',
        '1.9.4': '2020709689:6084',
        '1.10.2': '2020709689:6170',
        '1.11.2': '2020709689:6452',
        '1.12.2': '2020709689:6756'
        }


with open('config.yml', 'r') as f:
    config = yaml.load(f)
    project_url_root = config['project_url_root']
    mod_list = config['mod_list']
    project_list = config['project_list']
    file_list = config['file_list']
    user_agent_default = config['user_agent']


def get_html(url, user_agent=user_agent_default, retries=2):
    """通过地址获取网页"""
    headers = {'User-agent': user_agent}
    request = urllib.request.Request(url, headers=headers)
    try:
        html = urllib.request.urlopen(request).read()
    except urllib.error.URLError as e:
        print('urllib.error:{0}\nerror url:{1}\n'.format(e.reason, url))
        html = None
        if retries > 0:
            if hasattr(e, 'code') and 500 <= e.code < 600:
                return get_html(url, user_agent, retries - 1)
    return html


def _project_searcher(name):
    """负责在curseforge上按mod名称查找对应项目页"""
    html = str(get_html('{0}/search?search={1}'.format(project_url_root, name.replace(' ', '+'))))
    project_names = re.finditer(r'<a class="my-auto" href="/minecraft/mc-mods/(.*?)">\\r\\n\s*<h3 class=".*?">(.*?)</h3>', html)
    print("--------------------------------[{0}]的匹配项：--------------------------------".format(name))
    result = []
    for i,v in enumerate(project_names):
        result.append(v.group(1))
        print('{0}{1}. [ {2}----{3} ]\n'.format('\t' * i, i + 1, v.group(1), v.group(2)))
    print("----------------------------------------------------------------")
    return result


def _file_searcher(project, version):
    """在curseforge的项目页下查找对应版本的文件id和文件名"""
    html = str(get_html('{0}/{1}/files/all?filter-game-version={2}'.format(project_url_root, project, version)))
    file_id = re.search(r'<a data-action="file-link" href="/minecraft/mc-mods/.*?/files/(\d+)">.*?</a>', html)
    if file_id:
        html = str(get_html('{0}/{1}/files/{2}'.format(project_url_root, project, file_id.group(1))))
        file_name = re.search(r'<span class="font-bold text-sm leading-loose">Filename</span>\\r\\n\s*<span class="text-sm">(.*?)</span>', html)
        if file_name:
            return file_id.group(1), file_name.group(1)

    return None, None


def _search_project_by_name(name):
    """查找项目名称的交互界面"""

    search_result = _project_searcher(name)

    while True:
        input_str = input("请输入匹配的序号，[ 回车 ]默认为[ 1 ]，[ 空格 ]则跳过放弃，[ rs ]手动输入关键字并重新搜索：")
        if input_str == '':
            input_value = 0
            break
        elif input_str == ' ':
            input_value = -1
            break
        elif input_str.strip() == 'rs':
            fixed_name = input("请重新输入[ {0} ]的名称：\n".format(name))
            search_result = _project_searcher(fixed_name)
        else:
            input_value = int(input_str) - 1 if input_str.isdigit() else -1
            if 0 <= input_value < len(search_result):
                break

    result = search_result[input_value] if 0 <= input_value < len(search_result) else ''
    print("[ {0} ]的匹配项为[ {1} ]\n".format(name, result))
    return result


def _search_file_by_version(version='1.12.2'):
    version_code = VERSION_DICT[version]

    sys.stdout.write(u'\r当前抓取的mod：')

    with open(project_list, 'r') as pl:
        csv_data = csv.reader(pl)
        if os.path.exists(file_list):
            os.remove(file_list)
        with open (file_list, 'w+') as fl:
            for i,p in csv_data:
                file_info = _file_searcher(p, version_code)
                fl.write('{0},{1},{2},{3}\n'.format(i, p, file_info[0], file_info[1]))
                sys.stdout.write(u'\r                                                                \r当前抓取的mod：' + i)



with open(mod_list, 'r') as ml:
    input_str = input("""----------------------------------------------------------------
* 刷新mod列表请按[ 1 ]
* 刷新mod版本请按[ 2 ]
---------------------------------------------------------------""")

    if input_str == '1':

        csv_data = csv.reader(ml)

        if os.path.exists(project_list):
          os.remove(project_list)
        with open(project_list, 'w+') as pl:
          for i,n,_,_ in csv_data:
              pl.write('{0},{1}\n'.format(i, _search_project_by_name(n)))

    elif input_str == '2':

        _search_file_by_version()

    else:
        pass

