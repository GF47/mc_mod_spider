@echo off
echo ��ȡ���µ�mod��Ϣ
python mod_info.py
echo.
echo �Աȱ���mod��Ϣ�������и��µ�mod�����洢�ڡ�tmp/mods���ļ�����
python mod_downloader.py
set /p a=�������������
