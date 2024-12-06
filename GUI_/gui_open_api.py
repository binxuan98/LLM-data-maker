from openai import OpenAI
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from doc.document_processor import DocumentProcessor
from GUI_ import gui_api_setup
from doc import json_extractor
from threading import Thread
import json

# 设置 OpenAI API 客户端
client = OpenAI(
    api_key="sk-EKXvYp3G9cZGnJfQSU7RfCLEsgufsez2qfpkOWFA6o2RhFqe",
    base_url="https://api.chatanywhere.tech"
)

class GUI1:
    def __init__(self, master):
        self.master = master
        master.title("大模型数据收集应用（当前：API 对话模式）")

        self.is_on_top = tk.BooleanVar()
        self.doc_processor = DocumentProcessor()

        self.selected_template = None

        # 创建一个新的按钮
        self.switch_button = tk.Button(master, text="切换至 网页对话模式", command=self.switch_to_gui, height=2, width=12)
        self.switch_button.grid(row=7, column=0, padx=1, pady=2)

        # 设置默认的 Base URL 和 TXT 文件路径
        self.default_base_url = "http://1.180.205.129:21011/chat/chat"
        self.default_txt_path = "/Users/zhangbinxuan/Downloads"

        # 调用 setup_frames 函数
        gui_api_setup.setup_frames_api(self)

        # 直接调用 setup_gui 函数
        gui_api_setup.setup_gui_api(self)

    def set_topmost(self):
        """根据复选框的选择设置窗口是否置顶"""
        self.master.attributes("-topmost", self.is_on_top.get())

    def collect_json_data(self):
        txt_path = filedialog.askopenfilename(filetypes=[("Text 文本文件", "*.txt")])  # 选择文本文件
        if txt_path:
            json_data = json_extractor.extract_json_from_text(txt_path)  # 调用新的功能模块中的函数

            if json_data:
                save_path = filedialog.asksaveasfilename(defaultextension=".json",
                                                         filetypes=[("JSON 文件", "*.json")])  # 选择保存路径
                if save_path:
                    with open(save_path, 'w', encoding='utf-8') as f:
                        json.dump(json_data, f, indent=4, ensure_ascii=False)  # 写入 JSON 数据到文件中
                    messagebox.showinfo("提示", "JSON 数据提取完成并保存到文件中！")
                else:
                    messagebox.showinfo("提示", "未选择保存路径！")
            else:
                messagebox.showinfo("提示", "未找到有效的 JSON 数据！")
        else:
            messagebox.showinfo("提示", "未选择文本文件！")

    def update_template_text(self, selected_template):
        # 获取模板选项的索引
        template_options = ["通用", "文旅-管理角度", "文旅-游客角度", "小红书", "知乎", "自定义"]
        template_index = template_options.index(selected_template)

        # 保存当前选择的模板
        self.selected_template = self.templates[template_index]

        # 如果选择的是自定义模板，那么允许用户在文本框中编辑
        if selected_template == "自定义":
            self.template_text.config(state=tk.NORMAL)  # 允许在模板文本框中编辑
            self.template_text.delete('1.0', tk.END)  # 清空文本框
            self.template_text.insert(tk.END, self.templates[template_index])  # 插入选定模板内容
            self.template_content.set(self.templates[template_index])  # 更新模板内容变量
        else:
            # 否则，从模板列表中获取对应的模板内容
            self.template_text.config(state=tk.NORMAL)  # 允许在文本框中编辑
            self.template_text.delete('1.0', tk.END)  # 清空文本框
            self.template_text.insert(tk.END, self.templates[template_index])  # 插入选定模板内容
            self.template_content.set(self.templates[template_index])  # 更新模板内容变量
            self.template_text.config(state=tk.DISABLED)  # 禁止在文本框中编辑

    def update_status_label(self):
        status_text = f"文档总段落数：{self.doc_processor.total_paragraphs}，当前处理到第 {self.doc_processor.current_paragraph} 段"
        self.status_label.config(text=status_text)

    def switch_to_gui(self):
        self.master.destroy()  # 销毁当前的 GUI1 界面
        root = tk.Tk()  # 创建一个新的 Tkinter 窗口
        from GUI_.gui import GUI  # 导入 GUI 类
        gui = GUI(root)  # 创建一个新的 GUI 界面
        root.mainloop()  # 启动 Tkinter 的主循环

    def switch_gui(self):
        self.master.destroy()  # 销毁当前的GUI
        root = tk.Tk()  # 创建一个新的Tkinter窗口
        from MENU.menu import GUIWithMenu  # 将导入语句放在函数内部
        gui = GUIWithMenu(root)  # 创建一个新的GUIWithMenu
        root.mainloop()  # 启动Tkinter的主循环

    def select_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Word 文档", "*.docx")])
        if file_path:
            self.label.config(text="已选择文档：" + file_path)
            self.doc_processor.load_document(file_path)
            self.update_status_label()
        else:
            self.label.config(text="未选择文档")

    def update_status_label(self):
        status_text = f"文档总段落数：{self.doc_processor.total_paragraphs}，当前处理到第 {self.doc_processor.current_paragraph} 段"
        self.status_label.config(text=status_text)

    def stop(self):
        # 停止从 API 获取数据
        self.should_stop = True  # 假设你有一个名为 should_stop 的属性来控制是否应该停止从 API 获取数据

        # 在文本框中显示 "已经停止对话"
        self.output_text.insert(tk.END, "已经停止对话\n")
        self.output_text.see(tk.END)

    def start(self):
        # 创建一个新的线程来执行 start_thread 方法
        self.should_stop = False  # 在开始新的对话之前，确保 should_stop 属性为 False
        Thread(target=self.start_thread).start()

    def start_thread(self):
        base_url = self.base_url_entry.get()

        if not base_url:
            messagebox.showinfo("提示", "请输入Base URL")
            return

        # 从 Word 文档中读取内容并逐段发送对话请求
        if self.doc_processor.content:
            paragraphs = self.doc_processor.content.split('\n')

            # 禁用开始按钮
            self.start_button.config(state="disabled")

            for index, part in enumerate(paragraphs, 1):
                # 获取当前模板内容
                current_template = self.template_text.get("1.0", tk.END).strip()
                if not current_template:
                    messagebox.showinfo("提示", "请输入自定义模板！")
                    return

                # 创建对话消息
                messages = [
                    {"role": "user", "content": current_template.replace("{content}", part.strip())}
                ]

                self.doc_processor.current_paragraph = index  # 更新当前处理的段落数
                self.update_status_label()  # 更新状态标签

                # 发送对话请求
                try:
                    for chunk in self.gpt_35_api_stream(messages):
                        # 在获取每一行数据之前，检查是否应该停止
                        if self.should_stop:
                            break

                        # 确保chunk包含所需的属性
                        if 'choices' in chunk and len(chunk['choices']) > 0:
                            delta = chunk['choices'][0].get('delta', {})
                            if 'content' in delta:
                                # 将数据实时显示在文本框中
                                self.output_text.insert(tk.END, delta['content'])
                                # 滚动到文本框的末尾
                                self.output_text.see(tk.END)
                except Exception as e:
                    messagebox.showinfo("提示", f"对话请求失败：{e}")

                # 在获取每一段数据之后，检查是否应该停止
                if self.should_stop:
                    break

            # 启用开始按钮和停止按钮
            self.start_button.config(state="normal")
            self.stop_button.config(state="normal")
        else:
            messagebox.showinfo("提示", "请选择一个 Word 文档")

    def gpt_35_api_stream(self, messages: list):
        """为提供的对话消息创建新的回答 (流式传输)

        Args:
            messages (list): 完整的对话消息
        """
        stream = client.chat.completions.create(
            model='gpt-3.5-turbo',
            messages=messages,
            stream=True,
        )
        for chunk in stream:
            yield chunk

