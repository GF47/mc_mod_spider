# !usr/bin/env python

import os
import zipfile
import yaml
import json
import re
import csv


error_list = []
project_list = []

with open('config.yml', 'r') as f:
    config = yaml.load(f)
    mod_dir = config['mod_dir']
    mod_list =  config['mod_info']

if os.path.exists(mod_dir):
    files = os.listdir(mod_dir)
    for f in files:
        if f.endswith('.jar'):
            zf = zipfile.ZipFile(mod_dir + '/' + f)
            if 'mcmod.info' in zf.namelist():
                mcmod_info = zf.open('mcmod.info').read()
                zf.close()

                try:
                    info_str = mcmod_info.replace(b'\n', b'').decode(encoding='utf-8')
                    info = json.loads(re.sub(r'\\x[0-9a-f]{2}', ' ', info_str))
                    if type(info) is dict:
                        project_list.append((info['modList'][0]['name'], f))
                    else:
                        project_list.append((info[0]['name'], f))
                except:
                    print(u'error:' + f)
                    project_list.append(('', f))
                    error_list.append(f)
            else:
                error_list.append(f)
    if os.path.exists(mod_list):
        os.remove(mod_list)
    with open(mod_list, 'w+') as ml:
        for m,f in project_list:
            ml.writelines(m + ',' + f + '\n')

print('----------------错误列表----------------------------------------')
for _ in error_list:
    print(_)
print('----------------------------------------------------------------')
