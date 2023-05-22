# Patrick_Bot
<div align=center><img src="Src\Patrick.png" style="width:20%;"/></br>
<img alt="GitHub last commit" src="https://img.shields.io/github/last-commit/Lord2333/Patrick_Bot?logo=github&amp;label=上次更新&amp;link=https://github.com/Lord2333/Patrick_Bot"/><img src="https://img.shields.io/github/license/Lord2333/Patrick_Bot"/></br>这里是比奇堡派大星！</div>

------

# 零、简介

Patrick_Bot（下文简称派大星）是一个基于[botoy](https://github.com/opq-osc/botoy)框架的QQBot，部分功能继承于[CSGOSkin_Bot](https://github.com/opq-osc/CSGOSkin_Bot)，功能较杂（大部分都还在脑子里）。

派大星的大部分功能都依赖于[Patrick.py](./Patrick.py)实现，包括但不限于插件管理、发送幻影坦克图片、~~CSGO饰品监控~~等。如果你需要移植派大星的功能到自己的机器人请按需复制Patrick.py中的函数

# 一、功能列表

```shell
+------------------+----------+----------------------------------+
|       插件名     |    作者   |            使用方法               |
+------------------+----------+----------------------------------+
|   Github缩略图   | Lord2333 | 发送github项目链接自动渲染缩略图    | 
|      派大星      | Lord2333 |  发送 派大星 查看机器人运行信息     |  
|      小电影      | Lord2333 |          搜番号+[番号]            |
+------------------+----------+----------------------------------+
```

Todo：

- [ ] CSGO皮肤监控插件
- [ ] 权限管理插件补全
- [ ] 幻影坦克插件
- [ ] TBD...

# 二、部署使用

首先确保你能够正常运行OPQBot框架，下载或克隆本项目后打开[botoy.json](./botoy.json)，按照下方注释进行修改

```json
{
  "url": "127.0.0.1:8086",  //你的OPQBot监听地址，这是默认的端口
  "qq": 1107459688,         //你的bot的QQ号
  "Pid": 5792,				//OPQ进程的IPD，这一项可以不填，会自动生成
  "admin": 123456789,		//管理员QQ号
  "XDY_API": "搜片API",	  //搜番号API，详见https://deta.space/discovery/r/9mjmveukbxmiox4u
  "Sql_name": "plugins.db",//插件管理数据库
}
```

然后在终端中运行`pip install -r requirements.txt`或`pip3 install -r requirements.txt`安装所需依赖，安装完成后运行`python bot.py`或`python3 bot.py`即可

```shell
+------------------+----------+----------------------------------+-------------------------------+
|       Name       |  Author  |              Usage               |              Meta             |
+------------------+----------+----------------------------------+-------------------------------+
| Github缩略图 eyi | Lord2333 | 发送github项目链接自动渲染缩略图 | plugins\bot_github.py line 14 |
|    派大星 ahn    | Lord2333 |  发送 派大星 查看机器人运行信息  |   plugins\bot_info.py line 7  |
|    小电影 ziy    | Lord2333 |          搜番号+[番号]           |   plugins\bot_XDY.py line 17  |
+------------------+----------+----------------------------------+-------------------------------+
ℹ️ 05-22 14:21:27 INFO 连接中[ws://127.0.0.1:8086/ws]...
✔️ 05-22 14:21:28 SUCCESS 连接成功!
```



