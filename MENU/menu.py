import tkinter as tk
from tkinter import messagebox
import webbrowser
from GUI.gui import GUI


class GUIWithMenu(GUI):
    def __init__(self, master):
        super().__init__(master)

        # 创建菜单栏
        self.menu_bar = tk.Menu(master)
        self.master.config(menu=self.menu_bar)

        # 创建直达大模型菜单
        self.model_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="大模型网页传送门", menu=self.model_menu)
        self.model_menu.add_command(label="ChatGPT", command=self.open_model_link_1)
        self.model_menu.add_command(label="智谱清言", command=self.open_model_link_2)
        self.model_menu.add_command(label="文新一言", command=self.open_model_link_3)
        self.model_menu.add_command(label="通义千问", command=self.open_model_link_4)

        # 创建帮助菜单
        self.help_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="帮助", menu=self.help_menu)
        self.help_menu.add_command(label="关于", command=self.show_about)

        # 创建科学上网攻略子菜单
        self.internet_guide_menu = tk.Menu(self.help_menu, tearoff=0)
        # self.help_menu.add_cascade(label="科学上网攻略", menu=self.internet_guide_menu)
        # self.internet_guide_menu.add_command(label="一键跳转", command=self.open_internet_guide)
        # self.internet_guide_menu.add_command(label="文字攻略", command=self.show_internet_guide)






    def show_about(self):
        about_message = "本程序由斌轩开发，遇到任何问题请联系zhangbinxuan21@163.com"
        messagebox.showinfo("关于", about_message)

    def show_internet_guide(self):
        guide_message = "请访问以下网页，“https://ikuuu.pw/auth/register?code=Wo7O”\n如遇到问题请联系zhangbinxuan21@163.com"
        messagebox.showinfo("科学上网攻略", guide_message)

    def open_internet_guide(self):
        link = "https://ikuuu.pw/auth/register?code=Wo7O"
        webbrowser.open_new(link)




    def open_model_link_1(self):
        link = "https://chat.openai.com/"
        webbrowser.open_new(link)

    def open_model_link_2(self):
        link = "https://chatglm.cn/"
        webbrowser.open_new(link)

    def open_model_link_3(self):
        link = "https://yiyan.baidu.com/"
        webbrowser.open_new(link)

    def open_model_link_4(self):
        link = "https://tongyi.aliyun.com/qianwen/"
        webbrowser.open_new(link)

