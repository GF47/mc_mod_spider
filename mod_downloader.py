# !usr/bin/env python

import csv
import urllib
import urllib.request
import urllib.error
import os
import concurrent.futures
import yaml

TEMP_MOD_PATH = os.getcwd() + '/tmp/mods'


def _read_csv(path):
    """读取csv文件"""
    if os.path.exists(path):
        with open(path, 'r') as f:
            csv_list = list(csv.reader(f))
            return csv_list
    return None


def _get_different_mods(old, new):
    """比较两个list的数据，找出新list中更改过的"""
    list_different = []
    if old is None:
        new.pop(0)  # 第一行是列类型说明
        return new
    for _ in new:
        if _ not in old and _[2] is not None:
            list_different.append(_)

    return list_different


def _download_file(url, file_name):
    """
    下载文件
    :param url: 文件地址
    :param file_name: 文件名称
    :return: 下载成功与否
    """
    print(u'下载：' + url)
    try:
        opener = urllib.request.build_opener()
        opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:64.0) Gecko/20100101 Firefox/64.0')]
        urllib.request.install_opener(opener)
        urllib.request.urlretrieve(url, file_name)
    except urllib.error.URLError as e:
        print(u'下载错误' + e.reason)
        return False
    return True


def _download_mod(project_url_root, project_name, file_id, file_name):
    """
    下载mod文件
    :param project_url_root: 网站项目根目录
    :param project_name: mod项目名称
    :param file_id: 最新的符合版本的mod文件id
    :param file_name: mod文件名
    :return: none
    """
    url = '{}{}/files/{}/download'.format(project_url_root, project_name, file_id)
    file_path = '{}/{}'.format(TEMP_MOD_PATH, file_name)
    _download_file(url, file_path)


def _make_temp_mod_dir():
    """临时存放mod的文件夹"""
    if not os.path.exists(TEMP_MOD_PATH):
        os.makedirs(TEMP_MOD_PATH)


def download():
    _make_temp_mod_dir()

    with open('config.yml', 'r') as y:
        config = yaml.load(y)

        project_url_root = config['project_url_root']
        old_list = config['old_list']
        new_list = config['new_list']
        max_thread_job = config['max_thread_job']

    mod_list_2b_download = _get_different_mods(_read_csv(old_list), _read_csv(new_list))
    with concurrent.futures.ThreadPoolExecutor(max_thread_job) as executor:
        for _ in mod_list_2b_download:
            executor.submit(_download_mod, project_url_root, _[0], _[2], _[3])


if __name__ == '__main__':
    download()
