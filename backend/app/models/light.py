"""
智能灯设备模型
"""
from typing import Dict, Any
from .base import BaseDevice

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