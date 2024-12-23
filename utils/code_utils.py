"""代码处理相关的工具函数"""
import re

def preprocess_code(code):
    """预处理代码文本"""
    if not isinstance(code, str):
        return []
    return code.split('\n')

def normalize_line(line):
    """标准化代码行，保留结构特征"""
    # 替换字符串常量
    line = re.sub(r'"[^"]*"', 'STR', line)
    
    # 替换带数字的变量名（如data1, data2）
    line = re.sub(r'\b\w+\d+\b', 'VAR', line)
    
    # 替换Verilog数字常量
    line = re.sub(r'\b\d+\'b[01]+\b', 'BIN', line)  # 二进制
    line = re.sub(r'\b\d+\'h[0-9a-fA-F]+\b', 'HEX', line)  # 十六进制
    line = re.sub(r'\b\d+\'d\d+\b', 'DEC', line)  # 十进制
    
    # 替换普通数字
    line = re.sub(r'\b\d+\b', 'NUM', line)
    
    # 规范化空白字符
    return ' '.join(line.split())

def is_comment_line(line):
    """检查是否为注释行"""
    line = line.strip()
    return (line.startswith('//') or 
            line.startswith('/*') or 
            line.startswith('*') or 
            line.endswith('*/'))

def is_blank_line(line):
    """检查是否为空白行"""
    return not bool(line.strip())
