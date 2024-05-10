from tkinter import filedialog
from tkinter import messagebox
from threading import Thread
from datetime import datetime
from doc import json_extractor
from doc.document_processor import DocumentProcessor
import json
import gui_setup
import tkinter as tk
import time
class GUI:
    def __init__(self, master):
        self.master = master
        master.title("大模型数据收集应用")
        # master.iconbitmap("icon.ico")  #新增app图标


        self.should_pause = False  # 暂停标志
        self.is_on_top = tk.BooleanVar(value=False)  # 是否置顶，默认为不置顶

        self.doc_processor = DocumentProcessor()

        # 创建复选框用于控制置顶功能
        self.topmost_checkbox = tk.Checkbutton(master, text="勾选此处\n将窗口置顶", variable=self.is_on_top, command=self.set_topmost)
        self.topmost_checkbox.grid(row=0, column=0, padx=10, pady=2, sticky="w")

        # 创建各个功能区域的 Frame
        self.template_frame = tk.Frame(master)
        self.template_frame.grid(row=0, column=1, padx=2, pady=2)



        self.output_frame = tk.Frame(master)
        self.output_frame.grid(row=2, column=1, padx=2, pady=2)

        # 创建一个框架来包含 file_frame 和 template_selection_frame
        self.file_template_frame = tk.Frame(master)
        self.file_template_frame.grid(row=1, column=1, padx=2, pady=2)

        # 放置 file_frame 和 template_selection_frame
        self.file_frame = tk.Frame(self.file_template_frame)
        self.file_frame.pack(side=tk.LEFT, padx=2, pady=2)

        self.template_selection_frame = tk.Frame(self.file_template_frame)
        self.template_selection_frame.pack(side=tk.LEFT, padx=2, pady=2)

        self.status_frame = tk.Frame(master)
        self.status_frame.grid(row=5, column=1, padx=2, pady=2)

        # 创建一个框架来包含按钮
        self.button_pause_frame = tk.Frame(master)
        self.button_pause_frame.grid(row=4, column=1, padx=2, pady=2)

        # 在框架中放置按钮
        self.button_frame = tk.Frame(self.button_pause_frame)
        self.button_frame.pack(side=tk.LEFT, padx=5, pady=2)

        self.pause_frame = tk.Frame(self.button_pause_frame)
        self.pause_frame.pack(side=tk.LEFT, padx=5, pady=2)


        self.sleep_frame = tk.Frame(master)
        self.sleep_frame.grid(row=6, column=1, padx=2, pady=2)

        self.json_frame = tk.Frame(master)
        self.json_frame.grid(row=7, column=1, padx=2, pady=2)

        self.switch_button= tk.Frame(master)
        self.switch_button.grid(row=8, column=1, padx=2, pady=2)

        # 直接调用 setup_gui 函数
        gui_setup.setup_gui(self)







    def select_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Word 文档", "*.docx")])
        if file_path:
            self.label.config(text="已选择文档：" + file_path)
            self.doc_processor.load_document(file_path)
            self.update_status_label()
        else:
            self.label.config(text="未选择文档")

    def process_text(self):
        if self.doc_processor.content:
            # 显示开始生成提示信息
            self.output_text.insert(tk.END, f"{datetime.now().strftime('%Y.%m.%d-%H:%M:%S')} 开始生成\n")
            self.output_text.see(tk.END)
            self.master.update()

            self.process_button.config(state="disabled")
            # 在新线程中启动倒计时
            Thread(target=self.countdown, args=(5,)).start()  # 倒计时 5 秒
        else:
            messagebox.showinfo("提示", "请选择一个 Word 文档")

    def countdown(self, seconds):
        for i in range(seconds, 0, -1):
            time.sleep(1)  # 暂停一秒
            self.output_text.insert(tk.END, f"倒计时 {i} 秒...请将鼠标放置在网页对话框中\n")
            self.output_text.see(tk.END)
            self.master.update()
        # 倒计时结束，开始执行后续步骤
        Thread(target=self.process_text_thread).start()

    def countdown_after_resume(self, seconds):
        # 倒计时 5 秒
        for i in range(seconds, 0, -1):
            time.sleep(1)  # 暂停一秒
            self.output_text.insert(tk.END, f"倒计时 {i} 秒...请将鼠标放置在网页对话框中\n")
            self.output_text.see(tk.END)
            self.master.update()
        # 倒计时结束后，继续运行

        self.should_pause = False  # 设置为继续状态

    # def pause_resume_process(self):
    #     if self.should_pause:  # 如果当前处于暂停状态
    #         self.should_pause = False  # 设置为继续状态
    #         self.pause_button.config(text="暂停")  # 修改按钮文本为“暂停”
    #         self.pause_status_label.config(text="")  # 清空状态信息
    #     else:
    #         self.should_pause = True  # 设置为暂停状态
    #         self.pause_button.config(text="继续")  # 修改按钮文本为“继续”
    #         timestamp = datetime.now().strftime('%Y.%m.%d-%H:%M:%S')
    #         # 获取当前处理到的段落索引
    #         current_index = self.doc_processor.current_paragraph
    #         # 在文本框中插入指定信息
    #         self.output_text.insert(tk.END,
    #                                 f"{timestamp} 当前处理到第{current_index}段，程序已经暂停，如需继续运行，请点击（继续）按钮\n")
    #         self.output_text.see(tk.END)  # 滚动到文本末尾

    # def pause_resume_process(self):
    #     if self.should_pause:  # 如果当前处于暂停状态
    #         self.should_pause = False  # 设置为继续状态
    #         self.pause_button.config(text="暂停")  # 修改按钮文本为“暂停”
    #         self.pause_status_label.config(text="")  # 清空状态信息
    #
    #         # 在新线程中启动倒计时
    #         Thread(target=self.countdown_and_resume, args=(5,)).start()  # 倒计时 5 秒并继续运行
    #     else:
    #         self.should_pause = True  # 设置为暂停状态
    #         self.pause_button.config(text="继续")  # 修改按钮文本为“继续”
    #         timestamp = datetime.now().strftime('%Y.%m.%d-%H:%M:%S')
    #         # 获取当前处理到的段落索引
    #         current_index = self.doc_processor.current_paragraph
    #         # 在文本框中插入指定信息
    #         self.output_text.insert(tk.END,
    #                                 f"{timestamp} 当前处理到第{current_index}段，程序已经暂停，如需继续运行，请点击（继续）按钮\n")
    #
    #         self.output_text.see(tk.END)  # 滚动到文本末尾

    def pause_resume_process(self):
        if self.should_pause:  # 如果当前处于暂停状态

            self.pause_button.config(text="暂停")  # 修改按钮文本为“暂停”
            # self.pause_status_label.config(text="")  # 清空状态信息

            # 在新线程中启动倒计时
            Thread(target=self.countdown_after_resume, args=(5,)).start()  # 倒计时 5 秒并继续运行

        else:
            self.should_pause = True  # 设置为暂停状态
            self.pause_button.config(text="继续")  # 修改按钮文本为“继续”
            timestamp = datetime.now().strftime('%Y.%m.%d-%H:%M:%S')
            # 获取当前处理到的段落索引
            current_index = self.doc_processor.current_paragraph
            # 在文本框中插入指定信息
            self.output_text.insert(tk.END,
                                    f"{timestamp} 当前处理到第{current_index}段，程序已经暂停，如需继续运行，请点击（继续）按钮\n")
            self.output_text.see(tk.END)  # 滚动到文本末尾



    def process_text_thread(self):
        if self.doc_processor.content:
            # 获取用户输入的等待时间
            sleep_time = self.sleep_value.get()

            self.process_button.config(state="disabled")  # 禁用开始按钮
            selected_template = self.selected_template.get()
            if selected_template == "自定义":
                custom_template = self.template_text.get("1.0", tk.END).strip()  # 从文本框中获取自定义模板
                if not custom_template:
                    messagebox.showinfo("提示", "请输入自定义模板！")
                    return
                template = custom_template
            else:
                # 获取模板选项的索引
                template_options = ["通用", "文旅-管理角度", "文旅-游客角度", "小红书", "知乎"
                                    ]
                template_index = template_options.index(selected_template)
                template = self.templates[template_index]  # 获取选定的模板
            for index, part in enumerate(self.doc_processor.content.split('\n'), 1):
                while self.should_pause:  # 检查是否需要暂停
                    time.sleep(1)  # 暂停一秒
                    continue  # 继续等待暂停解除

                # 显示当前的文本内容和时间
                timestamp = datetime.now().strftime('%Y.%m.%d-%H:%M:%S')
                self.output_text.insert(tk.END, f"{timestamp} 第{index}段 复制成功，请勿移动鼠标⌛️\n")
                # 滚动到文本末尾
                self.output_text.see(tk.END)
                # 更新界面以显示实时内容
                self.master.update()

                if part.strip():
                    self.doc_processor.process_paragraphs(template, index, sleep_time)  # 处理每个段落
                    self.master.after(0, self.update_status_label)  # 更新状态标签

            self.master.after(0, self.show_generation_complete_message)  # 显示生成完成提示信息
            self.process_button.config(state="normal")  # 启用开始按钮
        else:
            messagebox.showinfo("提示", "请选择一个 Word 文档")
    def show_generation_complete_message(self):
        messagebox.showinfo("提示", "生成完成！")

    def update_status_label(self):
        status_text = f"文档总段落数：{self.doc_processor.total_paragraphs}，当前处理到第 {self.doc_processor.current_paragraph} 段"
        self.status_label.config(text=status_text)

    def update_template_text(self, selected_template):
        # 获取模板选项的索引
        template_options = ["通用", "文旅-管理角度", "文旅-游客角度", "小红书", "知乎","自定义"]
        template_index = template_options.index(selected_template)

        # 如果选择的是自定义模板，那么允许用户在文本框中编辑
        if selected_template == "自定义":
            self.template_text.config(state=tk.NORMAL)  # 允许在模板文本框中编辑
            self.template_text.delete('1.0', tk.END)  # 清空文本框
            self.template_text.insert(tk.END, self.templates[template_index])  # 插入选定模板内容
            self.template_content.set(self.templates[template_index])  # 更新模板内容变量
        else:
            # 否则，从模板列表中获取对应的模板内容
            self.template_text.config(state=tk.NORMAL)  # 允许在模板文本框中编辑
            self.template_text.delete('1.0', tk.END)  # 清空文本框
            self.template_text.insert(tk.END, self.templates[template_index])  # 插入选定模板内容
            self.template_content.set(self.templates[template_index])  # 更新模板内容变量
            self.template_text.config(state=tk.DISABLED)  # 禁止在模板文本框中编辑

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

    def set_topmost(self):
        """根据复选框的选择设置窗口是否置顶"""
        self.master.attributes("-topmost", self.is_on_top.get())