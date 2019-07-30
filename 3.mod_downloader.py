# !usr/bin/env python

import os
import csv
import urllib
import urllib.request
import urllib.error
import concurrent.futures
import yaml

TEMP_MOD_PATH = os.getcwd() + '/tmp/mods'

with open('config.yml', 'r') as y:
    config = yaml.load(y)

    file_list = config['file_list']
    project_url_root = config['project_url_root']
    max_thread_job = config['max_thread_job']
    user_agent = config['user_agent']

def _read_csv(path):
    """读取csv文件"""
    if os.path.exists(path):
        with open(path, 'r') as f:
            csv_list = list(csv.reader(f))
            return csv_list
    return None


def _downloader(url, user_agent, file_name):
    """
    下载文件
    :param url: 文件地址
    :param file_name: 文件名称
    :return: 下载成功与否
    """
    print(u'下载：' + url)
    try:
        opener = urllib.request.build_opener()
        opener.addheaders=[('User-Agent', user_agent)]
        urllib.request.install_opener(opener)
        urllib.request.urlretrieve(url, file_name)
        flag = True
    except urllib.error.URLError as e:
        print(url + u'下载错误：' + e.reason)


def _download_mod(url_root, user_agent, project_id, file_id, file_name):
    """
    下载mod文件
    """
    # curseforge改版后存储位置发生了变化 https://media.forgecdn.net/files/file_id前4位/file_id后3位/file_name
    # url = url_root + '/' + file_id[0:4] + '/' + file_id[4:] + '/' + file_name
    url = url_root + '/' + project_id + '/download/' + file_id + '/file'
    file_path = TEMP_MOD_PATH + '/' + file_name
    _downloader(url, user_agent, file_path)


def main():
    # 临时存放mod的文件夹
    if not os.path.exists(TEMP_MOD_PATH):
        os.makedirs(TEMP_MOD_PATH)

    fl = _read_csv(file_list)

    if fl:
        with concurrent.futures.ThreadPoolExecutor(max_thread_job) as executor:
            for i in fl:
                executor.submit(_download_mod, project_url_root, user_agent, i[1], i[2], i[3])


if __name__ == '__main__':
    main()
