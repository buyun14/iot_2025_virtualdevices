"""
智能家居设备模拟模块

此模块包含了各种智能家居设备的类定义，每个类都实现了特定设备的功能和行为。
所有设备类都继承自基础设备类 BaseDevice，确保统一的接口和基本功能。
"""

from abc import ABC, abstractmethod
import json
from typing import Dict, Any, Optional

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
    
    def to_dict(self) -> Dict[str, Any]:
        """
        将设备状态转换为字典格式
        
        Returns:
            Dict[str, Any]: 包含设备状态的字典
        """
        return {
            "type": self.type,
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

class Light(BaseDevice):
    """智能灯设备类"""
    
    def __init__(self, device_id: str):
        """
        初始化智能灯设备
        
        Args:
            device_id (str): 设备唯一标识符
        """
        super().__init__(device_id)
        self.state = "off"
        self.brightness = 50
    
    def get_state(self) -> Dict[str, Any]:
        return {
            "state": self.state,
            "brightness": self.brightness
        }
    
    def handle_command(self, command: Dict[str, Any]) -> None:
        cmd_type = command.get("command")
        if cmd_type == "turn_on":
            self.state = "on"
        elif cmd_type == "turn_off":
            self.state = "off"
        elif cmd_type == "set_brightness":
            self.brightness = command.get("brightness", 100)

class Thermostat(BaseDevice):
    """温控器设备类"""
    
    def __init__(self, device_id: str):
        """
        初始化温控器设备
        
        Args:
            device_id (str): 设备唯一标识符
        """
        super().__init__(device_id)
        self.current_temp = 22
        self.target_temp = 24
    
    def get_state(self) -> Dict[str, Any]:
        return {
            "current_temp": self.current_temp,
            "target_temp": self.target_temp
        }
    
    def handle_command(self, command: Dict[str, Any]) -> None:
        cmd_type = command.get("command")
        if cmd_type == "set_target_temp":
            self.target_temp = command.get("temperature", 24)
    
    def update_current_temp(self, temp: float) -> None:
        """
        更新当前温度
        
        Args:
            temp (float): 新的温度值
        """
        self.current_temp = temp

class DoorLock(BaseDevice):
    """智能门锁设备类"""
    
    def __init__(self, device_id: str):
        """
        初始化智能门锁设备
        
        Args:
            device_id (str): 设备唯一标识符
        """
        super().__init__(device_id)
        self.locked = True
    
    def get_state(self) -> Dict[str, Any]:
        return {"locked": self.locked}
    
    def handle_command(self, command: Dict[str, Any]) -> None:
        cmd_type = command.get("command")
        if cmd_type == "lock":
            self.locked = True
        elif cmd_type == "unlock":
            self.locked = False

class Blind(BaseDevice):
    """智能窗帘设备类"""
    
    def __init__(self, device_id: str):
        """
        初始化智能窗帘设备
        
        Args:
            device_id (str): 设备唯一标识符
        """
        super().__init__(device_id)
        self.position = 0  # 0-100%
    
    def get_state(self) -> Dict[str, Any]:
        return {"position": self.position}
    
    def handle_command(self, command: Dict[str, Any]) -> None:
        cmd_type = command.get("command")
        if cmd_type == "open":
            self.position = 100
        elif cmd_type == "close":
            self.position = 0
        elif cmd_type == "set_position":
            self.position = command.get("position", 0)

class AirConditioner(BaseDevice):
    """空调设备类"""
    
    def __init__(self, device_id: str):
        """
        初始化空调设备
        
        Args:
            device_id (str): 设备唯一标识符
        """
        super().__init__(device_id)
        self.on = False
        self.temp = 26
    
    def get_state(self) -> Dict[str, Any]:
        return {
            "on": self.on,
            "temp": self.temp
        }
    
    def handle_command(self, command: Dict[str, Any]) -> None:
        cmd_type = command.get("command")
        if cmd_type == "turn_on":
            self.on = True
        elif cmd_type == "turn_off":
            self.on = False
        elif cmd_type == "set_temp":
            self.temp = command.get("temperature", 26)

class SmokeDetector(BaseDevice):
    """烟雾报警器设备类"""
    
    def __init__(self, device_id: str):
        """
        初始化烟雾报警器设备
        
        Args:
            device_id (str): 设备唯一标识符
        """
        super().__init__(device_id)
        self.alarm = False
    
    def get_state(self) -> Dict[str, Any]:
        return {"alarm": self.alarm}
    
    def handle_command(self, command: Dict[str, Any]) -> None:
        cmd_type = command.get("command")
        if cmd_type == "reset":
            self.alarm = False
    
    def trigger_alarm(self) -> None:
        """触发烟雾报警"""
        self.alarm = True

class Fan(BaseDevice):
    """风扇设备类"""
    
    def __init__(self, device_id: str):
        """
        初始化风扇设备
        
        Args:
            device_id (str): 设备唯一标识符
        """
        super().__init__(device_id)
        self.on = False
        self.speed = 1
    
    def get_state(self) -> Dict[str, Any]:
        return {
            "on": self.on,
            "speed": self.speed
        }
    
    def handle_command(self, command: Dict[str, Any]) -> None:
        cmd_type = command.get("command")
        if cmd_type == "turn_on":
            self.on = True
        elif cmd_type == "turn_off":
            self.on = False
        elif cmd_type == "set_speed":
            self.speed = command.get("speed", 1)

class Plug(BaseDevice):
    """智能插座设备类"""
    
    def __init__(self, device_id: str):
        """
        初始化智能插座设备
        
        Args:
            device_id (str): 设备唯一标识符
        """
        super().__init__(device_id)
        self.on = False
    
    def get_state(self) -> Dict[str, Any]:
        return {"on": self.on}
    
    def handle_command(self, command: Dict[str, Any]) -> None:
        cmd_type = command.get("command")
        if cmd_type == "turn_on":
            self.on = True
        elif cmd_type == "turn_off":
            self.on = False 