"""
Copyright (c) 2024 Rujia Wang

This file is part of DQEvaluator, licensed under custom license.
See LICENSE file in the project root for license information.
"""

"""Verilog代码熵分析器"""
import numpy as np
from collections import Counter, defaultdict
import re
from config.analysis_config import ENTROPY_CONFIG

class EntropyAnalyzer:
    def __init__(self, config=None):
        """初始化熵分析器
        
        Args:
            config: 分析配置，如果为None则使用默认配置
        """
        self.config = config or ENTROPY_CONFIG
        self.block_weights = self.config['block_weights']
        self.window_size = self.config['window_size']
        self.thresholds = self.config['thresholds']
        
        # 编译正则表达式
        self.patterns = {
            # 时序逻辑相关
            'always_ff': re.compile(r'\balways_ff\b'),
            'always_posedge': re.compile(r'\balways\s*@\s*\(\s*posedge\b'),
            'always_negedge': re.compile(r'\balways\s*@\s*\(\s*negedge\b'),
            
            # 组合逻辑相关
            'always_comb': re.compile(r'\balways_comb\b'),
            'assign': re.compile(r'\bassign\b'),
            'case': re.compile(r'\bcase[xz]?\b'),
            'if_else': re.compile(r'\bif\b|\belse\b'),
            
            # 数据类型定义
            'reg_def': re.compile(r'\breg\b\s+[a-zA-Z_]\w*'),
            'wire_def': re.compile(r'\bwire\b\s+[a-zA-Z_]\w*'),
            'logic_def': re.compile(r'\blogic\b\s+[a-zA-Z_]\w*'),
            
            # 模块接口
            'port_def': re.compile(r'\b(input|output|inout)\b'),
            'parameter_def': re.compile(r'\bparameter\b'),
            'localparameter': re.compile(r'\blocalparam\b'),
            
            # 结构化设计
            'module_def': re.compile(r'\bmodule\s+[a-zA-Z_]\w*'),
            'function_def': re.compile(r'\bfunction\b'),
            'task_def': re.compile(r'\btask\b'),
            'generate': re.compile(r'\bgenerate\b'),
            
            # 验证相关
            'initial': re.compile(r'\binitial\b'),
            'assert': re.compile(r'\bassert\b'),
            'property': re.compile(r'\bproperty\b'),
            
            # 其他常用结构
            'typedef': re.compile(r'\btypedef\b'),
            'enum': re.compile(r'\benum\b'),
            'struct': re.compile(r'\bstruct\b'),
        }
        
        # 代码块类型映射
        self.block_mapping = {
            'Sequential': ['always_ff', 'always_posedge', 'always_negedge'],
            'Combinational': ['always_comb', 'assign', 'case', 'if_else'],
            'Data Types': ['reg_def', 'wire_def', 'logic_def'],
            'Module Interface': ['port_def', 'parameter_def', 'localparameter'],
            'Design Structure': ['module_def', 'function_def', 'task_def', 'generate'],
            'Verification': ['initial', 'assert', 'property'],
            'Others': ['typedef', 'enum', 'struct']
        }
    
    def analyze_block_entropy(self, code_text):
        """分析代码块的熵
        
        Args:
            code_text: 代码文本
            
        Returns:
            dict: 代码块熵分析结果
        """
        # 统计每种代码块的出现次数
        block_counts = {
            block_type: len(pattern.findall(code_text))
            for block_type, pattern in self.patterns.items()
        }
        
        # 计算总权重
        total_weight = sum(
            count * self.block_weights[block_type]
            for block_type, count in block_counts.items()
        )
        
        if total_weight == 0:
            return {
                'entropy': 0,
                'block_counts': block_counts,
            }
        
        # 计算每个块的加权频率
        weighted_frequencies = {
            block_type: (count * self.block_weights[block_type]) / total_weight
            for block_type, count in block_counts.items()
            if count > 0
        }
        
        # 计算熵
        entropy = -sum(
            freq * np.log2(freq)
            for freq in weighted_frequencies.values()
            if freq > 0
        )
        
        # 归一化熵
        max_entropy = np.log2(len(self.block_weights))
        normalized_entropy = entropy / max_entropy if max_entropy > 0 else 0
        
        return {
            'entropy': normalized_entropy,
            'block_counts': block_counts,
        }
    
    def analyze_code_entropy(self, df):
        """分析所有代码文件的信息熵
        
        Args:
            df: 包含代码的DataFrame
            
        Returns:
            dict: 熵分析结果
        """
        print("\nAnalyzing code entropy...")
        
        # 初始化统计
        all_block_counts = Counter()
        all_entropies = []
        
        # 分析每个文件
        for code in df['text']:
            result = self.analyze_block_entropy(code)
            all_entropies.append(result['entropy'])
            all_block_counts.update(result['block_counts'])
        
        # 计算每种代码块类型的总数
        block_type_counts = {
            block_type: sum(
                all_block_counts[block]
                for block in blocks
            )
            for block_type, blocks in self.block_mapping.items()
        }
        
        # 计算总体统计信息
        return {
            'global_entropy_stats': {
                'mean': float(np.mean(all_entropies)),
                'std': float(np.std(all_entropies)),
                'min': float(np.min(all_entropies)),
                'max': float(np.max(all_entropies)),
                'median': float(np.median(all_entropies))
            },
            'block_stats': {
                'total_blocks': sum(all_block_counts.values()),
                'block_counts': dict(all_block_counts),
                'block_type_counts': block_type_counts,
                'top_blocks': [
                    {'block': block, 'count': count}
                    for block, count in all_block_counts.most_common(10)
                ]
            },
            'config': self.config
        }
