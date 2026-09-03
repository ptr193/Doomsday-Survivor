# -*- coding: utf-8 -*-

import random
import logging
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional

class GameUtils:
    """游戏工具类"""
    
    @staticmethod
    def format_time(seconds: int) -> str:
        """格式化时间显示"""
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60
        
        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{secs:02d}"
        else:
            return f"{minutes:02d}:{secs:02d}"
    
    @staticmethod
    def format_number(number: int) -> str:
        """格式化数字显示"""
        if number >= 1000000:
            return f"{number/1000000:.1f}M"
        elif number >= 1000:
            return f"{number/1000:.1f}K"
        else:
            return str(number)
    
    @staticmethod
    def calculate_distance(x1: float, y1: float, x2: float, y2: float) -> float:
        """计算两点之间的距离"""
        return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
    
    @staticmethod
    def get_random_weighted_choice(choices: List[Any], weights: List[float]) -> Any:
        """加权随机选择"""
        if len(choices) != len(weights):
            raise ValueError("Choices and weights must have the same length")
        
        total = sum(weights)
        r = random.uniform(0, total)
        current = 0
        
        for i, weight in enumerate(weights):
            current += weight
            if r <= current:
                return choices[i]
        
        return choices[-1]  # 防止浮点数误差
    
    @staticmethod
    def clamp(value: float, min_val: float, max_val: float) -> float:
        """限制数值范围"""
        return max(min_val, min(value, max_val))
    
    @staticmethod
    def lerp(start: float, end: float, factor: float) -> float:
        """线性插值"""
        return start + (end - start) * factor
    
    @staticmethod
    def ease_in_out(t: float) -> float:
        """缓动函数"""
        return t * t * (3 - 2 * t)
    
    @staticmethod
    def generate_id(prefix: str = "") -> str:
        """生成唯一ID"""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        random_str = ''.join(random.choices('0123456789abcdef', k=6))
        return f"{prefix}{timestamp}_{random_str}"
    
    @staticmethod
    def calculate_experience_required(level: int, base_exp: int = 100) -> int:
        """计算升级所需经验值"""
        return int(base_exp * (level ** 1.5))
    
    @staticmethod
    def calculate_level(exp: int, base_exp: int = 100) -> int:
        """根据经验值计算等级"""
        level = 1
        while exp >= GameUtils.calculate_experience_required(level, base_exp):
            exp -= GameUtils.calculate_experience_required(level, base_exp)
            level += 1
        return level
    
    @staticmethod
    def calculate_skill_modifier(skill_level: int, base_value: float = 1.0) -> float:
        """计算技能修正值"""
        return base_value * (1 + (skill_level - 1) * 0.1)
    
    @staticmethod
    def format_duration(seconds: int) -> str:
        """格式化持续时间"""
        if seconds < 60:
            return f"{seconds}秒"
        elif seconds < 3600:
            minutes = seconds // 60
            return f"{minutes}分钟"
        elif seconds < 86400:
            hours = seconds // 3600
            return f"{hours}小时"
        else:
            days = seconds // 86400
            return f"{days}天"

class FileUtils:
    """文件工具类"""
    
    @staticmethod
    def ensure_directory(directory: str) -> bool:
        """确保目录存在"""
        try:
            os.makedirs(directory, exist_ok=True)
            return True
        except Exception as e:
            logging.error(f"创建目录失败: {e}")
            return False
    
    @staticmethod
    def read_json_file(file_path: str) -> Optional[Dict[str, Any]]:
        """读取JSON文件"""
        try:
            if not os.path.exists(file_path):
                return None
            
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logging.error(f"读取JSON文件失败: {e}")
            return None
    
    @staticmethod
    def write_json_file(file_path: str, data: Dict[str, Any]) -> bool:
        """写入JSON文件"""
        try:
            # 确保目录存在
            directory = os.path.dirname(file_path)
            FileUtils.ensure_directory(directory)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            logging.error(f"写入JSON文件失败: {e}")
            return False
    
    @staticmethod
    def read_text_file(file_path: str) -> Optional[str]:
        """读取文本文件"""
        try:
            if not os.path.exists(file_path):
                return None
            
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            logging.error(f"读取文本文件失败: {e}")
            return None
    
    @staticmethod
    def write_text_file(file_path: str, content: str) -> bool:
        """写入文本文件"""
        try:
            directory = os.path.dirname(file_path)
            FileUtils.ensure_directory(directory)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        except Exception as e:
            logging.error(f"写入文本文件失败: {e}")
            return False
    
    @staticmethod
    def list_files(directory: str, extension: str = None) -> List[str]:
        """列出目录中的文件"""
        try:
            if not os.path.exists(directory):
                return []
            
            files = []
            for filename in os.listdir(directory):
                file_path = os.path.join(directory, filename)
                if os.path.isfile(file_path):
                    if extension is None or filename.endswith(extension):
                        files.append(filename)
            return files
        except Exception as e:
            logging.error(f"列出文件失败: {e}")
            return []
    
    @staticmethod
    def get_file_size(file_path: str) -> Optional[int]:
        """获取文件大小（字节）"""
        try:
            return os.path.getsize(file_path)
        except Exception as e:
            logging.error(f"获取文件大小失败: {e}")
            return None
    
    @staticmethod
    def backup_file(file_path: str, backup_suffix: str = ".bak") -> bool:
        """备份文件"""
        try:
            if not os.path.exists(file_path):
                return False
            
            backup_path = file_path + backup_suffix
            import shutil
            shutil.copy2(file_path, backup_path)
            return True
        except Exception as e:
            logging.error(f"备份文件失败: {e}")
            return False

