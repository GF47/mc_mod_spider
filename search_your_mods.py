# !usr/bin/env python

import os
import zipfile
import yaml
import json
import re
import csv
import fuzzywuzzy.process

project_list = []
error_list = []


def fuzzy_finder(user_input, collection):
    """模糊查询"""
    return [x for x, _ in fuzzywuzzy.process.extract(user_input, collection)]


with open('config.yml', 'r') as f:
    config = yaml.load(f)
    mod_dir = config['mod_dir']
    mod_list = config['mod_list']

if os.path.exists(mod_dir):
    files = os.listdir(mod_dir)
    for f in files:
        if f.endswith('.jar'):
            zf = zipfile.ZipFile(mod_dir + '/' + f)
            if 'mcmod.info' in zf.namelist():
                mcmode_info = zf.open('mcmod.info').read()
                zf.close()

                try:
                    info_str = mcmode_info.replace(b'\n', b'').decode(encoding='utf-8')
                    info = json.loads(re.sub(r'\\x[0-9a-f]{2}', ' ', info_str))
                    if type(info) is dict:
                        project_list.append((info['modList'][0]['name'], f))
                    else:
                        project_list.append((info[0]['name'], f))
                except :
                    print(u'发生错误' + f)
                    error_list.append(f)
            else:
                error_list.append(f)

    with open('mod_dictionary.csv', 'r') as md:
        csv_data = csv.reader(md)
        mod_dict = [x for x, _, _ in csv_data]

    for i, item in enumerate(project_list):
        fuzzy_result = fuzzy_finder(item[0], mod_dict)
        result_str = '----------------------------------------------------------------'
        for j, result in enumerate(fuzzy_result):
            result_str += '\n{}    <{}>'.format(str(j), result)
        print(result_str)

        input_str = input(u'[<{}----{}>]的匹配结果为（按回车默认为0，空格回车为跳过）：'.format(item[0], item[1]))
        if input_str is '':
            input_value = 0
        elif input_str is ' ':
            input_value = -1
        else:
            try:
                input_value = int(input_str)
            except:
                input_value = -1

        if 0 <= input_value < len(fuzzy_result):
            project_list[i] = fuzzy_result[input_value]
            print(u'选择结果：{}    {}'.format(input_value, project_list[i]))
        else:
            project_list[i] = ''
            error_list.append(item[1])
            print(u'跳过')

    if os.path.exists(mod_list):
        os.remove(mod_list)
    with open(mod_list, 'w+') as ml:
        for _ in project_list:
            ml.writelines(_ + '\n')

    print('----------------------------------------------------------------')
    print(u'下列mod查询失败')
    print('----------------------------------------------------------------')
    for i in error_list:
        print(i)
    input_str = input(u'是否写入[error.txt]文件 y/n')
    if input_str is 'y':
        if os.path.exists('error.txt'):
            os.remove('error.txt')
        with open('error.txt', 'w+') as error_txt:
            for _ in error_list:
                error_txt.writelines(_ + '\n')
