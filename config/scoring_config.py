"""
Copyright (c) 2024 Rujia Wang

This file is part of DQEvaluator, licensed under custom license.
See LICENSE file in the project root for license information.
"""

"""打分配置"""

SCORING_CONFIG = {
    # 代码长度指标
    'code_length_metrics': {
        'max_file_length': 3000,     # 单文件最大行数
        'min_file_length': 30,       # 单文件最小行数
        'long_lines_threshold': 0.25,  # 长行比例阈值
        'max_line_length': 100,       # 单行最大字符数
    },
    
    # 行统计指标
    'line_stats_metrics': {
        'comment_ratio_min': 0.25,    # 最小注释比例
        'comment_ratio_max': 0.35,    # 最大注释比例
        'blank_ratio_min': 0.15,      # 最小空行比例
        'blank_ratio_max': 0.2,      # 最大空行比例
        'code_ratio_min': 0.45,       # 最小代码比例
        'code_ratio_max': 0.6,       # 最大代码比例
    },
    
    # 复杂度指标
    'complexity_metrics': {
        'max_entropy': 0.65,          # 最大熵值
        'min_entropy': 0.25,          # 最小熵值
        'block_type_thresholds': {   # 代码块类型比例阈值
            'Sequential': 0.12,        # 时序逻辑最小比例
            'Combinational': 0.25,     # 组合逻辑最小比例
            'Data Types': 0.12,        # 数据类型最小比例
            'Module Interface': 0.25,  # 模块接口最小比例
            'Design Structure': 0.12,  # 设计结构最小比例
            'Verification': 0.08      # 验证代码最小比例
        }
    },
    
    # 重复度指标
    'duplication_metrics': {
        'max_duplication_ratio': 0.12,     # 最大重复率
        'high_duplication_ratio': 0.08,    # 高重复文件比例阈值
        'max_identical_blocks': 3,        # 最大相同代码块数
        'min_duplicate_block_lines': 5,   # 最小重复块行数
    },
    
    # 熵分析指标
    'entropy_metrics': {
        'block_distribution': {           # 代码块分布权重
            'port_def': 0.2,            # 端口定义
            'parameter_def': 0.12,         # 参数定义
            'wire_def': 0.12,             # 线网定义
            'reg_def': 0.12,              # 寄存器定义
            'assign': 0.15,              # 组合逻辑赋值
            'always_posedge': 0.15,      # 时序逻辑
            'if_else': 0.08,              # 条件语句
            'case': 0.08,                 # 分支语句
            'module_def': 0.05           # 模块定义
        }
    },
    
    # 权重配置
    'weights': {
        'code_length': 0.15,      # 代码长度权重
        'line_stats': 0.3,       # 行统计权重
        'complexity': 0.2,       # 复杂度权重
        'duplication': 0.25,      # 重复度权重
        'entropy': 0.1           # 熵分析权重
    }
}
