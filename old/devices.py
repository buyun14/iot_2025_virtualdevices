"""
智能家居设备模拟模块

此模块包含了各种智能家居设备的类定义，每个类都实现了特定设备的功能和行为。
所有设备类都继承自基础设备类 BaseDevice，确保统一的接口和基本功能。
"""

from abc import ABC, abstractmethod
import json
from typing import Dict, Any, Optional
from datetime import datetime
import random

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
        self.color_temp = 4000  # 色温（开尔文）
        self.power_consumption = 0  # 功率消耗（瓦特）
    
    def get_state(self) -> Dict[str, Any]:
        return {
            "state": self.state,
            "brightness": self.brightness,
            "color_temp": self.color_temp,
            "power_consumption": self.power_consumption
        }
    
    def handle_command(self, command: Dict[str, Any]) -> None:
        cmd_type = command.get("command")
        if cmd_type == "turn_on":
            self.state = "on"
            self.power_consumption = self.brightness * 0.1  # 模拟功率消耗
        elif cmd_type == "turn_off":
            self.state = "off"
            self.power_consumption = 0
        elif cmd_type == "set_brightness":
            try:
                brightness = int(command.get("brightness", 100))
                self.brightness = max(0, min(100, brightness))
                if self.state == "on":
                    self.power_consumption = self.brightness * 0.1
            except (ValueError, TypeError):
                self.error_state = "无效的亮度值"
        elif cmd_type == "set_color_temp":
            try:
                temp = int(command.get("color_temp", 4000))
                self.color_temp = max(2700, min(6500, temp))
            except (ValueError, TypeError):
                self.error_state = "无效的色温值"
        self.update_status()

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
        self.humidity = 50
        self.mode = "auto"  # auto, heat, cool
        self.fan_speed = "auto"  # auto, low, medium, high
    
    def get_state(self) -> Dict[str, Any]:
        return {
            "current_temp": self.current_temp,
            "target_temp": self.target_temp,
            "humidity": self.humidity,
            "mode": self.mode,
            "fan_speed": self.fan_speed
        }
    
    def handle_command(self, command: Dict[str, Any]) -> None:
        cmd_type = command.get("command")
        if cmd_type == "set_target_temp":
            try:
                temp = float(command.get("temperature", 24))
                self.target_temp = max(16, min(30, temp))
            except (ValueError, TypeError):
                self.error_state = "无效的温度值"
        elif cmd_type == "set_mode":
            mode = command.get("mode", "auto")
            if mode in ["auto", "heat", "cool"]:
                self.mode = mode
            else:
                self.error_state = "无效的模式"
        elif cmd_type == "set_fan_speed":
            speed = command.get("speed", "auto")
            if speed in ["auto", "low", "medium", "high"]:
                self.fan_speed = speed
            else:
                self.error_state = "无效的风速"
        self.update_status()
    
    def update_current_temp(self, temp: float) -> None:
        """更新当前温度和湿度"""
        self.current_temp = temp
        # 模拟湿度变化
        self.humidity = max(30, min(80, self.humidity + random.uniform(-2, 2)))
        self.update_status()

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
        self.battery_level = 100
        self.last_lock_time = None
        self.last_unlock_time = None
    
    def get_state(self) -> Dict[str, Any]:
        return {
            "locked": self.locked,
            "battery_level": self.battery_level,
            "last_lock_time": self.last_lock_time,
            "last_unlock_time": self.last_unlock_time
        }
    
    def handle_command(self, command: Dict[str, Any]) -> None:
        cmd_type = command.get("command")
        if cmd_type == "lock":
            self.locked = True
            self.last_lock_time = datetime.now().isoformat()
            self.battery_level = max(0, self.battery_level - 0.1)
        elif cmd_type == "unlock":
            self.locked = False
            self.last_unlock_time = datetime.now().isoformat()
            self.battery_level = max(0, self.battery_level - 0.1)
        self.update_status()

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
        self.tilt = 0  # 0-180度
        self.moving = False
        self.last_move_time = None
    
    def get_state(self) -> Dict[str, Any]:
        return {
            "position": self.position,
            "tilt": self.tilt,
            "moving": self.moving,
            "last_move_time": self.last_move_time
        }
    
    def handle_command(self, command: Dict[str, Any]) -> None:
        cmd_type = command.get("command")
        if cmd_type == "open":
            self.position = 100
            self.moving = True
        elif cmd_type == "close":
            self.position = 0
            self.moving = True
        elif cmd_type == "set_position":
            try:
                position = int(command.get("position", 0))
                self.position = max(0, min(100, position))
                self.moving = True
            except (ValueError, TypeError):
                self.error_state = "无效的位置值"
        elif cmd_type == "set_tilt":
            try:
                tilt = int(command.get("tilt", 0))
                self.tilt = max(0, min(180, tilt))
            except (ValueError, TypeError):
                self.error_state = "无效的倾斜角度"
        
        if self.moving:
            self.last_move_time = datetime.now().isoformat()
            # 模拟移动完成
            self.moving = False
        self.update_status()

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
        self.mode = "cool"  # cool, heat, dry, fan
        self.fan_speed = "auto"  # auto, low, medium, high
        self.swing = False
        self.power_consumption = 0
    
    def get_state(self) -> Dict[str, Any]:
        return {
            "on": self.on,
            "temp": self.temp,
            "mode": self.mode,
            "fan_speed": self.fan_speed,
            "swing": self.swing,
            "power_consumption": self.power_consumption
        }
    
    def handle_command(self, command: Dict[str, Any]) -> None:
        cmd_type = command.get("command")
        if cmd_type == "turn_on":
            self.on = True
            self.power_consumption = 1000  # 模拟功率消耗
        elif cmd_type == "turn_off":
            self.on = False
            self.power_consumption = 0
        elif cmd_type == "set_temp":
            try:
                temp = float(command.get("temperature", 26))
                self.temp = max(16, min(30, temp))
            except (ValueError, TypeError):
                self.error_state = "无效的温度值"
        elif cmd_type == "set_mode":
            mode = command.get("mode", "cool")
            if mode in ["cool", "heat", "dry", "fan"]:
                self.mode = mode
            else:
                self.error_state = "无效的模式"
        elif cmd_type == "set_fan_speed":
            speed = command.get("speed", "auto")
            if speed in ["auto", "low", "medium", "high"]:
                self.fan_speed = speed
            else:
                self.error_state = "无效的风速"
        elif cmd_type == "toggle_swing":
            self.swing = not self.swing
        self.update_status()

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
        self.battery_level = 100
        self.smoke_level = 0  # 0-100
        self.last_test_time = None
    
    def get_state(self) -> Dict[str, Any]:
        return {
            "alarm": self.alarm,
            "battery_level": self.battery_level,
            "smoke_level": self.smoke_level,
            "last_test_time": self.last_test_time
        }
    
    def handle_command(self, command: Dict[str, Any]) -> None:
        cmd_type = command.get("command")
        if cmd_type == "reset":
            self.alarm = False
            self.smoke_level = 0
        elif cmd_type == "test":
            self.last_test_time = datetime.now().isoformat()
            self.battery_level = max(0, self.battery_level - 0.5)
        self.update_status()
    
    def trigger_alarm(self) -> None:
        """触发烟雾报警"""
        self.alarm = True
        self.smoke_level = random.randint(50, 100)
        self.update_status()

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
        self.speed = 1  # 1-3
        self.oscillate = False
        self.timer = 0  # 定时关闭时间（分钟）
        self.power_consumption = 0
    
    def get_state(self) -> Dict[str, Any]:
        return {
            "on": self.on,
            "speed": self.speed,
            "oscillate": self.oscillate,
            "timer": self.timer,
            "power_consumption": self.power_consumption
        }
    
    def handle_command(self, command: Dict[str, Any]) -> None:
        cmd_type = command.get("command")
        if cmd_type == "turn_on":
            self.on = True
            self.power_consumption = self.speed * 20  # 模拟功率消耗
        elif cmd_type == "turn_off":
            self.on = False
            self.power_consumption = 0
        elif cmd_type == "set_speed":
            try:
                speed = int(command.get("speed", 1))
                self.speed = max(1, min(3, speed))
                if self.on:
                    self.power_consumption = self.speed * 20
            except (ValueError, TypeError):
                self.error_state = "无效的风速值"
        elif cmd_type == "toggle_oscillate":
            self.oscillate = not self.oscillate
        elif cmd_type == "set_timer":
            try:
                timer = int(command.get("minutes", 0))
                self.timer = max(0, min(120, timer))
            except (ValueError, TypeError):
                self.error_state = "无效的定时值"
        self.update_status()

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
        self.power_consumption = 0
        self.voltage = 220
        self.current = 0
        self.power_factor = 0.95
        self.timer = 0  # 定时关闭时间（分钟）
    
    def get_state(self) -> Dict[str, Any]:
        return {
            "on": self.on,
            "power_consumption": self.power_consumption,
            "voltage": self.voltage,
            "current": self.current,
            "power_factor": self.power_factor,
            "timer": self.timer
        }
    
    def handle_command(self, command: Dict[str, Any]) -> None:
        cmd_type = command.get("command")
        if cmd_type == "turn_on":
            self.on = True
            self.power_consumption = random.uniform(50, 200)  # 模拟功率消耗
            self.current = self.power_consumption / self.voltage
        elif cmd_type == "turn_off":
            self.on = False
            self.power_consumption = 0
            self.current = 0
        elif cmd_type == "set_timer":
            try:
                timer = int(command.get("minutes", 0))
                self.timer = max(0, min(120, timer))
            except (ValueError, TypeError):
                self.error_state = "无效的定时值"
        self.update_status() 