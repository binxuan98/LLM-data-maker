import tkinter as tk

# 优化
def setup_gui_api(self):

    # 模板内容显示区域
    self.template_content = tk.StringVar()
    self.template_text = tk.Text(self.template_frame, height=10, width=50)
    self.template_text.pack(padx=2, pady=2)

    # 文件选择区域
    self.label = tk.Label(self.file_frame, text="第1步:选择文档：")
    self.label.pack(side=tk.LEFT, padx=2, pady=2)

    self.select_button = tk.Button(self.file_frame, text="选择", command=self.select_file)
    self.select_button.pack(side=tk.LEFT, padx=2, pady=2)

    # 输出文本区域
    self.output_text = tk.Text(self.output_frame, height=30, width=100)
    self.output_text.pack(padx=2, pady=2)

    # 模板选择区域
    self.label_template = tk.Label(self.template_selection_frame, text="第2步:选择模板：")
    self.label_template.pack(side=tk.LEFT, padx=2, pady=2)
    # 添加自定义模板选项
    template_options = ["通用", "文旅-管理角度", "文旅-游客角度", "小红书", "知乎","自定义"]  # List of template options including "自定义"
    self.selected_template = tk.StringVar(self.master)
    self.selected_template.set("通用")  # 默认选择第一个模板
    self.template_option = tk.OptionMenu(self.template_selection_frame, self.selected_template,
                                         *template_options, command=self.update_template_text)
    self.template_option.pack(side=tk.LEFT, padx=2, pady=2)
    # 功能按钮区域


    # 状态显示区域
    self.status_label = tk.Label(self.status_frame, text="", font=("Arial", 10))
    self.status_label.pack(padx=2, pady=2)

    # 暂停按钮区域




    # JSON 数据收集区域
    self.collect_json_label = tk.Label(self.json_frame, text="等word文档中所有段落依次问答完毕后，点击下面按钮，自动提取历史记录转为训练所需JSON 问答数据", font=("Arial", 10))
    self.collect_json_label.pack(padx=2, pady=2)

    self.collect_json_button = tk.Button(self.json_frame, text="将上面对话记录一键转为JSON", command=self.collect_json_data_api,height=3, width=20, bg="blue",
                                         fg="black")
    self.collect_json_button.pack(padx=2, pady=2)







    # 定义模板内容
    self.templates = [
        '''
根据以下文旅知识：
"{content}"\n
让我们思考一下，请你为我构造一个多轮问答数据，其中包含指令(instruction)和标准答案(output)，
如果你认为某些任务需要特定的上下文或输入(input),请为这些任务添加相应的输入(input)。
确保问题和答案与文旅领域相关，你认为的标准答案请尽量回答的全面且有逻辑，回答的越详细越好。
请分三行输出三条结构化 JSON 对象：
{
  "instruction": "",
  "input": "",
  "output": ""
}
        ''',
        '''
        根据以下文旅知识：
        "{content}"\n
        让我们思考一下，请你为我构造一个多轮问答数据,包含用户的问题input和你认为的标准答案output,你认为的标准答案请尽量回答的全面且有逻辑，回答的越详细越好，“从文旅管理单位的角度出发”作为instruction指令，分三行输出三条结构化 JSON 对象：
        { "instruction": "从文旅管理单位的角度出发", "input": "", "output": " "  },
        ''',
        '''
        根据以下文旅知识：
        "{content}"\n
        让我们思考一下，请你为我构造一个多轮问答数据,包含用户的问题input和你认为的标准答案output,你认为的标准答案请尽量回答的全面且有逻辑，回答的越详细越好，“从游客的角度出发”作为instruction指令，分三行输出三条结构化 JSON 对象：
        { "instruction": "从游客的角度出发", "input": "", "output": " "  },
        ''',
        '''
        以下内容是小红书风格文字：
        "{content}"\n
        让我们思考一下，请你为我构造一个多轮问答数据,包含问题input和你认为的标准答案output,你认为的标准答案请尽量回答的全面且有逻辑，回答的越详细越好，“用小红书风格来回答”作为instruction指令，分三行输出三条结构化 JSON 对象：
        { "instruction": "用小红书风格来回答", "input": "", "output": " "  },
        ''',
        '''
        以下内容是知乎风格文字：
        "{content}"\n
        让我们思考一下，请你为我构造一个多轮问答数据,包含问题input和你认为的标准答案output,你认为的标准答案请尽量回答的全面且有逻辑，回答的越详细越好，“用知乎风格来回答”作为instruction指令，分三行输出三条结构化 JSON 对象：
        { "instruction": "用知乎风格来回答", "input": "", "output": " "  },
        ''',
        '''
        以下内容是<建议修改>风格文字：
        "{content}"\n
        让我们思考一下，请你为我构造一个多轮问答数据,包含问题input和你认为的标准答案output,你认为的标准答案请尽量回答的全面且有逻辑，回答的越详细越好，“用<建议修改>来回答”作为instruction指令，分三行输出三条结构化 JSON 对象：
        { "instruction": "用<建议修改>来回答", "input": "", "output": " "  },
        '''
    ]


    # 初始化模板文本框显示模板1的
    self.update_template_text("通用")

    # 创建变量用于存储当前复制粘贴的内容
    self.copy_content = tk.StringVar()

