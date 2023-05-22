from botoy import S, ctx, mark_recv
from Patrick import Patrick

pdx = Patrick()


async def main():
	if m := (ctx.group_msg or ctx.friend_msg):
		if m.text == "派大星":
			runtime = pdx.get_bot_runtime()
			n_plugins = pdx.get_plugins_list()
			if len(pdx.plugins) != len(n_plugins):  # 如果插件数量变化，则新生成表格
				pdx.plugins = n_plugins
				pdx.generate_table(pdx.plugins, 'new')
			await S.image('./Src/plugins.png', '%s\n目前已加载插件：' % runtime)
		elif m.text == ".admin":
			if pdx.is_admin(m):
				pdx.plugins = pdx.get_plugins_list(1)  # 获取插件列表
				await S.image(pdx.generate_table(pdx.plugins),
				              '''插件目录下所有插件：\n回复插件序号操作插件''')
                #  未完待续...
				pdx.plugins = pdx.get_plugins_list()
			else:
				await S.text("您不是海绵宝宝！")  # 反正私聊也用不上

mark_recv(main, author='Lord2333', name="派大星", usage='发送 派大星 查看机器人运行信息')
