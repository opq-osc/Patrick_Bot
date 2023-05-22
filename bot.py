from botoy import bot

if __name__ == "__main__":
	bot.load_plugins()  # 加载插件
	bot.print_receivers()  # 打印插件信息
	bot.run()  # 一键启动
