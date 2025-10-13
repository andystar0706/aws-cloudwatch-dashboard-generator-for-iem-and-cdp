import re
import json
import time
import logging

def is_integer(value):
    """基本整數判斷"""
    pattern = r'^-?\d+$'
    return bool(re.match(pattern, str(value)))

def is_valid_word(value):
    """
    判斷是否為有效單字
    - 排除 None
    - 排除空字符串 ''
    - 排除純空白字符串 '   '
    """
    if value is None:
        return False
        
    if not isinstance(value, str):
        return False
        
    if not value.strip():  # 處理空字符串和純空白
        return False
        
    return True

def is_valid_statistic(value):
    """
    判斷是否為有效的 CloudWatch statistic
    
    Valid values:
    - SampleCount
    - Average
    - Sum
    - Minimum
    - Maximum
    - p[0-9]{1,2}(\.[0-9]+)? (例如: p90, p95, p99, p99.9)
    """
    if not isinstance(value, str):
        return False
        
    # 基本統計方法
    basic_stats = {'SampleCount', 'Average', 'Sum', 'Minimum', 'Maximum'}
    if value in basic_stats:
        return True
        
    # 百分位數檢查 (p + 數字)
    if value.startswith('p'):
        try:
            percentile = float(value[1:])  # 轉換 'p' 後面的數字
            return 0 <= percentile <= 100
        except ValueError:
            return False
            
    return False

def save_to_json(data, filename):
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error saving to JSON: {e}")
        return False
    
def get_current_timestamp() -> str:
    """
    獲取當前的 Unix timestamp (字符串格式)
    Returns:
        str: Unix timestamp string
    """
    return str(int(time.time()))

def get_logger(name):
    logging.basicConfig(
        filename = 'dashboard.log',
        level = logging.INFO,
        format = "%(asctime)s [%(levelname)s] %(name)s - %(message)s",
        datefmt = "%Y-%m-%d %H:%M:%S"
    )
    logger = logging.getLogger(name)
    return logger

def load_json_config(file_path: str) -> list:
    """Load JSON configuration file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return []
    
if __name__ == '__main__':
    print(is_valid_statistic('AVG'))
    print(is_valid_statistic('Average'))
    print(is_valid_statistic('p50'))
    print(is_valid_statistic('P50'))
    print(is_valid_statistic('PP50'))
    print(is_valid_statistic('P500'))
    print(get_current_timestamp())
