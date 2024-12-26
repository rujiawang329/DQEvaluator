"""
Copyright (c) 2024 Rujia Wang

This file is part of DQEvaluator, licensed under custom license.
See LICENSE file in the project root for license information.
"""

"""代码重复分析器"""
from collections import defaultdict
import numpy as np
from utils.code_utils import preprocess_code, normalize_line
from config.analysis_config import DUPLICATION_CONFIG

class DuplicationAnalyzer:
    def __init__(self, config=None):
        """初始化重复分析器
        
        Args:
            config: 分析配置，如果为None则使用默认配置
        """
        self.config = config or DUPLICATION_CONFIG
        
        # 设置块分析参数
        block_config = self.config['block_analysis']
        self.min_block_size = block_config['min_block_size']
        self.max_block_size = block_config['max_block_size']
        self.block_sample_size = block_config['sample_size']
        self.min_file_lines = block_config['min_file_lines']
        
        # 设置行分析参数
        line_config = self.config['line_analysis']
        self.min_line_length = line_config['min_line_length']
        self.high_duplication_threshold = line_config['high_duplication_threshold']
        
        # 设置通用参数
        self.random_seed = self.config['general']['random_seed']

    def find_line_duplicates(self, code_lines):
        """查找代码中的行级重复"""
        line_patterns = defaultdict(list)
        original_lines = {}  # 保存原始行用于展示
        
        for i, line in enumerate(code_lines):
            if len(line) > self.min_line_length:  # 忽略很短的行
                normalized = normalize_line(line)
                line_patterns[normalized].append(i)
                if normalized not in original_lines:
                    original_lines[normalized] = line
        
        # 找出重复的模式
        duplicates = {pattern: {
            'lines': lines,
            'original': original_lines[pattern],
            'count': len(lines)
        } for pattern, lines in line_patterns.items() 
        if len(lines) > 1}
        
        if not code_lines:
            return 0, 0, {}
        
        # 计算行级重复率
        total_lines = len(code_lines)
        duplicated_lines = sum(len(info['lines']) - 1 for info in duplicates.values())
        duplication_ratio = duplicated_lines / total_lines if total_lines > 0 else 0
        
        return duplication_ratio, len(duplicates), duplicates

    def find_duplicate_blocks(self, code_lines):
        """使用滑动窗口和哈希方法查找重复代码块"""
        block_hashes = defaultdict(list)
        duplicate_blocks = []
        
        # 计算步长（跳过一些行以提高性能）
        step = max(1, len(code_lines) // 1000)  # 对于大文件使用更大的步长
        
        # 对不同大小的块进行查找
        for block_size in range(self.min_block_size, min(self.max_block_size + 1, len(code_lines))):
            # 使用滑动窗口计算每个块的哈希值，使用步长来跳过一些位置
            for i in range(0, len(code_lines) - block_size + 1, step):
                block = code_lines[i:i + block_size]
                # 标准化并连接块中的行
                normalized_block = '\n'.join(normalize_line(line) for line in block)
                block_hash = hash(normalized_block)
                
                # 记录相同哈希值的块位置
                block_hashes[block_hash].append((i, block))
        
        # 收集重复块信息
        seen_positions = set()
        for block_hash, positions in block_hashes.items():
            if len(positions) > 1:  # 找到重复块
                # 检查是否与已找到的块重叠
                current_positions = set(range(pos[0], pos[0] + len(pos[1])) 
                                     for pos in positions)
                
                # 如果这个块与已找到的块没有重叠，添加到结果中
                if not any(pos in seen_positions for positions_set in current_positions 
                          for pos in positions_set):
                    duplicate_blocks.append({
                        'lines': [pos[0] for pos in positions],
                        'size': len(positions[0][1]),
                        'count': len(positions),
                        'example': '\n'.join(positions[0][1])
                    })
                    # 更新已见过的位置
                    for positions_set in current_positions:
                        seen_positions.update(positions_set)
        
        return duplicate_blocks

    def analyze_code_duplication(self, df):
        """分析代码重复情况"""
        # 设置随机种子
        np.random.seed(self.random_seed)
        
        # 第一阶段：对所有文件进行行级重复分析
        print("\nAnalyzing line-level duplications for all files...")
        line_duplication_ratios = []
        line_duplicate_patterns = []
        all_line_duplicates = []
        
        for code in df['text']:
            processed_lines = preprocess_code(code)
            ratio, num_patterns, patterns = self.find_line_duplicates(processed_lines)
            line_duplication_ratios.append(ratio)
            line_duplicate_patterns.append(num_patterns)
            if patterns:
                all_line_duplicates.extend(patterns.items())
        
        # 第二阶段：对抽样文件进行块级重复分析
        print(f"\nAnalyzing block-level duplications for {self.block_sample_size} sample files...")
        sampled_indices = np.random.choice(len(df), self.block_sample_size, replace=False)
        df_sample = df.iloc[sampled_indices]
        
        all_block_duplicates = []
        for code in df_sample['text']:
            processed_lines = preprocess_code(code)
            if len(processed_lines) >= self.min_file_lines:  # 只对较长的文件进行块分析
                block_duplicates = self.find_duplicate_blocks(processed_lines)
                if block_duplicates:
                    all_block_duplicates.extend(block_duplicates)
        
        # 分析重复模式类型
        pattern_types = {
            'variable': 0,  # 变量名变化
            'number': 0,    # 数值变化
            'mixed': 0,     # 混合变化
            'other': 0      # 其他
        }
        
        # 统计最常见的重复模式
        pattern_frequency = defaultdict(int)
        for pattern, info in all_line_duplicates:
            pattern_frequency[pattern] += info['count']
            
            # 判断模式类型
            if 'VAR' in pattern and ('BIN' in pattern or 'HEX' in pattern or 'DEC' in pattern or 'NUM' in pattern):
                pattern_types['mixed'] += 1
            elif 'VAR' in pattern:
                pattern_types['variable'] += 1
            elif 'BIN' in pattern or 'HEX' in pattern or 'DEC' in pattern or 'NUM' in pattern:
                pattern_types['number'] += 1
            else:
                pattern_types['other'] += 1
        
        # 获取最常见的重复模式
        top_patterns = sorted(all_line_duplicates, key=lambda x: x[1]['count'], reverse=True)[:5]
        
        # 获取最大的重复块
        top_blocks = sorted(all_block_duplicates, 
                          key=lambda x: x['size'] * (x['count'] - 1), 
                          reverse=True)[:5]
        
        return {
            'line_level': {
                'ratios': {
                    'mean': float(np.mean(line_duplication_ratios)),
                    'std': float(np.std(line_duplication_ratios)),
                    'min': float(np.min(line_duplication_ratios)),
                    'max': float(np.max(line_duplication_ratios)),
                    'median': float(np.median(line_duplication_ratios))
                },
                'patterns': {
                    'mean': float(np.mean(line_duplicate_patterns)),
                    'std': float(np.std(line_duplicate_patterns)),
                    'min': float(np.min(line_duplicate_patterns)),
                    'max': float(np.max(line_duplicate_patterns)),
                    'median': float(np.median(line_duplicate_patterns))
                },
                'pattern_types': pattern_types,
                'top_patterns': [
                    {
                        'pattern': pattern,
                        'example': info['original'],
                        'count': info['count']
                    }
                    for pattern, info in top_patterns
                ],
                'high_duplication_count': sum(1 for r in line_duplication_ratios 
                                            if r >= self.high_duplication_threshold),
                'total_files': len(line_duplication_ratios)
            },
            'block_level': {
                'total_blocks': len(all_block_duplicates),
                'top_blocks': [
                    {
                        'size': block['size'],
                        'count': block['count'],
                        'example': block['example']
                    }
                    for block in top_blocks
                ],
                'sample_size': self.block_sample_size,
                'config': {
                    'min_block_size': self.min_block_size,
                    'max_block_size': self.max_block_size,
                    'min_file_lines': self.min_file_lines
                }
            }
        }