def setup_frames_api(self):
    """设置所有框架"""
    # 创建置顶复选框
    self.topmost_checkbox = tk.Checkbutton(
        self.master, 
        text="勾选此处\n将窗口置顶", 
        variable=self.state['is_on_top'],  # 使用 state 字典中的变量
        command=self.set_topmost
    )
    self.topmost_checkbox.grid(row=0, column=0, padx=10, pady=2, sticky="w")

    # 创建主要框架
    self.template_frame = tk.Frame(self.master)
    self.template_frame.grid(row=0, column=1, padx=2, pady=2)

    self.output_frame = tk.Frame(self.master)
    self.output_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

    self.file_template_frame = tk.Frame(self.master)
    self.file_template_frame.grid(row=1, column=1, padx=2, pady=2)

    self.file_frame = tk.Frame(self.file_template_frame)
    self.file_frame.pack(side=tk.LEFT, padx=2, pady=2)

    self.template_selection_frame = tk.Frame(self.file_template_frame)
    self.template_selection_frame.pack(side=tk.LEFT, padx=2, pady=2)

    self.status_frame = tk.Frame(self.master)
    self.status_frame.grid(row=4, column=1, padx=2, pady=2)

    self.sleep_frame = tk.Frame(self.master)
    self.sleep_frame.grid(row=5, column=0, columnspan=2, padx=2, pady=2)

    self.json_frame = tk.Frame(self.master)
    self.json_frame.grid(row=6, column=1, padx=2, pady=2)

    # 创建一个新的 Frame 来放置这些组件
    input_frame = tk.Frame(self.master)
    input_frame.grid(row=1, column=0, padx=2, pady=2)

    # 在新的 Frame 中添加两个输入框
    self.base_url_label = tk.Label(input_frame, text="api_url:")
    self.base_url_label.grid(row=0, column=0, padx=2, pady=2)
    self.base_url_entry = tk.Entry(input_frame)
    self.base_url_entry.grid(row=0, column=1, padx=2, pady=2)
    self.base_url_entry.insert(tk.END, self.DEFAULT_BASE_URL)

    # 创建一个新的 Frame 来放置这两个按钮
    button_frame = tk.Frame(self.master)
    button_frame.grid(row=3, column=0, columnspan=2, padx=2, pady=2)

    # 修改开始按钮的命令函数
    self.start_button = tk.Button(button_frame, text="API对话", command=self.start, height=3, width=10)
    self.start_button.pack(side=tk.LEFT, padx=20, pady=2)

    # 新增一个 "停止" 按钮
    self.stop_button = tk.Button(button_frame, text="停止", command=self.stop, height=3, width=10)
    self.stop_button.pack(side=tk.LEFT, padx=20, pady=2)





