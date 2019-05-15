# !/usr/bin/env python

import os
import sys
import urllib
import urllib.request
import urllib.error
import re
import yaml
import csv
import concurrent.futures

# 版本列表
VERSION_DICT = {
    '1.7.10': '2020709689:4449',
    '1.8.9': '2020709689:5806',
    '1.9.4': '2020709689:6084',
    '1.10.2': '2020709689:6170',
    '1.11.2': '2020709689:6452',
    '1.12.2': '2020709689:6756'
}

# list[mod_name, project_id, file_id, file_name]
LIST_MPF = []

user_agent_Mozilla = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:64.0) Gecko/20100101 Firefox/64.0'

def get_html(url, user_agent=user_agent_Mozilla, retries=2):
    """获取mod主页面"""
    headers = {'User-agent': user_agent}
    request = urllib.request.Request(url, headers=headers)
    try:
        html = urllib.request.urlopen(request).read()
    except urllib.error.URLError as e:
        print('urllib.error: ' + e.reason)
        print('error url:' + url)
        html = None
        if retries > 0:
            if hasattr(e, 'code') and 500 <= e.code < 600:
                return get_html(url, user_agent, retries - 1)
    return html


def _get_project_id(project_url):
    """获取mod项目id"""
    html = str(get_html(project_url))
    info = re.search(r'<div class="info-data">(.*?)</div>', html)
    return info.group(1)


def _get_file_id(project_url, version):
    """获取对应版本的mod文件id"""
    html = str(get_html(project_url + '/files?filter-game-version=' + version))
    info = re.search(r'class="button tip fa-icon-download icon-only" href="/projects/.*?/files/(\d*)/download"', html)
    file_id = info.group(1)

    html = str(get_html(project_url + '/files/' + file_id))
    info = re.search(r'<div class="info-label">Filename</div>(\\r\\n)?\s*<div class="info-data overflow-tip">(.*?)</div>', html)
    file_name = info.group(2)
    if not file_name.endswith('.jar'):
        file_name += '.jar'

    return file_id, file_name


def _save_full_info(project_url_root, project_name, mod_count, version):
    """保存一条完整的mod信息"""
    project_url = project_url_root + project_name
    project_id = _get_project_id(project_url)
    file_id, file_name = _get_file_id(project_url, version)

    LIST_MPF.append((project_name, project_id, file_id, file_name))

    sys.stdout.write(u'\r进度：%d%%' % (100 * len(LIST_MPF) / mod_count))
    sys.stdout.flush()


def get_mod_list():

    with open('config.yml', 'r') as y:
        config = yaml.load(y)

        project_url_root = config['project_url_root']
        old_list = config['old_list']
        new_list = config['new_list']
        # 读取并发数量
        max_thread_job = config['max_thread_job']
        mod_list_txt = config['mod_list']

    if os.path.exists(new_list):
        if os.path.exists(old_list):
            os.remove(old_list)
        os.rename(new_list, old_list)

    # 这里有个问题，有些mod是支持整个1.12大版本的，所以应该再适配一下1.12版本
    version = config['version']
    print(u'版本：' + version)
    version = VERSION_DICT[version]
    sys.stdout.write(u'\r进度：0%')

    with open(mod_list_txt, 'r') as mlt:
        mod_list = [x.strip('\n') for x in mlt.readlines()]  # 卡这好久，咩咩的还要去掉个换行符……

    mod_count = len(mod_list)
    with concurrent.futures.ThreadPoolExecutor(max_thread_job) as executor:
        for _ in mod_list:
            executor.submit(_save_full_info, project_url_root, _, mod_count, version)

    with open(new_list, 'w', encoding='utf-8', newline='') as nf:
        w = csv.writer(nf)
        w.writerow(['Url Name', 'Project ID', 'File ID', 'File Name'])
        for _ in LIST_MPF:
            w.writerow(_)


if __name__ == '__main__':
    get_mod_list()