class MathUtils:
    """数学工具类"""
    
    @staticmethod
    def probability(percent: float) -> bool:
        """概率判断"""
        return random.random() < (percent / 100.0)
    
    @staticmethod
    def random_int(min_val: int, max_val: int) -> int:
        """生成随机整数"""
        return random.randint(min_val, max_val)
    
    @staticmethod
    def random_float(min_val: float, max_val: float) -> float:
        """生成随机浮点数"""
        return random.uniform(min_val, max_val)
    
    @staticmethod
    def random_choice(choices: List[Any]) -> Any:
        """随机选择"""
        return random.choice(choices)
    
    @staticmethod
    def random_sample(choices: List[Any], count: int) -> List[Any]:
        """随机抽样"""
        return random.sample(choices, min(count, len(choices)))
    
    @staticmethod
    def calculate_percentage(part: float, whole: float) -> float:
        """计算百分比"""
        if whole == 0:
            return 0.0
        return (part / whole) * 100.0
    
    @staticmethod
    def calculate_average(numbers: List[float]) -> float:
        """计算平均值"""
        if not numbers:
            return 0.0
        return sum(numbers) / len(numbers)
    
    @staticmethod
    def calculate_median(numbers: List[float]) -> float:
        """计算中位数"""
        if not numbers:
            return 0.0
        
        sorted_numbers = sorted(numbers)
        n = len(sorted_numbers)
        
        if n % 2 == 0:
            return (sorted_numbers[n//2 - 1] + sorted_numbers[n//2]) / 2
        else:
            return sorted_numbers[n//2]
    
    @staticmethod
    def normalize_value(value: float, min_val: float, max_val: float) -> float:
        """归一化数值"""
        if max_val == min_val:
            return 0.0
        return (value - min_val) / (max_val - min_val)
    
    @staticmethod
    def denormalize_value(normalized: float, min_val: float, max_val: float) -> float:
        """反归一化数值"""
        return min_val + normalized * (max_val - min_val)

class TextUtils:
    """文本工具类"""
    
    @staticmethod
    def truncate_text(text: str, max_length: int, ellipsis: str = "...") -> str:
        """截断文本"""
        if len(text) <= max_length:
            return text
        
        return text[:max_length - len(ellipsis)] + ellipsis
    
    @staticmethod
    def wrap_text(text: str, width: int) -> List[str]:
        """文本换行"""
        words = text.split()
        lines = []
        current_line = []
        current_length = 0
        
        for word in words:
            word_length = len(word)
            
            # 如果当前行为空，或者加上这个词不会超过宽度
            if not current_line or current_length + word_length + 1 <= width:
                current_line.append(word)
                current_length += word_length + (1 if current_line else 0)
            else:
                lines.append(' '.join(current_line))
                current_line = [word]
                current_length = word_length
        
        if current_line:
            lines.append(' '.join(current_line))
        
        return lines
    
    @staticmethod
    def format_list(items: List[str], conjunction: str = "和") -> str:
        """格式化列表"""
        if not items:
            return ""
        elif len(items) == 1:
            return items[0]
        elif len(items) == 2:
            return f"{items[0]} {conjunction} {items[1]}"
        else:
            return f"{', '.join(items[:-1})} {conjunction} {items[-1]}"
    
    @staticmethod
    def capitalize_first(text: str) -> str:
        """首字母大写"""
        if not text:
            return text
        return text[0].upper() + text[1:]
    
    @staticmethod
    def remove_extra_spaces(text: str) -> str:
        """移除多余空格"""
        return ' '.join(text.split())
    
    @staticmethod
    def generate_random_name() -> str:
        """生成随机名字"""
        first_names = ["张", "王", "李", "赵", "陈", "刘", "杨", "黄", "周", "吴"]
        last_names = ["明", "伟", "芳", "娜", "秀英", "强", "静", "霞", "建军", "艳"]
        return random.choice(first_names) + random.choice(last_names)

class TimeUtils:
    """时间工具类"""
    
    @staticmethod
    def get_current_timestamp() -> float:
        """获取当前时间戳"""
        return datetime.now().timestamp()
    
    @staticmethod
    def format_datetime(dt: datetime, format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
        """格式化日期时间"""
        return dt.strftime(format_str)
    
    @staticmethod
    def parse_datetime(datetime_str: str, format_str: str = "%Y-%m-%d %H:%M:%S") -> Optional[datetime]:
        """解析日期时间"""
        try:
            return datetime.strptime(datetime_str, format_str)
        except ValueError:
            return None
    
    @staticmethod
    def add_days(dt: datetime, days: int) -> datetime:
        """添加天数"""
        return dt + timedelta(days=days)
    
    @staticmethod
    def add_hours(dt: datetime, hours: int) -> datetime:
        """添加小时"""
        return dt + timedelta(hours=hours)
    
    @staticmethod
    def add_minutes(dt: datetime, minutes: int) -> datetime:
        """添加分钟"""
        return dt + timedelta(minutes=minutes)
    
    @staticmethod
    def is_same_day(dt1: datetime, dt2: datetime) -> bool:
        """判断是否为同一天"""
        return dt1.date() == dt2.date()
    
    @staticmethod
    def get_days_between(start_dt: datetime, end_dt: datetime) -> int:
        """计算天数差"""
        return (end_dt.date() - start_dt.date()).days
    
    @staticmethod
    def get_time_of_day(hour: int) -> str:
        """获取时间段描述"""
        if 5 <= hour < 8:
            return "清晨"
        elif 8 <= hour < 12:
            return "上午"
        elif 12 <= hour < 14:
            return "中午"
        elif 14 <= hour < 18:
            return "下午"
        elif 18 <= hour < 22:
            return "晚上"
        else:
            return "深夜"

class ValidationUtils:
    """验证工具类"""
    
    @staticmethod
    def is_valid_email(email: str) -> bool:
        """验证邮箱格式"""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def is_valid_filename(filename: str) -> bool:
        """验证文件名"""
        import re
        # 不允许的字符
        invalid_chars = r'[<>:"/\\|?*\x00-\x1f]'
        return re.search(invalid_chars, filename) is None
    
    @staticmethod
    def is_within_range(value: float, min_val: float, max_val: float) -> bool:
        """验证数值范围"""
        return min_val <= value <= max_val
    
    @staticmethod
    def is_positive_number(value: float) -> bool:
        """验证正数"""
        return value > 0
    
    @staticmethod
    def is_non_negative_number(value: float) -> bool:
        """验证非负数"""
        return value >= 0
    
    @staticmethod
    def validate_dict_structure(data: Dict, required_keys: List[str]) -> bool:
        """验证字典结构"""
        return all(key in data for key in required_keys)

class DebugUtils:
    """调试工具类"""
    
    @staticmethod
    def log_performance(func):
        """性能日志装饰器"""
        def wrapper(*args, **kwargs):
            start_time = datetime.now()
            result = func(*args, **kwargs)
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            logging.debug(f"函数 {func.__name__} 执行时间: {duration:.3f}秒")
            return result
        return wrapper
    
    @staticmethod
    def measure_execution_time(func, *args, **kwargs) -> float:
        """测量执行时间"""
        start_time = datetime.now()
        func(*args, **kwargs)
        end_time = datetime.now()
        return (end_time - start_time).total_seconds()
    
    @staticmethod
    def get_memory_usage() -> Optional[float]:
        """获取内存使用情况（MB）"""
        try:
            import psutil
            process = psutil.Process()
            return process.memory_info().rss / 1024 / 1024
        except ImportError:
            logging.warning("psutil 未安装，无法获取内存使用情况")
            return None
    
    @staticmethod
    def create_debug_report() -> Dict[str, Any]:
        """创建调试报告"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'python_version': os.sys.version,
            'platform': os.sys.platform,
            'current_directory': os.getcwd(),
            'memory_usage': DebugUtils.get_memory_usage()
        }
        return report
