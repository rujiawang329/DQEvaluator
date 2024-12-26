"""
Copyright (c) 2024 Rujia Wang

This file is part of DQEvaluator, licensed under custom license.
See LICENSE file in the project root for license information.
"""

#!/usr/bin/env python3
import os
import json
import pandas as pd
from datetime import datetime
from tqdm import tqdm
import numpy as np
from pathlib import Path
from typing import Dict, List, Tuple

from analyzers.length_analyzer import LengthAnalyzer
from analyzers.complexity_analyzer import ComplexityAnalyzer
from analyzers.duplication_analyzer import DuplicationAnalyzer
from analyzers.entropy_analyzer import EntropyAnalyzer
from analyzers.code_scorer import CodeScorer
from visualizers.code_visualizer import CodeVisualizer

def load_csv_data(file_path: str) -> pd.DataFrame:
    """加载CSV文件数据"""
    try:
        df = pd.read_csv(file_path)
        print(f"\nSuccessfully loaded {file_path}")
        print(f"Records count: {len(df)}\n")
        return df
    except Exception as e:
        print(f"Error loading {file_path}: {str(e)}")
        return None

def analyze_code(df: pd.DataFrame, pbar: tqdm) -> Dict:
    """分析代码并返回结果"""
    results = {}
    
    # 长度分析
    length_analyzer = LengthAnalyzer()
    results['length_stats'] = {
        'length_distribution': length_analyzer.analyze_code_length(df).to_dict(),
        'line_count_distribution': length_analyzer.analyze_line_counts(df).to_dict(),
        'line_length_stats': length_analyzer.analyze_line_lengths(df)
    }
    pbar.update(25)
    
    # 复杂度分析
    complexity_analyzer = ComplexityAnalyzer()
    results['complexity_stats'] = complexity_analyzer.analyze_code_complexity(df)
    pbar.update(25)
    
    # 重复度分析
    duplication_analyzer = DuplicationAnalyzer()
    results['duplication_stats'] = duplication_analyzer.analyze_code_duplication(df)
    pbar.update(25)
    
    # 熵分析
    entropy_analyzer = EntropyAnalyzer()
    results['entropy_stats'] = entropy_analyzer.analyze_code_entropy(df)
    pbar.update(25)
    
    return results

def print_analysis_stats(results: Dict, file_name: str):
    """打印分析统计信息"""
    print(f"\n=== Analysis Statistics for {file_name} ===")
    
    # 长度统计
    print("\n--- Code Length Statistics ---")
    length_stats = results['length_stats']
    print("\nLength Distribution:")
    print(pd.Series(length_stats['length_distribution']))
    print("\nLine Count Distribution:")
    print(pd.Series(length_stats['line_count_distribution']))
    print("\nLine Length Statistics:")
    ll_stats = length_stats['line_length_stats']
    print(f"Average line length: {ll_stats['mean']:.2f} characters")
    print(f"Median line length: {ll_stats['median']:.2f} characters")
    print(f"Shortest line: {ll_stats['min']:.1f} characters")
    print(f"Longest line: {ll_stats['max']:.1f} characters")
    print(f"Standard deviation: {ll_stats['std']:.2f} characters")
    print(f"Files with long lines (>80 chars): {ll_stats['files_with_long_lines']} ({ll_stats['long_lines_ratio']*100:.2f}%)")
    print(f"Total long lines: {ll_stats['total_long_lines']}")
    
    # 复杂度统计
    print("\n--- Code Complexity Statistics ---")
    complexity_stats = results['complexity_stats']
    print("\nLine Type Ratios (mean):")
    print(f"Blank Lines: {complexity_stats['blank_lines_ratio']['mean']:.2%}")
    print(f"Comment Lines: {complexity_stats['comment_lines_ratio']['mean']:.2%}")
    print(f"Code Lines: {complexity_stats['code_lines_ratio']['mean']:.2%}")
    
    # 重复度统计
    print("\n--- Code Duplication Statistics ---")
    duplication_stats = results['duplication_stats']
    line_stats = duplication_stats['line_level']
    print("\nLine-level Duplication:")
    print(f"Average duplication ratio: {line_stats['ratios']['mean']:.2%}")
    print(f"Median duplication ratio: {line_stats['ratios']['median']:.2%}")
    print(f"Files with high duplication: {line_stats['high_duplication_count']} ({line_stats['high_duplication_count']/line_stats['total_files']:.2%})")
    
    # 熵统计
    print("\n--- Code Entropy Statistics ---")
    entropy_stats = results['entropy_stats']
    stats = entropy_stats['global_entropy_stats']
    print("\nGlobal Entropy Statistics:")
    print(f"Mean: {stats['mean']:.3f}")
    print(f"Median: {stats['median']:.3f}")
    print(f"Std: {stats['std']:.3f}")
    print(f"Min: {stats['min']:.3f}")
    print(f"Max: {stats['max']:.3f}")
    
    print("\nTop 5 Most Used Verilog Blocks:")
    for block in entropy_stats['block_stats']['top_blocks'][:5]:
        print(f"  {block['block']}: {block['count']} occurrences")

