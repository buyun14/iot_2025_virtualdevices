"""
温控器设备模型
"""
from typing import Dict, Any
from .base import BaseDevice

class Thermostat(BaseDevice):
    """温控器设备类"""
    
    def __init__(self, device_id: str):
        """
        初始化温控器设备
        
        Args:
            device_id (str): 设备唯一标识符
        """
        super().__init__(device_id)
        self.mode = "auto"  # auto, heat, cool, off
        self.target_temp = 22.0  # 目标温度
        self.current_temp = 22.0  # 当前温度
        self.humidity = 50  # 湿度
        self.power_consumption = 0  # 功率消耗（瓦特）
    
    def get_state(self) -> Dict[str, Any]:
        return {
            "mode": self.mode,
            "target_temp": self.target_temp,
            "current_temp": self.current_temp,
            "humidity": self.humidity,
            "power_consumption": self.power_consumption
        }
    
    def handle_command(self, command: Dict[str, Any]) -> None:
        cmd_type = command.get("command")
        if cmd_type == "set_mode":
            mode = command.get("mode")
            if mode in ["auto", "heat", "cool", "off"]:
                self.mode = mode
                self._update_power_consumption()
        elif cmd_type == "set_target_temp":
            try:
                temp = float(command.get("temperature", 22.0))
                self.target_temp = max(16.0, min(30.0, temp))
                self._update_power_consumption()
            except (ValueError, TypeError):
                self.error_state = "无效的温度值"
        self.update_status()
    
    def _update_power_consumption(self):
        """更新功率消耗"""
        if self.mode == "off":
            self.power_consumption = 0
        elif self.mode == "heat":
            if self.current_temp < self.target_temp:
                self.power_consumption = 1500  # 加热时消耗1500W
            else:
                self.power_consumption = 0
        elif self.mode == "cool":
            if self.current_temp > self.target_temp:
                self.power_consumption = 1200  # 制冷时消耗1200W
            else:
                self.power_consumption = 0
        else:  # auto模式
            if abs(self.current_temp - self.target_temp) > 0.5:
                self.power_consumption = 1000  # 自动模式下消耗1000W
            else:
                self.power_consumption = 0 