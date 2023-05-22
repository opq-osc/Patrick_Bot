from Patrick import Patrick
from botoy import ctx, mark_recv, S, start_session

pdx = Patrick()


async def MirageTank():
	if msg := ctx.g:  # 群聊
		if msg.text == '幻影坦克':
			ss = start_session(group=True, multi_user=False)
			ss.set_finish_info("输入超时，对话结束")
			ss.set_default_timeout(20)
			img1res, s = await ss.must_image("请发送表层图(即不点开图片看到的图)")  # 该方法超时会直接结束对话
			img2res, s = await ss.image("请发送底层图(即点开图片看到的图，可与上图一致)")
			img1 = pdx.get_webpic(img1res[0].Url)
			img2 = pdx.get_webpic(img2res[0].Url)
			info = "表层图是否需要高斯模糊"
			if await ss.confirm(info):
				tank = pdx.MirageTank(img1, img2, Base64=True)
			else:
				tank = pdx.MirageTank(img1, img2, GaussianBlur=False, Base64=True)
			await s.image(tank)
			# await s.image(img2, '这是图2')

mark_recv(MirageTank, name="幻影坦克", author="Lord2333", usage='发送 幻影坦克 按提示操作即可')
