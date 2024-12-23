"""文件处理相关的工具函数"""
import os
import pandas as pd

def load_data(data_file):
    """加载数据文件"""
    try:
        # 尝试读取CSV文件
        df = pd.read_csv(data_file)
        
        # 确保有text列
        if 'text' not in df.columns:
            raise ValueError("CSV file must contain a 'text' column")
        
        # 重命名列以匹配代码
        df = df.rename(columns={'text': 'code_text'})
        
        print(f"\nSuccessfully loaded data with {len(df)} records")
        return df
    except Exception as e:
        print(f"Error loading data: {str(e)}")
        raise

def ensure_dir(directory):
    """确保目录存在，如果不存在则创建"""
    if not os.path.exists(directory):
        os.makedirs(directory)
