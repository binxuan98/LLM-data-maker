import requests
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from doc.document_processor import DocumentProcessor
from GUI_ import gui_api_setup
from doc import json_extractor
from threading import Thread
import json
import datetime
# 优化
class GUI1:
    # 将模板和URL定义为类变量
    DEFAULT_BASE_URL = "这里输入api请求地址"
    DEFAULT_MODEL = "Yi-1.5-34B-Chat"
    
    def __init__(self, master):
        # 初始化基本属性
        self._init_attributes(master)
        # 初始化UI组件
        self._init_ui()

    def _init_attributes(self, master):
        """初始化基本属性"""
        self.master = master
        self.master.title("大模型数据收集应用（当前：API 对话模式）")
        
        # 使用字典存储状态变量
        self.state = {
            'should_stop': False,
            'is_on_top': tk.BooleanVar(value=False)
        }
        
        # 添加窗口关闭协议
        self.master.protocol("WM_DELETE_WINDOW", self.master.destroy)
        
        self.doc_processor = DocumentProcessor()
        self.selected_template = None

    def _init_ui(self):
        """初始化UI组件"""
        self._create_switch_button()
        gui_api_setup.setup_frames_api(self)
        gui_api_setup.setup_gui_api(self)

    def _create_switch_button(self):
        """创建模式切换按钮"""
        self.switch_button = tk.Button(
            self.master,
            text="切换至 网页对话模式",
            command=self.switch_to_gui,
            height=2,
            width=15
        )
        self.switch_button.grid(row=6, column=0, padx=1, pady=2)

    def set_topmost(self):
        """根据复选框的选择设置窗口是否置顶"""
        is_top = self.state['is_on_top'].get()
        self.master.attributes("-topmost", is_top)

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
        """切换到GUI模式"""
        # 直接销毁当前窗口
        self.master.destroy()
        
        # 创建新窗口
        root = tk.Tk()
        from GUI_.gui import GUI
        gui = GUI(root)
        root.mainloop()

    def switch_gui(self):
        """切换到菜单模式"""
        # 直接销毁当前窗口
        self.master.destroy()
        
        # 创建新窗口
        root = tk.Tk()
        from MENU.menu import GUIWithMenu
        gui = GUIWithMenu(root)
        root.mainloop()

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
        self.state['should_stop'] = True  # 假设你有一个名为 should_stop 的属性来控制是否应该停止从 API 获取数据

        # 在文本框中显示 "已经停止对话"
        self.output_text.insert(tk.END, "已经停止对话\n")
        self.output_text.see(tk.END)

    def start(self):
        # 创建一个新的线程来执行 start_thread 方法
        self.state['should_stop'] = False  # 在开始新的对话之前，确保 should_stop 属性为 False
        Thread(target=self.start_thread).start()

    def start_thread(self):
        """优化API请求处理"""
        if not self._validate_inputs():
            return

        dialog_params = self._create_dialog_params()
        
        if not self.doc_processor.content:
            messagebox.showinfo("提示", "请选择一个 Word 文档")
            return

        self._process_paragraphs(dialog_params)

    def _validate_inputs(self):
        """验证输入参数"""
        base_url = self.base_url_entry.get()
        if not base_url:
            messagebox.showinfo("提示", "请输入Base URL")
            return False
        return True

    def _create_dialog_params(self):
        """创建对话参数"""
        return {
            "conversation_id": "",
            "history_len": -1,
            "history": [],
            "stream": True,
            "model_name": self.DEFAULT_MODEL,
            "temperature": 0.8,
            "max_tokens": 0,
            "prompt_name": "default"
        }

    def _process_paragraphs(self, dialog_params):
        """处理文档段落"""
        self.start_button.config(state="disabled")
        paragraphs = self.doc_processor.content.split('\n')

        for index, part in enumerate(paragraphs, 1):
            if self.state['should_stop']:
                break

            if not self._process_single_paragraph(dialog_params, part, index):
                break

        self._reset_buttons()

    def _process_single_paragraph(self, dialog_params, part, index):
        """处理单个段落"""
        current_template = self.template_text.get("1.0", tk.END).strip()
        if not current_template:
            messagebox.showinfo("提示", "请输入自定义模板！")
            return False

        params = dialog_params.copy()
        params["query"] = current_template.replace("{content}", part.strip())
        
        self._update_progress(index)
        return self._make_api_request(params)

    def _make_api_request(self, params):
        """发送API请求"""
        try:
            response = requests.post(
                self.base_url_entry.get(),
                json=params,
                headers=self._get_headers(),
                stream=True
            )

            if response.status_code == 200:
                return self._handle_response_stream(response)
            else:
                messagebox.showinfo("提示", f"对话请求失败！状态码：{response.status_code}")
                return False
        except Exception as e:
            messagebox.showinfo("错误", f"请求发生错误：{str(e)}")
            return False

    def _get_headers(self):
        """获取请求头"""
        return {
            "accept": "application/json",
            "Content-Type": "application/json",
        }

    def _handle_response_stream(self, response):
        """处理流式响应"""
        for line in response.iter_lines():
            if self.state['should_stop']:
                return False

            if line:
                try:
                    decoded_line = line.decode('utf-8')
                    data = json.loads(decoded_line.lstrip('data: '))
                    self._update_output(data['text'])
                except Exception as e:
                    print(f"处理响应时出错：{str(e)}")
                    continue
        return True

    def _update_progress(self, index):
        """更新进度显示"""
        self.doc_processor.current_paragraph = index
        self.update_status_label()

    def _update_output(self, text):
        """更新输出显示"""
        self.output_text.insert(tk.END, text)
        self.output_text.see(tk.END)

    def _reset_buttons(self):
        """重置按钮状态"""
        self.start_button.config(state="normal")
        self.stop_button.config(state="normal")

    def collect_json_data_api(self):
        # 从 output_text 文本框中获取所有文字
        output_text_content = self.output_text.get("1.0", tk.END)

        # 使用 extract_json_from_text 方法提取其中的 JSON 格式数据
        json_data = json_extractor.extract_json_from_output(output_text_content)

        if json_data:
            # 获取当前日期并格式化为字符串
            current_date = datetime.datetime.now().strftime("%Y-%m-%d")

            # 选择保存路径
            save_path = filedialog.asksaveasfilename(defaultextension=".json",
                                                     filetypes=[("JSON 文件", "*.json")],
                                                     initialfile=f"json-{current_date}")  # 使用当前日期作为默认文件名
            if save_path:
                # 将 JSON 数据保存到文件中
                with open(save_path, 'w', encoding='utf-8') as f:
                    json.dump(json_data, f, indent=4, ensure_ascii=False)
                messagebox.showinfo("提示", "JSON 数据提取完成并保存到文件中！")
            else:
                messagebox.showinfo("提示", "未选择保存路径！")
        else:
            messagebox.showinfo("提示", "未找到有效的 JSON 数据！")

    def _on_closing(self):
        """处理窗口关闭事件"""
        try:
            # 如果正在运行API请求，先停止
            if not self.state['should_stop']:
                self.stop()
            
            # 确保清理所有资源
            self.master.quit()
            self.master.destroy()
        except Exception as e:
            print(f"关闭窗口时出错: {str(e)}")
            # 如果出错，强制关闭
            try:
                self.master.destroy()
            except:
                pass

