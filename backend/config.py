"""
配置文件，包含应用的所有配置项
"""
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class Config:
    """基础配置类"""
    # Flask配置
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev')
    DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    
    # MQTT配置
    MQTT_BROKER = os.getenv('BROKER_IP', 'localhost')
    MQTT_PORT = int(os.getenv('BROKER_PORT', '1883'))
    MQTT_DEVICE_PREFIX = os.getenv('DEVICE_PREFIX', 'smart_home')
    
    # 设备更新间隔（秒）
    DEVICE_UPDATE_INTERVAL = 10
    
    # 设备类型映射
    DEVICE_TYPES = {
        "light": {
            "name": "智能灯",
            "commands": {
                "turn_on": "开灯",
                "turn_off": "关灯",
                "set_brightness": "设置亮度",
                "set_color_temp": "设置色温"
            }
        },
        "thermostat": {
            "name": "温控器",
            "commands": {
                "set_mode": "设置模式",
                "set_target_temp": "设置目标温度"
            }
        },
        "doorlock": {
            "name": "智能门锁",
            "commands": {
                "lock": "上锁",
                "unlock": "解锁",
                "check_battery": "检查电池"
            }
        }
    }

class DevelopmentConfig(Config):
    """开发环境配置"""
    DEBUG = True

class ProductionConfig(Config):
    """生产环境配置"""
    DEBUG = False

# 配置映射
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

# 获取当前配置
def get_config():
    """获取当前环境的配置"""
    env = os.getenv('FLASK_ENV', 'default')
    return config[env] 