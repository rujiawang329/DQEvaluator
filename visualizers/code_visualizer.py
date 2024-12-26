"""
Copyright (c) 2024 Rujia Wang

This file is part of DQEvaluator, licensed under custom license.
See LICENSE file in the project root for license information.
"""

import os
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from typing import List, Dict, Union

class CodeVisualizer:
    def __init__(self):
        """初始化代码可视化器"""
        # 设置图表样式
        plt.style.use('seaborn')
        sns.set_palette("husl")
    
    def plot_length_distribution(self, lengths: List[int], title: str, output_dir: str):
        """绘制代码长度分布图"""
        plt.figure(figsize=(10, 6))
        sns.histplot(lengths, bins=50)
        plt.title(title)
        plt.xlabel('Code Length (characters)')
        plt.ylabel('Frequency')
        
        # 保存图表
        plt.savefig(os.path.join(output_dir, 'length_distribution.png'))
        plt.close()
    
    def plot_line_length_distribution(self, line_lengths: List[int], output_dir: str):
        """绘制行长度分布图"""
        plt.figure(figsize=(10, 6))
        sns.histplot(line_lengths, bins=50)
        plt.title('Distribution of Line Lengths')
        plt.xlabel('Line Length (characters)')
        plt.ylabel('Frequency')
        plt.axvline(x=80, color='r', linestyle='--', label='80 characters limit')
        plt.legend()
        
        # 保存图表
        plt.savefig(os.path.join(output_dir, 'line_length_distribution.png'))
        plt.close()
    
    def plot_complexity_distribution(self, complexity_ratio: float, output_dir: str):
        """绘制代码复杂度分布图"""
        plt.figure(figsize=(8, 6))
        
        # 创建饼图
        labels = ['Code', 'Non-Code']
        sizes = [complexity_ratio, 1 - complexity_ratio]
        colors = ['#ff9999', '#66b3ff']
        
        plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
        plt.title('Code vs Non-Code Ratio')
        
        # 保存图表
        plt.savefig(os.path.join(output_dir, 'complexity_distribution.png'))
        plt.close()
    
    def plot_duplication_analysis(self, duplication_stats: Dict, output_dir: str):
        """绘制代码重复度分析图"""
        line_stats = duplication_stats['line_level']
        
        plt.figure(figsize=(10, 6))
        
        # 绘制重复率分布
        ratios = [r for r in line_stats['ratios'].values() if isinstance(r, (int, float))]
        sns.histplot(ratios, bins=30)
        plt.title('Distribution of Duplication Ratios')
        plt.xlabel('Duplication Ratio')
        plt.ylabel('Frequency')
        
        # 添加平均值和中位数线
        plt.axvline(x=line_stats['ratios']['mean'], color='r', linestyle='--', label='Mean')
        plt.axvline(x=line_stats['ratios']['median'], color='g', linestyle='--', label='Median')
        plt.legend()
        
        # 保存图表
        plt.savefig(os.path.join(output_dir, 'duplication_analysis.png'))
        plt.close()
        
        # 绘制重复模式类型分布
        if 'pattern_types' in line_stats:
            plt.figure(figsize=(10, 6))
            pattern_types = line_stats['pattern_types']
            plt.bar(pattern_types.keys(), pattern_types.values())
            plt.title('Distribution of Duplicate Pattern Types')
            plt.xlabel('Pattern Type')
            plt.ylabel('Count')
            plt.xticks(rotation=45)
            
            # 保存图表
            plt.savefig(os.path.join(output_dir, 'duplication_patterns.png'))
            plt.close()
    
    def plot_entropy_analysis(self, entropy_stats: Dict, output_dir: str):
        """绘制代码熵分析图"""
        stats = entropy_stats['global_entropy_stats']
        
        # 绘制熵分布箱线图
        plt.figure(figsize=(10, 6))
        entropy_values = [
            stats['min'],
            stats['mean'] - stats['std'],
            stats['mean'],
            stats['mean'] + stats['std'],
            stats['max']
        ]
        
        plt.boxplot(entropy_values)
        plt.title('Code Entropy Distribution')
        plt.ylabel('Entropy Value')
        
        # 添加统计值标注
        plt.text(1.1, stats['mean'], f'Mean: {stats["mean"]:.2f}', verticalalignment='center')
        plt.text(1.1, stats['median'], f'Median: {stats["median"]:.2f}', verticalalignment='center')
        
        # 保存图表
        plt.savefig(os.path.join(output_dir, 'entropy_analysis.png'))
        plt.close()
        
        # 绘制最常用的Verilog块分布
        if 'block_stats' in entropy_stats and 'top_blocks' in entropy_stats['block_stats']:
            plt.figure(figsize=(12, 6))
            top_blocks = entropy_stats['block_stats']['top_blocks'][:10]  # 只显示前10个
            
            blocks = [block['block'] for block in top_blocks]
            counts = [block['count'] for block in top_blocks]
            
            plt.bar(range(len(blocks)), counts)
            plt.title('Top 10 Most Used Verilog Blocks')
            plt.xlabel('Block Type')
            plt.ylabel('Frequency')
            plt.xticks(range(len(blocks)), blocks, rotation=45, ha='right')
            
            # 保存图表
            plt.savefig(os.path.join(output_dir, 'verilog_blocks.png'))
            plt.close()
