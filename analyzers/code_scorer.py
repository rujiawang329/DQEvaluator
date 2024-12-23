"""代码质量打分器"""
import numpy as np
from config.scoring_config import SCORING_CONFIG

class CodeScorer:
    def __init__(self, config=None):
        """初始化打分器
        
        Args:
            config: 打分配置，如果为None则使用默认配置
        """
        self.config = config or SCORING_CONFIG
        
    def score_code_length(self, length_stats):
        """评估代码长度
        
        Args:
            length_stats: 长度统计信息
            
        Returns:
            float: 得分(0-100)
        """
        metrics = self.config['code_length_metrics']
        score = 100.0
        
        # 评估文件长度分布
        mean_length = length_stats['length_distribution']['mean']
        if mean_length > metrics['max_file_length']:
            score *= 0.7
        elif mean_length < metrics['min_file_length']:
            score *= 0.8
            
        # 评估行长度
        if length_stats['line_length_stats']['long_lines_ratio'] > metrics['long_lines_threshold']:
            score *= 0.8
            
        return score
    
    def score_line_stats(self, complexity_stats):
        """评估行统计信息
        
        Args:
            complexity_stats: 复杂度统计信息
            
        Returns:
            float: 得分(0-100)
        """
        metrics = self.config['line_stats_metrics']
        score = 100.0
        
        # 评估注释比例
        comment_ratio = complexity_stats['comment_lines_ratio']['mean']
        if comment_ratio < metrics['comment_ratio_min']:
            score *= 0.7
        elif comment_ratio > metrics['comment_ratio_max']:
            score *= 0.9
            
        # 评估空行比例
        blank_ratio = complexity_stats['blank_lines_ratio']['mean']
        if blank_ratio < metrics['blank_ratio_min']:
            score *= 0.7
        elif blank_ratio > metrics['blank_ratio_max']:
            score *= 0.9
            
        # 评估代码比例
        code_ratio = complexity_stats['code_lines_ratio']['mean']
        if code_ratio < metrics['code_ratio_min']:
            score *= 0.8
        elif code_ratio > metrics['code_ratio_max']:
            score *= 0.9
            
        return score
    
    def score_complexity(self, entropy_stats):
        """评估代码复杂度
        
        Args:
            entropy_stats: 熵统计信息
            
        Returns:
            float: 得分(0-100)
        """
        metrics = self.config['complexity_metrics']
        score = 100.0
        
        # 评估熵值分布
        mean_entropy = entropy_stats['global_entropy_stats']['mean']
        if mean_entropy > metrics['max_entropy']:
            score *= 0.7
        elif mean_entropy < metrics['min_entropy']:
            score *= 0.8
            
        # 评估代码块类型分布
        block_stats = entropy_stats['block_stats']
        total_blocks = block_stats['total_blocks']
        if total_blocks > 0:
            for block_type, threshold in metrics['block_type_thresholds'].items():
                type_count = block_stats['block_type_counts'].get(block_type, 0)
                type_ratio = type_count / total_blocks
                if type_ratio < threshold:
                    score *= 0.9
                    
        return score
    
    def score_duplication(self, duplication_stats):
        """评估代码重复度
        
        Args:
            duplication_stats: 重复度统计信息
            
        Returns:
            float: 得分(0-100)
        """
        metrics = self.config['duplication_metrics']
        score = 100.0
        
        # 评估重复率
        if duplication_stats['line_level']['ratios']['mean'] > metrics['max_duplication_ratio']:
            score *= 0.7
            
        # 评估高重复文件比例
        high_dup_ratio = duplication_stats['line_level']['high_duplication_count'] / duplication_stats['line_level']['total_files']
        if high_dup_ratio > metrics['high_duplication_ratio']:
            score *= 0.8
            
        # 评估重复块
        if 'block_level' in duplication_stats:
            blocks = duplication_stats['block_level']
            if len(blocks['top_blocks']) > metrics['max_identical_blocks']:
                score *= 0.9
                
        return score
    
    def score_entropy(self, entropy_stats):
        """评估代码熵
        
        Args:
            entropy_stats: 熵统计信息
            
        Returns:
            float: 得分(0-100)
        """
        metrics = self.config['entropy_metrics']
        score = 100.0
        
        block_stats = entropy_stats['block_stats']
        total_blocks = block_stats['total_blocks']
        
        if total_blocks == 0:
            return score
            
        # 评估代码块分布
        for block_type, weight in metrics['block_distribution'].items():
            type_count = next((block['count'] for block in block_stats['top_blocks'] 
                             if block['block'] == block_type), 0)
            type_ratio = type_count / total_blocks
            
            if type_ratio < weight:
                score *= (0.9 + 0.1 * (type_ratio / weight))
                
        return score
    
    def calculate_final_score(self, scores):
        """计算最终得分
        
        Args:
            scores: 各维度得分
            
        Returns:
            dict: 最终得分和评级
        """
        weights = self.config['weights']
        
        # 计算加权得分
        final_score = (
            scores['code_length'] * weights['code_length'] +
            scores['line_stats'] * weights['line_stats'] +
            scores['complexity'] * weights['complexity'] +
            scores['duplication'] * weights['duplication'] +
            scores['entropy'] * weights['entropy']
        )
        
        # 确定评级
        if final_score >= 90:
            grade = 'A'
        elif final_score >= 80:
            grade = 'B'
        elif final_score >= 70:
            grade = 'C'
        elif final_score >= 60:
            grade = 'D'
        else:
            grade = 'F'
            
        return {
            'score': final_score,
            'grade': grade,
            'dimension_scores': scores
        }
    
    def score_codebase(self, analysis_results):
        """对代码库进行打分
        
        Args:
            analysis_results: 分析结果
            
        Returns:
            dict: 打分结果
        """
        # 计算各维度得分
        scores = {
            'code_length': self.score_code_length(analysis_results['length_stats']),
            'line_stats': self.score_line_stats(analysis_results['complexity_stats']),
            'complexity': self.score_complexity(analysis_results['entropy_stats']),
            'duplication': self.score_duplication(analysis_results['duplication_stats']),
            'entropy': self.score_entropy(analysis_results['entropy_stats'])
        }
        
        # 计算最终得分
        return self.calculate_final_score(scores)
