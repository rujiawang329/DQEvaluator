import os
import pandas as pd

def convert_verilog_to_csv(input_dir: str, output_dir: str):
    """将每个.v文件转换为单独的CSV文件
    
    Args:
        input_dir: 包含.v文件的目录路径
        output_dir: 输出CSV文件的目录路径
    """
    # 遍历目录中的所有.v文件
    for filename in os.listdir(input_dir):
        if filename.endswith('.v'):
            input_path = os.path.join(input_dir, filename)
            # 创建对应的csv文件名
            output_filename = filename.replace('.v', '.csv')
            output_path = os.path.join(output_dir, output_filename)
            
            try:
                # 读取Verilog文件内容
                with open(input_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 创建单行DataFrame
                df = pd.DataFrame({'text': [content]})
                
                # 保存为CSV
                df.to_csv(output_path, index=False)
                print(f"Successfully converted: {filename} -> {output_filename}")
            except Exception as e:
                print(f"Error processing {filename}: {str(e)}")

def merge_verilog_to_single_csv(input_dir: str, output_file: str):
    """将目录下所有.v文件合并为单个CSV文件
    
    Args:
        input_dir: 包含.v文件的目录路径
        output_file: 输出的CSV文件路径
    """
    # 存储所有文件内容
    contents = []
    
    # 遍历目录中的所有.v文件
    for filename in os.listdir(input_dir):
        if filename.endswith('.v'):
            input_path = os.path.join(input_dir, filename)
            try:
                # 读取Verilog文件内容
                with open(input_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                contents.append(content)
                print(f"Successfully read: {filename}")
            except Exception as e:
                print(f"Error processing {filename}: {str(e)}")
    
    # 创建DataFrame，只包含text列
    df = pd.DataFrame({'text': contents})
    
    # 保存为CSV
    df.to_csv(output_file, index=False)
    print(f"\nSuccessfully merged {len(contents)} files into: {output_file}")

if __name__ == "__main__":
    input_dir = "test_data"
    output_dir = "data"
    
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)
    
    # 转换为单独的CSV文件
    convert_verilog_to_csv(input_dir, output_dir)
    
    # 合并为单个CSV文件
    # output_merged = os.path.join(output_dir, "merged_verilog.csv")
    # merge_verilog_to_single_csv(input_dir, output_merged)
