"""代码复杂度分析器"""
import numpy as np
from utils.code_utils import preprocess_code, is_comment_line, is_blank_line

class ComplexityAnalyzer:
    def analyze_code_complexity(self, df):
        """分析代码复杂度"""
        blank_lines_ratio = []
        comment_lines_ratio = []
        code_lines_ratio = []

        for code in df['text']:
            lines = preprocess_code(code)
            if not lines:
                continue

            total_lines = len(lines)
            blank_count = sum(1 for line in lines if is_blank_line(line))
            comment_count = sum(1 for line in lines if is_comment_line(line))
            code_count = total_lines - blank_count - comment_count

            blank_lines_ratio.append(blank_count / total_lines if total_lines > 0 else 0)
            comment_lines_ratio.append(comment_count / total_lines if total_lines > 0 else 0)
            code_lines_ratio.append(code_count / total_lines if total_lines > 0 else 0)

        return {
            'blank_lines_ratio': {
                'mean': float(np.mean(blank_lines_ratio)),
                'std': float(np.std(blank_lines_ratio)),
                'min': float(np.min(blank_lines_ratio)),
                'max': float(np.max(blank_lines_ratio))
            },
            'comment_lines_ratio': {
                'mean': float(np.mean(comment_lines_ratio)),
                'std': float(np.std(comment_lines_ratio)),
                'min': float(np.min(comment_lines_ratio)),
                'max': float(np.max(comment_lines_ratio))
            },
            'code_lines_ratio': {
                'mean': float(np.mean(code_lines_ratio)),
                'std': float(np.std(code_lines_ratio)),
                'min': float(np.min(code_lines_ratio)),
                'max': float(np.max(code_lines_ratio))
            }
        }