def save_analysis_report(results: Dict, stats_dir: str, filename: str) -> Tuple[str, str]:
    """保存分析报告和统计信息"""
    # 创建文件名（不带扩展名）
    base_name = f"{Path(filename).stem}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    # 创建报告目录
    report_dir = os.path.join(stats_dir, base_name)
    os.makedirs(report_dir, exist_ok=True)
    
    # 保存JSON报告
    report_path = os.path.join(report_dir, f"{base_name}_report.json")
    with open(report_path, 'w') as f:
        json.dump(results, f, indent=4)
    
    # 保存统计信息
    stats_path = os.path.join(report_dir, f"{base_name}_stats.txt")
    with open(stats_path, 'w') as f:
        # 重定向print输出到文件
        import sys
        original_stdout = sys.stdout
        sys.stdout = f
        print_analysis_stats(results, filename)
        sys.stdout = original_stdout
    
    return report_dir, report_path

def generate_visualizations(results: Dict, df: pd.DataFrame, output_dir: str, visualizer: CodeVisualizer):
    """生成可视化图表"""
    # 代码长度分布
    visualizer.plot_length_distribution(
        lengths=df['text'].str.len(),
        title='Distribution of Code Lengths',
        output_dir=output_dir
    )
    
    # 行长度分布
    visualizer.plot_line_length_distribution(
        line_lengths=[len(line) for code in df['text'] for line in code.split('\n')],
        output_dir=output_dir
    )
    
    # 复杂度分布
    visualizer.plot_complexity_distribution(
        complexity_ratio=results['complexity_stats']['code_lines_ratio']['mean'],
        output_dir=output_dir
    )
    
    # 重复度分析
    visualizer.plot_duplication_analysis(
        duplication_stats=results['duplication_stats'],
        output_dir=output_dir
    )
    
    # 熵分析
    visualizer.plot_entropy_analysis(
        entropy_stats=results['entropy_stats'],
        output_dir=output_dir
    )

def print_score_summary(scores: Dict, title: str = ""):
    """打印评分摘要"""
    print(f"\n=== {title} ===")
    print(f"Final Score: {scores['score']:.1f}")
    print(f"Grade: {scores['grade']}")
    print("\nDimension Scores:")
    for dim, score in scores['dimension_scores'].items():
        print(f"  {dim}: {score:.1f}")

def calculate_dataset_average(all_scores: List[Dict]) -> Dict:
    """计算数据集的平均分数"""
    if not all_scores:
        return None
        
    avg_scores = {
        'dimension_scores': {},
        'score': 0,
    }
    
    # 计算各维度平均分
    dims = all_scores[0]['dimension_scores'].keys()
    for dim in dims:
        scores = [s['dimension_scores'][dim] for s in all_scores]
        avg_scores['dimension_scores'][dim] = np.mean(scores)
    
    # 计算总分平均分
    avg_scores['score'] = np.mean([s['score'] for s in all_scores])
    
    # 确定总体评级
    if avg_scores['score'] >= 90:
        avg_scores['grade'] = 'A'
    elif avg_scores['score'] >= 80:
        avg_scores['grade'] = 'B'
    elif avg_scores['score'] >= 70:
        avg_scores['grade'] = 'C'
    elif avg_scores['score'] >= 60:
        avg_scores['grade'] = 'D'
    else:
        avg_scores['grade'] = 'F'
        
    return avg_scores

def main():
    # 设置数据和输出目录
    data_dir = "data"
    stats_dir = "results"
    os.makedirs(stats_dir, exist_ok=True)
    
    # 获取所有CSV文件
    csv_files = [f for f in os.listdir(data_dir) if f.endswith('.csv')]
    total_files = len(csv_files)
    
    if total_files == 0:
        print(f"No CSV files found in the {data_dir} directory!")
        return
        
    print(f"\nFound {total_files} CSV files to analyze")
    
    # 初始化评分器和可视化器
    scorer = CodeScorer()
    visualizer = CodeVisualizer()
    all_scores = []
    
    # 总进度条
    with tqdm(total=total_files, desc="Total Progress", position=0) as total_pbar:
        for csv_file in csv_files:
            print(f"\nProcessing: {csv_file}")
            
            # 加载数据
            df = load_csv_data(os.path.join(data_dir, csv_file))
            if df is None:
                total_pbar.update(1)
                continue
                
            # 单文件进度条
            with tqdm(total=100, desc="File Progress", position=1, leave=False) as file_pbar:
                # 分析代码
                results = analyze_code(df, file_pbar)
                
                # 评分
                scores = scorer.score_codebase(results)
                all_scores.append(scores)
                
                # 保存报告和统计信息
                report_dir, report_path = save_analysis_report(results, stats_dir, csv_file)
                
                # 生成可视化
                generate_visualizations(results, df, report_dir, visualizer)
                
                # 打印单文件评分结果
                print_score_summary(scores, f"Code Quality Score - {csv_file}")
                print(f"\nAnalysis report and visualizations saved to: {report_dir}")
            
            total_pbar.update(1)
    
    # 计算并打印数据集平均分
    dataset_avg = calculate_dataset_average(all_scores)
    if dataset_avg:
        print("\n" + "="*50)
        print_score_summary(dataset_avg, "Dataset Average Scores")
        print("="*50)

if __name__ == "__main__":
    main()
