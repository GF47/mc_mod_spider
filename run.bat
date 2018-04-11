@echo off
echo 爬取最新的mod信息
python mod_info.py
echo.
echo 对比本地mod信息，下载有更新的mod，并存储在【tmp/mods】文件夹中
python mod_downloader.py
set /p a=请输入任意键：
