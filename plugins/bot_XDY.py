import httpx
from botoy import ctx, mark_recv, jconfig, S
from bs4 import BeautifulSoup as bs
from Patrick import Patrick

pdx = Patrick()

proxies = jconfig.proxies_http
headers = {
	"User-Agent": ":Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko)Version/5.1 Safari/534.50",
	"content-type": "text/html; charset=utf-8",
}

__doc__ = """小电影"""


async def main():
	if m := (ctx.friend_msg or ctx.group_msg):
		if '搜番号' in m.text:
			_S = S.bind(ctx)
			FH = m.text[3:].strip()
			Txt = ''
			if FH.isspace() or len(FH) == 0 or "[ATALL()]" in FH:
				await _S.atext("请输入 搜番号+番号\n如：.搜番号ipx177")
				return
			FH_data = Get_FH(FH).json()
			if FH_data:
				for F_data in FH_data:
					Txt = str(F_data['title']) + "\n番号：" + str(F_data['fh']) + "\n发行日期：" + str(
						F_data['meta']) + "\n评分：" + str(
						F_data['score']) + "\n访问地址：" + str(F_data['url'])
					pic = pdx.get_webpic(F_data['img'])  # 获取封面
					await _S.image(text=Txt, data=pdx.MirageTank(pic, text=F_data['fh'], color=True,Base64=True))
			else:
				await _S.text("请求频繁，请稍后再试！")


def S_fh(FH):
	FH_data = []
	API = "https://javdb.com/search?q=" + FH + "&f=all"
	res = httpx.get(API, proxies=proxies, headers=headers).text
	soup = bs(res, 'html.parser')
	List = soup.find("div", class_="movie-list")
	Items = List.find_all("div", class_="item")
	i = 0
	Web = soup.find('body').get("data-domain").replace('.', '。')
	for item in Items:
		if i <= 4:
			i += 1
			# Web = 'https://javdb.com'
			url = item.find('a').get("href")
			title = item.find('a').get("title")
			fh = item.find('strong').text
			meta = item.find('div', class_='meta').text.replace(" ", "").replace('\n', '')
			score = item.find('span', class_='value').text.replace(u"\xa0", u"").replace(" ", "").replace('\n', '')
			img = item.find('img').get("src")
			FH_data.append({
				"url": Web + url,
				"title": title,
				"fh": fh,
				"meta": meta,
				"score": score,
				"img": img})
		else:
			break
	return FH_data


def Get_FH(FH):
	XDY_API = jconfig.XDY_API + FH
	return httpx.get(XDY_API)


mark_recv(main, author='Lord2333', name="小电影", usage='搜番号+[番号]')
