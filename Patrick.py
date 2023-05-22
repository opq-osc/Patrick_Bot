"""
Patrick v1.0.0

这里是比奇堡派大星~\n\n
Patrick是一个基于botoy的QQ机器人工具库，封装了一些我认为可能会用的上的小函数，同时提供了一个用于插件管理的思路，
具体用法详见下方注释。\n\n如果派大星能够帮助到你进行，就请你动动发财的小手，给我点个star吧~这是对我最大的鼓励！\n\n
"""

from psutil import Process, NoSuchProcess, process_iter
from botoy import jconfig, bot
from prettytable import PrettyTable
from ptable import FormatTable
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter
import numpy as np
import re, sqlite3, base64, io, sys, time, requests
from typing import *


class Patrick:
	def __init__(self):
		self.plugins = []
		self.admin = jconfig.get("admin")  # 管理员QQ号
		self.sql_name = jconfig.get("Sql_name")  # 数据库文件名
		self.conn = self.con2sql()  # 连接数据库
		np.seterr(divide="ignore", invalid="ignore")

	def get_bot_runtime(self) -> str:
		# botoy.json中是否保存了opq主程序的PID
		try:
			pid = int(jconfig.get("Pid"))
			runtime = time.time() - Process(pid).create_time()
			runtime = self.count_time(runtime)
			return "机器人已运行了" + runtime
		except NoSuchProcess:  # 第一次运行或无效进程
			return self.update_pid()
		except TypeError:
			return self.update_pid()

	def count_time(self, Time) -> str:
		"""
		将秒数转换为天时分秒

		:param Time: 以秒为单位的时间
		:return: 返回格式为 xx天xx小时xx分xx秒 的字符串
		"""
		day = Time // (24 * 3600)
		Time = Time % (24 * 3600)
		hour = Time // 3600
		Time %= 3600
		minute = Time // 60
		Time %= 60
		second = Time
		return "%d天%d时%d分%d秒" % (day, hour, minute, second)

	def update_pid(self, pid_name="OPQBot") -> str:
		"""
		更新opq主程序的PID，并返回进程运行时间

		:param pid_name: 默认为OPQBot，可自行修改
		:return: 返回运行时间或错误信息
		"""
		for proc in process_iter():
			if pid_name in proc.name():
				pid = proc.pid
				jconfig.get_configuration().update("Pid", pid)
				# 获取pid运行时间
				runtime = time.time() - Process(pid).create_time()
				runtime = self.count_time(runtime)
				return "机器人已运行了" + runtime
		return "当前没有正在运行的%s进程哦~" % pid_name

	def get_plugins_list(self, flag=0) -> list:
		"""
		获取已加载插件列表

		:param flag: 0为已加载插件，1为所有插件
		:return: 插件列表
		"""
		table = []
		if flag == 0:
			for receiver in bot.receivers:
				info = receiver.info
				table.append([re.sub(r' [a-zA-Z]*', '', info.name), info.author, info.usage])  # 正则去除插件名后面的英文
		# elif flag == 1:
		# 	dir_list = os.listdir("./plugins")  # 获取插件目录下的文件列表
		# 	for receiver in bot.receivers:
		# 		info = receiver.info
		# 		table.append([re.sub(r' [a-zA-Z]*', '', info.name), info.meta])  # 显示插件名及文件名
		# 	if len(dir_list)-1 == len(table):  # 判断是否有未加载的插件
		# 		return table
		# 	else:
		# 		req = len(dir_list)-1-len(table)  # 计算未加载插件数量
		# 		temp_dir = []
		# 		for info in table:
		# 			meta = info[1]
		# 			meta = re.search(r'\\(.*) l', meta).group(1)  # 截取插件文件名
		# 			temp_dir.append(meta)
		# 		for dir in dir_list:
		# 			if dir not in temp_dir:
		# 				table.append([re.search(r'(.*).py', dir).group(1), 'plugins/' + dir])
		# 				req -= 1
		# 				if not req:
		# 					break
		elif flag == 1:
			for receiver in bot.receivers:
				info = receiver.info
				table.append(re.sub(r' [a-zA-Z]*', '', info.name))  # 只要中文名就行了
		return table

	def generate_table(self, table, table_type='group') -> str:
		"""
		生成插件表格图片

		:param table: 二维列表，每一行为一条记录
		:param table_type: 表格类型，group为群组，friend为私聊，new为新插件
		:return: base64编码的图片
		"""
		if len(sys.argv) == 2:
			s = sys.argv[1]
			tab = FormatTable(s)
		else:
			tab = FormatTable()
		# 设置表头
		if len(table[0]) == 3:
			tab.set_title(["插件名", "作者", "食用方法"])
		elif len(table[0]) == 2:
			if table_type == "group":
				tab.set_title(["插件名", "群号"])
			elif table_type == "friend":
				tab.set_title(["插件名", "QQ"])
		elif len(table[0]) == 4:
			tab.set_title(["插件名", "群聊", "私聊", "临时会话"])
		for row in table:
			tab.add_row([str(i) for i in row])  # 需要把元组转换为列表
		tab_info = tab.show()
		if len(table[0]) == 4:
			tab_info = tab_info.replace("1", "√").replace("0", "×")
		space = 10
		# windows
		font = ImageFont.truetype('C:\\WINDOWS\\Fonts\\simsun.ttc', 15, encoding='utf-8')
		# Image模块创建一个图片对象
		im = Image.new('RGB', (10, 10), (0, 0, 0, 0))
		draw = ImageDraw.Draw(im, "RGB")
		img_size = draw.multiline_textsize(tab_info + "\n", font=font)
		im_new = im.resize((img_size[0] + space * 2, img_size[1] + space * 2))
		del draw
		del im
		draw = ImageDraw.Draw(im_new, 'RGB')
		draw.multiline_text((space, space), tab_info + "\nBot by Lord2333", fill=(255, 255, 255), font=font)
		temp = io.BytesIO()
		im_new.save(temp, format='PNG')
		if table_type == 'new':
			im_new.save('./Src/plugins.png', format='png')
		base64_str = base64.b64encode(temp.getvalue()).decode('utf-8')
		return base64_str

	def is_admin(self, context) -> bool:
		"""
		判断是否为管理员

		:return: 返回True或False
		"""
		if context.from_user == self.admin:
			return True
		else:
			return False

	def con2sql(self) -> object:
		"""
		连接sqlite3数据库的函数，返回一个连接对象

		:return: obj
		"""
		if self.sql_name:
			conn = sqlite3.connect(self.sql_name)
		else:
			return None
		return conn

	def get_plugin_plan(self) -> list:
		"""
		获取插件的配置信息，在机器人启动时调用，默认所有插件权限都开启，此时权限数据库为黑名单模式
		在friend和group表中的用户和群无法使用插件，反之为白名单模式，在表中的用户和群可以使用插件

		:return: 插件配置信息格式为[插件名, 群聊开关, 私聊开关, 临时会话开关]
		"""
		cursor = self.conn.cursor()  # 连接数据库
		try:
			cursor.execute("SELECT * FROM plugin_list")
			data = cursor.fetchall()
		except sqlite3.OperationalError:  # 数据库中没有plugin_list表
			return None
		if len(data) < len(self.get_plugins_list(1)):  # 数据库中插件配置信息小于已加载插件数量
			data = [i[0] for i in cursor.execute("SELECT Plugin_name FROM plugin_list")]
			plugins = self.get_plugins_list(1)  # 获取到活动插件列表
			if data is []:
				for plugin in plugins:
					cursor.execute("INSERT INTO plugin_list VALUES('%s', 1, 1, 1)" % plugin)  # 默认全部为开启
			else:
				for plugin in plugins:
					if plugin not in data:  # 插入新插件
						cursor.execute("INSERT INTO plugin_list VALUES('%s', 1, 1, 1)" % plugin)
			self.conn.commit()
			cursor.execute("SELECT * FROM group_config")
			data = cursor.fetchall()
		cursor.close()  # 记得关闭游标！！！
		return data

	def get_plugin_group(self, plugin_name="派大星") -> list:
		"""
		获取插件的群聊配置信息

		:param plugin_name: 插件名
		:return: 插件白名单/黑名单列表
		"""
		cursor = self.conn.cursor()
		try:
			cursor.execute("SELECT * FROM group_config where Plugin_name = '%s';" % plugin_name)
			data = cursor.fetchall()
		except sqlite3.OperationalError:
			return None
		cursor.close()  # 记得关闭游标！！！
		return data

	def get_plugin_friend(self, plugin_name="派大星") -> list:
		"""
		获取插件的私聊配置信息

		:param plugin_name: 插件名
		:return: 插件白名单/黑名单列表
		"""
		cursor = self.conn.cursor()
		try:
			cursor.execute("SELECT * FROM friend_config where Plugin_name = '%s';" % plugin_name)
			data = cursor.fetchall()
		except sqlite3.OperationalError:
			return None
		cursor.close()
		return data

	def generate_plugin_authority(self, is_admin_msg=False, plugin_name=""):
		"""
		生成插件权限表格，在群聊时显示本群全部插件权限，在管理员私聊时显示全部插件黑/白名单
		输入插件名时显示该插件的黑/白名单。当图片过长时仅显示前五个用户

		:param is_admin_msg: 是否为管理员私聊
		:param plugin_name: 插件名，默认为空
		:return:
		"""
		if is_admin_msg:
			if plugin_name:
				...
		else:
			...

	def get_webpic(self, url: str) -> Image.Image:
		"""
		获取网络图片

		:param url: 图片链接
		:return: 图片对象
		"""
		try:
			headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "}
			response = requests.get(url, headers=headers)
			img = Image.open(io.BytesIO(response.content))
			return img
		except:
			return None

	# 以下三个函数来自 https://github.com/Aloxaf/MirageTankGo
	def resize_image(self, im1: Image.Image, im2: Image.Image, mode: str) -> Tuple[Image.Image, Image.Image]:
		"""
		统一图像大小
		"""
		_wimg = im1.convert(mode)
		_bimg = im2.convert(mode)

		wwidth, wheight = _wimg.size
		bwidth, bheight = _bimg.size

		width = max(wwidth, bwidth)
		height = max(wheight, bheight)

		wimg = Image.new(mode, (width, height), 255)
		bimg = Image.new(mode, (width, height), 0)

		wimg.paste(_wimg, ((width - wwidth) // 2, (height - wheight) // 2))
		bimg.paste(_bimg, ((width - bwidth) // 2, (height - bheight) // 2))

		return wimg, bimg

	def gray_car(
			self,
			wimg: Image.Image,
			bimg: Image.Image,
			wlight: float = 1.0,
			blight: float = 0.3,
			chess: bool = False,
	) -> Image.Image:
		"""
		发黑白车
		:param wimg: 白色背景下的图片
		:param bimg: 黑色背景下的图片
		:param wlight: wimg 的亮度
		:param blight: bimg 的亮度
		:param chess: 是否棋盘格化
		:return: 处理后的图像
		"""
		wimg, bimg = self.resize_image(wimg, bimg, "L")
		wpix = np.array(wimg).astype("float64")
		bpix = np.array(bimg).astype("float64")
		# 棋盘格化
		# 规则: if (x + y) % 2 == 0 { wpix[x][y] = 255 } else { bpix[x][y] = 0 }
		if chess:
			wpix[::2, ::2] = 255.0
			bpix[1::2, 1::2] = 0.0
		wpix *= wlight
		bpix *= blight
		a = 1.0 - wpix / 255.0 + bpix / 255.0
		r = np.where(a != 0, bpix / a, 255.0)
		pixels = np.dstack((r, r, r, a * 255.0))
		pixels[pixels > 255] = 255
		return Image.fromarray(pixels.astype("uint8"), "RGBA")

	def color_car(
			self,
			wimg: Image.Image,
			bimg: Image.Image,
			wlight: float = 1.0,
			blight: float = 0.18,
			wcolor: float = 0.5,
			bcolor: float = 0.7,
			chess: bool = False,
	) -> Image.Image:
		"""
		发彩色车

		:param wimg: 白色背景下的图片
		:param bimg: 黑色背景下的图片
		:param wlight: wimg 的亮度
		:param blight: bimg 的亮度
		:param wcolor: wimg 的色彩保留比例
		:param bcolor: bimg 的色彩保留比例
		:param chess: 是否棋盘格化
		:return: 处理后的图像
		"""
		wimg = ImageEnhance.Brightness(wimg).enhance(wlight)
		bimg = ImageEnhance.Brightness(bimg).enhance(blight)
		wimg, bimg = self.resize_image(wimg, bimg, "RGB")
		wpix = np.array(wimg).astype("float64")
		bpix = np.array(bimg).astype("float64")
		if chess:
			wpix[::2, ::2] = [255., 255., 255.]
			bpix[1::2, 1::2] = [0., 0., 0.]
		wpix /= 255.
		bpix /= 255.
		wgray = wpix[:, :, 0] * 0.334 + wpix[:, :, 1] * 0.333 + wpix[:, :, 2] * 0.333
		wpix *= wcolor
		wpix[:, :, 0] += wgray * (1. - wcolor)
		wpix[:, :, 1] += wgray * (1. - wcolor)
		wpix[:, :, 2] += wgray * (1. - wcolor)
		bgray = bpix[:, :, 0] * 0.334 + bpix[:, :, 1] * 0.333 + bpix[:, :, 2] * 0.333
		bpix *= bcolor
		bpix[:, :, 0] += bgray * (1. - bcolor)
		bpix[:, :, 1] += bgray * (1. - bcolor)
		bpix[:, :, 2] += bgray * (1. - bcolor)
		d = 1. - wpix + bpix
		d[:, :, 0] = d[:, :, 1] = d[:, :, 2] = d[:, :, 0] * 0.222 + d[:, :, 1] * 0.707 + d[:, :, 2] * 0.071
		p = np.where(d != 0, bpix / d * 255., 255.)
		a = d[:, :, 0] * 255.
		colors = np.zeros((p.shape[0], p.shape[1], 4))
		colors[:, :, :3] = p
		colors[:, :, -1] = a
		colors[colors > 255] = 255
		return Image.fromarray(colors.astype("uint8")).convert("RGBA")

	def pic_waterprint(self, Image: Image.Image, text: str) -> Image.Image:
		"""
		给图片上添加水印

		:param Image: pillow.Image对象
		:param text: 水印文字
		:return: pillow.Image对象
		"""
		im = Image
		draw = ImageDraw.Draw(im)
		# 设置字体
		font = ImageFont.truetype('C:/Windows/Fonts/simhei.ttf', int(im.size[1] / 4))  # 自适应字体大小
		draw.text((im.size[0] / 4, im.size[1] / 2 - 50), text, font=font, fill=(255, 0, 0))
		return im

	def MirageTank(self,
	               img1: Image.Image,
	               img2: Image.Image = None,
	               text: str = '',
	               color: bool = False,
	               GaussianBlur: int = 15,
	               Base64: bool = False
	):
		"""
		生成幻影坦克

		:param img1: 前景图，必须传入，默认做高斯模糊处理
		:param img2: 背景图，可以不传入使用前景图作为背景图
		:param text: 水印文字
		:param color: 是否为彩色
		:param GaussianBlur: 0为不使用高斯模糊，传入数值为高斯模糊的半径
		:param Base64: 是否返回base64编码
		:return: pillow.Image对象或base64编码
		"""
		temp_img = Image.Image()
		if img2:
			if GaussianBlur:
				img1 = img1.filter(ImageFilter.GaussianBlur(radius=GaussianBlur))
			if text:
				img1 = self.pic_waterprint(img1, text)
		else:
			img2 = img1
			if GaussianBlur:
				img1 = img1.filter(ImageFilter.GaussianBlur(radius=GaussianBlur))
			if text:
				img1 = self.pic_waterprint(img1, text)
		if color:
			temp_img = self.color_car(img1, img2)
		else:
			temp_img = self.gray_car(img1, img2)
		if Base64:
			temp = io.BytesIO()
			temp_img.save(temp, format='PNG')
			base64_str = base64.b64encode(temp.getvalue()).decode('utf-8')
			return base64_str
		else:
			return temp_img


if __name__ == "__main__":
	pdx = Patrick()
	# plugin_data = [('派大星', '1', '1', '1')]
	# print(pdx.generate_table(plugin_data))
	url = 'https://c0.jdbstatic.com/covers/qd/qDg6M.jpg'
	im1 = pdx.get_webpic(url)
	pdx.MirageTank(im1, text='IPX115').save("./Src/gray_av.png")
	print(1)
