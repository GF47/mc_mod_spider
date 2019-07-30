
# mc_mod_spider
用来将minecraft的mod自动同步到curseforge的最新版本。
顺带练手爬虫。

---

## 功能
* 扫描已经安装的mod，将列表存储在 *mod_list.txt* 中。
* 爬取curseforge的mod信息，将下载后的mod文件存储在 *tmp/mods* 中。
* 待完成的功能
    * 自动放到游戏mod文件夹中（感觉没啥必要）。
    * 有些mod实际上是大版本通用的，但是现在的做法是匹配到具体的小版本，所以会出现找不到的情况……
## 用法
* 修改 *config.yml* 文件。
    * 修改 *version* 项，默认为 1.12.2。
    * 修改 *origin_mod_dir* 项，内容为自己的游戏mod目录，形如 *F:\Game\MultiMC\instances\BWEA\.minecraft\mods* 。
* 运行 *1.列出mod表格.bat*
* 运行 *2.在curseforge上查找.bat* ，依次选择mod对应的curseforge项目id，和最新mod的id
* 运行 *3.下载mod.bat* ，等待运行完成，下载好的mod文件就在 *tmp/mods* 目录下。
