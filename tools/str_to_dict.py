# 👇 新增：把字符串转成 {"question": ...}
from langchain_core.runnables import RunnableLambda


def convert_input(x):
    if isinstance(x, str):
        return {"question": x}
    return x  # 已经是 dict，直接返回

input_converter = RunnableLambda(convert_input)