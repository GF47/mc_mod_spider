# mc_mod_spider
用来将minecraft的mod自动同步到curseforge的最新版本。
顺带练手爬虫。

---

## 功能
* 扫描已经安装的mod，将列表存储在 *mod_list.txt* 中。
* 爬取curseforge的mod信息，如果有更新，则将更新的mod文件存储在 *tmp/mods* 中。
    > mod名称匹配curseforge的项目名称是放在本地做的，从jar包里获取mod名称，然后模糊匹配到mod项目字典。其中的 *mod_dictionary.csv* 文件是从一个国内开源翻译项目[Minecraft-Mod-Language-Package](https://github.com/CFPAOrg/Minecraft-Mod-Language-Package)中提取的，懒得自己爬了。下载量有些不太够的mod在这里找不到，现在的版本需要手动去查，以后大概会改成非本地匹配，但是这样就会用到curseforge网站自己的搜索功能，有点虚。
* 待完成的功能
    * 自动放到游戏mod文件夹中（感觉没啥必要）。
    * 有些mod实际上是大版本通用的，但是现在的做法是匹配到具体的小版本，所以会出现找不到的情况……
## 用法
* 修改 *config.yml* 文件。
    * 修改 *version* 项，默认为 1.12.2。
    * 修改 *mod_dir* 项，内容为自己的游戏mod目录，反斜杠即可。
* 如果是第一次用，删掉 *new_list.txt* 和 *mod_list.txt* 文件。
* 运行 *search_your_mods.bat*，根据提示选择mod所对应的curseforge项目，最后会在同级目录下生成 *mod_list.txt* 文件，本地mod项目字典中找不到的，需要手动去curseforge复制项目名称（并不是页面上的mod名字，而是网页url中的projects后边紧跟的字段）。
* 运行 *run.bat* ，等待运行完成，下载好的mod文件就在 *tmp/mods* 目录下。