# json_extractor.py

import json
import re

def extract_json_from_text(txt_path):
    with open(txt_path, 'r', encoding='utf-8') as f:
        content = f.read()

    json_data = []

    # 尝试从文本中提取 JSON 数据
    json_objs = get_objects_from_string(content)
    if json_objs:
        json_data.extend(json_objs)

    return json_data

def get_objects_from_string(s):
    json_objs = []

    # 尝试匹配 json object
    reg = r"\{[\s\S]*?\}"  # 修改正则表达式以非贪婪方式匹配多个 JSON 对象
    matches = re.findall(reg, s)
    for match in matches:
        try:
            json_obj = json.loads(match)
            # 检查 JSON 对象是否为空，或者只包含空字符串或者空格
            if json_obj and not all(value.strip() == "" for value in json_obj.values()):
                json_objs.append(json_obj)
        except Exception as e:
            pass

    return json_objs
