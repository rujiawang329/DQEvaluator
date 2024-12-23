"""代码行长度分析器"""
import numpy as np
from utils.code_utils import preprocess_code

class LineLengthAnalyzer:
    def analyze_line_lengths(self, df):
        """分析每个文件中代码行的长度分布"""
        file_line_lengths = []
        
        for code in df['code_text']:
            # 获取每行代码
            lines = preprocess_code(code)
            
            # 计算每行的长度
            line_lengths = [len(line.rstrip()) for line in lines if line.strip()]
            
            if line_lengths:
                file_line_lengths.append({
                    'min_length': min(line_lengths),
                    'max_length': max(line_lengths),
                    'mean_length': np.mean(line_lengths),
                    'median_length': np.median(line_lengths),
                    'std_length': np.std(line_lengths),
                    'long_lines_count': sum(1 for x in line_lengths if x > 80),  # 超过80字符的行数
                    'total_lines': len(line_lengths)
                })
            else:
                file_line_lengths.append({
                    'min_length': 0,
                    'max_length': 0,
                    'mean_length': 0,
                    'median_length': 0,
                    'std_length': 0,
                    'long_lines_count': 0,
                    'total_lines': 0
                })
        
        # 计算整体统计信息
        all_stats = {
            'line_length_stats': {
                'min': float(np.min([x['min_length'] for x in file_line_lengths])),
                'max': float(np.max([x['max_length'] for x in file_line_lengths])),
                'mean': float(np.mean([x['mean_length'] for x in file_line_lengths])),
                'median': float(np.median([x['median_length'] for x in file_line_lengths])),
                'std': float(np.mean([x['std_length'] for x in file_line_lengths])),
                'files_with_long_lines': sum(1 for x in file_line_lengths if x['long_lines_count'] > 0),
                'total_long_lines': sum(x['long_lines_count'] for x in file_line_lengths),
                'total_files': len(file_line_lengths)
            }
        }
        
        return all_stats
