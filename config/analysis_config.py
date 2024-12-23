"""分析配置参数"""

# 代码重复分析配置
DUPLICATION_CONFIG = {
    # 块分析配置
    'block_analysis': {
        'min_block_size': 3,        # 最小重复块大小（行数）
        'max_block_size': 20,       # 最大重复块大小（行数）
        'sample_size': 30,          # 块分析的样本文件数量
        'min_file_lines': 10,       # 进行块分析的最小文件行数
    },
    
    # 行分析配置
    'line_analysis': {
        'min_line_length': 5,       # 最小行长度，小于此长度的行将被忽略
        'high_duplication_threshold': 0.3,  # 高重复率阈值（30%）
    },
    
    # 通用配置
    'general': {
        'random_seed': 42,          # 随机种子，用于采样
    }
}

# 代码复杂度分析配置
COMPLEXITY_CONFIG = {
    'min_file_size': 10,           # 最小文件大小（字节）
    'max_file_size': 1000000,      # 最大文件大小（字节）
}

# 代码长度分析配置
LENGTH_CONFIG = {
    'long_line_threshold': 80,      # 长行阈值（字符数）
    'max_line_length': 200,         # 可视化时的最大行长度
}

# Verilog代码熵分析配置
ENTROPY_CONFIG = {
    # Verilog语法块权重
    'block_weights': {
        # 时序逻辑相关
        'always_ff': 2.0,       # 时序always块
        'always_posedge': 1.8,  # 上升沿触发
        'always_negedge': 1.8,  # 下降沿触发
        
        # 组合逻辑相关
        'always_comb': 1.8,     # 组合always块
        'assign': 1.5,          # 组合逻辑赋值
        'case': 1.6,            # case语句块
        'if_else': 1.4,         # if-else块
        
        # 数据类型定义
        'reg_def': 1.2,         # 寄存器定义
        'wire_def': 1.2,        # 线网定义
        'logic_def': 1.2,       # SystemVerilog逻辑类型定义
        
        # 模块接口
        'port_def': 1.5,        # 端口定义块
        'parameter_def': 1.4,   # 参数定义块
        'localparameter': 1.3,  # 本地参数定义
        
        # 结构化设计
        'module_def': 2.0,      # 模块定义块
        'function_def': 1.7,    # 函数定义块
        'task_def': 1.7,        # 任务定义块
        'generate': 1.6,        # generate块
        
        # 验证相关
        'initial': 1.3,         # 仿真初始化块
        'assert': 1.4,          # 断言语句
        'property': 1.5,        # 属性定义
        
        # 其他常用结构
        'typedef': 1.3,         # 类型定义
        'enum': 1.4,            # 枚举定义
        'struct': 1.5,          # 结构体定义
    },
    
    # 分析窗口大小
    'window_size': 50,         # 滑动窗口大小（行数）
    
    # 分析阈值
    'thresholds': {
        'low_entropy': 0.3,    # 低熵阈值
        'high_entropy': 0.7,   # 高熵阈值
    }
}

# 可视化配置
VISUALIZATION_CONFIG = {
    'figure_size': (10, 6),         # 图表大小
    'hist_bins': 50,                # 直方图箱数
    'dpi': 300,                     # 图表DPI
}
