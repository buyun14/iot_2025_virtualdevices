"""
基础设备模型
"""
from abc import ABC, abstractmethod
from datetime import datetime
import random
from typing import Dict, Any

class BaseDevice(ABC):
    """基础设备类，定义了所有设备共有的属性和方法"""
    
    def __init__(self, device_id: str):
        """
        初始化基础设备
        
        Args:
            device_id (str): 设备唯一标识符
        """
        self.device_id = device_id
        self.type = self.__class__.__name__.lower()
        self.last_update = datetime.now()
        self.online = True
        self.error_state = None
    
    def to_dict(self) -> Dict[str, Any]:
        """
        将设备状态转换为字典格式
        
        Returns:
            Dict[str, Any]: 包含设备状态的字典
        """
        return {
            "type": self.type,
            "online": self.online,
            "last_update": self.last_update.isoformat(),
            "error_state": self.error_state,
            **self.get_state()
        }
    
    @abstractmethod
    def get_state(self) -> Dict[str, Any]:
        """
        获取设备当前状态
        
        Returns:
            Dict[str, Any]: 设备状态字典
        """
        pass
    
    @abstractmethod
    def handle_command(self, command: Dict[str, Any]) -> None:
        """
        处理设备控制命令
        
        Args:
            command (Dict[str, Any]): 控制命令字典
        """
        pass
    
    def update_status(self):
        """更新设备状态时间戳"""
        self.last_update = datetime.now()
        # 模拟设备偶尔离线
        if random.random() < 0.01:  # 1%的概率设备离线
            self.online = False
            self.error_state = "设备连接异常"
        else:
            self.online = True
            self.error_state = None 