from tkinter import filedialog, messagebox
from threading import Thread
from datetime import datetime
from doc import json_extractor
from doc.document_processor import DocumentProcessor
import json
from GUI_ import gui_setup
import tkinter as tk
import time

class GUI:
    def __init__(self, master):
        # 初始化基本属性
        self._init_attributes(master)
        # 初始化UI组件
        self._init_ui()

    def _init_attributes(self, master):
        """初始化基本属性"""
        self.master = master
        self.master.title("大模型数据收集应用（当前：网页对话模式）")
        
        # 使用字典存储状态变量，提高访问效率
        self.state = {
            'should_pause': False,
            'is_on_top': tk.BooleanVar(value=False)
        }
        
        # 添加窗口关闭协议
        self.master.protocol("WM_DELETE_WINDOW", self.master.destroy)
        
        # 预先创建 DocumentProcessor 实例
        self.doc_processor = DocumentProcessor()

    def _init_ui(self):
        """初始化UI组件"""
        # 先设置框架，再设置其他UI组件
        self._setup_frames()
        self._setup_gui()
        
        # 最后创建API按钮
        self._create_api_button()

    def _create_api_button(self):
        """创建API切换按钮"""
        self.api_button = tk.Button(
            self.master,
            text="切换至 API 对话模式",
            command=self.switch_to_api,
            height=2,
            width=12
        )
        self.api_button.grid(row=7, column=0, padx=2, pady=2)

    def _setup_frames(self):
        """设置框架"""
        gui_setup.setup_frames(self)

    def _setup_gui(self):
        """设置GUI组件"""
        gui_setup.setup_gui(self)

    def switch_to_api(self):
        """切换到API模式"""
        # 直接销毁当前窗口
        self.master.destroy()
        
        # 创建新窗口
        root = tk.Tk()
        from GUI_.gui_api import GUI1
        gui = GUI1(root)
        root.mainloop()

    def _on_api_window_close(self, api_window):
        """处理API窗口关闭事件"""
        api_window.destroy()
        self.master.deiconify()  # 重新显示主窗口

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

        self.state['should_pause'] = False  # 设置为继续状态


    def pause_resume_process(self):
        if self.state['should_pause']:  # 使用state字典
            self.pause_button.config(text="暂停")
            Thread(target=self.countdown_after_resume, args=(5,)).start()
        else:
            self.state['should_pause'] = True  # 使用state字典
            self.pause_button.config(text="继续")
            timestamp = datetime.now().strftime('%Y.%m.%d-%H:%M:%S')
            current_index = self.doc_processor.current_paragraph
            self.output_text.insert(tk.END,
                                  f"{timestamp} 当前处理到第{current_index}段，程序已经暂停，如需继续运行，请点击（继续）按钮\n")
            self.output_text.see(tk.END)



    def process_text_thread(self):
        """优化文本处理线程"""
        if not self.doc_processor.content:
            messagebox.showinfo("提示", "请选择一个 Word 文档")
            return

        self.process_button.config(state="disabled")
        sleep_time = self.sleep_value.get()
        template = self._get_template()
        
        # 使用生成器处理文档
        for index, part in self._process_document_parts():
            if self.state['should_pause']:
                self._handle_pause()
                continue
                
            self._update_ui_for_part(index)
            if part.strip():
                self.doc_processor.process_paragraphs(template, index, sleep_time)
                self.master.after(0, self.update_status_label)

        self.master.after(0, self._finish_processing)

    def _process_document_parts(self):
        """文档处理生成器"""
        return enumerate(
            self.doc_processor.content.split('\n'),
            1
        )

    def _update_ui_for_part(self, index):
        """更新UI显示"""
        timestamp = datetime.now().strftime('%Y.%m.%d-%H:%M:%S')
        self.output_text.insert(tk.END, 
            f"{timestamp} 第{index}段 复制成功，请勿移动鼠标⌛️\n")
        self.output_text.see(tk.END)
        self.master.update_idletasks()  # 使用update_idletasks代替update

    def _finish_processing(self):
        self.master.after(0, self.show_generation_complete_message)
        self.process_button.config(state="normal")

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
        self.master.attributes("-topmost", self.state['is_on_top'].get())

    def _get_template(self):
        """优化模板获取逻辑"""
        selected_template = self.selected_template.get()
        if selected_template == "自定义":
            custom_template = self.template_text.get("1.0", tk.END).strip()
            if not custom_template:
                raise ValueError("请输入自定义模板！")
            return custom_template
            
        template_options = ["通用", "文旅-管理角度", "文旅-游客角度", "小红书", "知乎"]
        template_index = template_options.index(selected_template)
        return self.templates[template_index]