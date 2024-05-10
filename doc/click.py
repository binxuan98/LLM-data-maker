import pyautogui
import time

class ChatBoxClicker:
    def __init__(self):
        pass

    def click_chat_box(self):
        """
        使用图像识别定位聊天框并模拟点击左键
        """
        # 截取屏幕区域，以便识别聊天框
        screenshot = pyautogui.screenshot()

        # 在截图中搜索聊天框特征
        chat_box_location = pyautogui.locateOnScreen('/Users/zhangbinxuan/Documents/free-self-instruct/app/大模型自动提问脚本app/chat_box.png')

        if chat_box_location is not None:
            # 如果找到聊天框，则获取其中心坐标
            x, y = pyautogui.center(chat_box_location)

            # 将鼠标移动到聊天框中心并模拟点击左键
            pyautogui.moveTo(x, y, duration=1)
            time.sleep(1)
            pyautogui.click()



