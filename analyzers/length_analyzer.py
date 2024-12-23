"""代码长度分析器"""
import pandas as pd
from utils.code_utils import preprocess_code

class LengthAnalyzer:
    def analyze_code_length(self, df):
        """分析代码长度统计
        
        Args:
            df: 包含代码的DataFrame
            
        Returns:
            pd.Series: 代码长度统计
        """
        code_lengths = df['text'].str.len()
        return code_lengths.describe()

    def analyze_line_counts(self, df):
        """分析代码行数统计
        
        Args:
            df: 包含代码的DataFrame
            
        Returns:
            pd.Series: 代码行数统计
        """
        line_counts = df['text'].apply(lambda x: len(preprocess_code(x)))
        return line_counts.describe()

    def analyze_line_lengths(self, df):
        """分析代码行长度统计
        
        Args:
            df: 包含代码的DataFrame
            
        Returns:
            dict: 代码行长度统计
        """
        # 收集所有行的长度
        line_lengths = []
        total_files = len(df)
        files_with_long_lines = 0
        total_long_lines = 0
        
        for code in df['text']:
            has_long_line = False
            for line in code.split('\n'):
                length = len(line)
                line_lengths.append(length)
                if length > 80:
                    total_long_lines += 1
                    has_long_line = True
            if has_long_line:
                files_with_long_lines += 1
        
        # 计算统计信息
        line_lengths = pd.Series(line_lengths)
        stats = line_lengths.describe()
        
        return {
            'mean': stats['mean'],
            'std': stats['std'],
            'min': stats['min'],
            'max': stats['max'],
            'median': stats['50%'],
            'total_files': total_files,
            'files_with_long_lines': files_with_long_lines,
            'total_long_lines': total_long_lines,
            'long_lines_count': files_with_long_lines,
            'long_lines_ratio': files_with_long_lines / total_files
        }
