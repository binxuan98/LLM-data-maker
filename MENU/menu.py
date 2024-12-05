import tkinter as tk
from tkinter import messagebox
import webbrowser
from GUI_.gui import GUI
from functools import partial


class GUIWithMenu(GUI):
    MODEL_LINKS = {
        "ChatGPT": "https://chat.openai.com/",
        "智谱清言": "https://chatglm.cn/",
        "文新一言": "https://yiyan.baidu.com/",
        "通义千问": "https://tongyi.aliyun.com/qianwen/",
        "DeepSeek": "https://chat.deepseek.com/"
    }

    def __init__(self, master):
        super().__init__(master)
        
        # 添加窗口关闭协议
        self.master.protocol("WM_DELETE_WINDOW", self.master.destroy)
        self._create_menus()

    def _configure_window(self, master):
        master.update_idletasks()
        master.protocol("WM_DELETE_WINDOW", self._on_closing)

    def _create_menus(self):
        self.menu_bar = tk.Menu(self.master)
        self.master.config(menu=self.menu_bar)

        self._create_model_menu()
        
        self._create_help_menu()

    def _create_model_menu(self):
        self.model_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="大模型网页传送门", menu=self.model_menu)
        
        for model_name, link in self.MODEL_LINKS.items():
            self.model_menu.add_command(
                label=model_name,
                command=partial(webbrowser.open_new, link)
            )

    def _create_help_menu(self):
        self.help_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="帮助", menu=self.help_menu)
        self.help_menu.add_command(label="关于", command=self.show_about)

    def show_about(self):
        about_message = "本程序由斌轩开发，遇到任何问题请联系zhangbinxuan21@163.com"
        messagebox.showinfo("关于", about_message)

    def _on_closing(self):
        self.master.destroy()




