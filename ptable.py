import sys


class FormatTable:

	def __init__(self, split_str='|'):
		# 初始化参数 >标题：title >行信息：rows >默认分隔符：split_str='|'
		self.title = self.split_str = self.title_str = None
		self.rows = []
		self.set_split(split_str)
		# >系统架构：sysVersion > python版本：py_version
		self.sysVersion = sys.platform
		self.py_version = sys.version[0]
		if self.py_version == '2':
			reload(sys)
			sys.setdefaultencoding('utf8')

	def str_len(self, check_str):
		# 汉字计数器，每个汉字宽度+1；返回需要增加的宽度
		if self.py_version == '2':
			return sum((1 for ch in check_str.decode('utf-8') if u'\u4e00' <= ch <= u'\u9fff'))
		else:
			return sum((1 for ch in check_str if u'\u4e00' <= ch <= u'\u9fff'))

	def set_title(self, title):
		# 设置标题，并添加到行信息
		self.title = title
		self.rows.append(title)

	def add_row(self, row):
		# 添加行信息，字段不足自动补齐'None'
		diff = len(self.title) - len(row)
		if diff > 0:
			row.extend(['None' for i in range(diff)])
		self.rows.append(row)

	def get_max_wide(self):
		# 计算表格 纵列最大宽度
		return [max(len(ele.encode('utf-8')) for ele in i) for i in zip(*self.rows)]

	def set_split(self, split_str):
		# 设置分隔符
		self.split_str = split_str
		# 标题分隔符，单字符默认为+，超过单字符即设置为split_str
		self.title_str = '+' if len(self.split_str) == 1 else self.split_str

	def show(self, visible=False):
		res = ""
		# 输出表格信息
		split_len = 2
		max_index_list = self.get_max_wide()
		# print(max_index_list)
		# 格式化分隔符（i + split_len：列间距）
		lab_format = ['{0:-^%s}' % (i + split_len) for i in max_index_list]
		lab_print = '{0}{1}{0}'.format(self.title_str, self.title_str.join([f.format('-') for f in lab_format]))
		for row in self.rows:
			if self.sysVersion == 'win32':
				row_format = ['{0:^%s}' % (t - self.str_len(i) + 2) for t, i in zip(max_index_list, row)]
			else:
				row_format = ['{0:^%s}' % (t - self.str_len(i) + 2) for t, i in zip(max_index_list, row)]
			row_print = '{0}{1}{0}'.format(
				self.split_str, self.split_str.join([f.format(r) for f, r in zip(row_format, row)]))
			if row == self.title:
				res += ('{0}\n{1}\n{0}'.format(lab_print, row_print))
			else:
				res += ("\n"+row_print)
		res += ("\n"+lab_print)
		if visible:
			print(res)
		return res


if __name__ == '__main__':
	if len(sys.argv) == 2:
		s = sys.argv[1]
		table = FormatTable(s)
	else:
		table = FormatTable()
	table.set_title(['编号', '云编号', '名称', 'IP地址'])
	table.add_row(['2', '√', '√', '√'])
	table.add_row(['3', '×', '√', '×'])
	table.show(True)
