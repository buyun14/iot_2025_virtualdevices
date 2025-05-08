"""
空调设备模型
"""
from typing import Dict, Any
from .base import BaseDevice

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
        self.power_consumption = 0  # 功率消耗（瓦特）
    
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
            self._update_power_consumption()
        elif cmd_type == "turn_off":
            self.on = False
            self.power_consumption = 0
        elif cmd_type == "set_temp":
            try:
                temp = float(command.get("temperature", 26))
                self.temp = max(16, min(30, temp))
                if self.on:
                    self._update_power_consumption()
            except (ValueError, TypeError):
                self.error_state = "无效的温度值"
        elif cmd_type == "set_mode":
            mode = command.get("mode", "cool")
            if mode in ["cool", "heat", "dry", "fan"]:
                self.mode = mode
                if self.on:
                    self._update_power_consumption()
            else:
                self.error_state = "无效的模式"
        elif cmd_type == "set_fan_speed":
            speed = command.get("speed", "auto")
            if speed in ["auto", "low", "medium", "high"]:
                self.fan_speed = speed
                if self.on:
                    self._update_power_consumption()
            else:
                self.error_state = "无效的风速"
        elif cmd_type == "toggle_swing":
            self.swing = not self.swing
            if self.on:
                self._update_power_consumption()
        self.update_status()
    
    def _update_power_consumption(self):
        """更新功率消耗"""
        if not self.on:
            self.power_consumption = 0
            return
        
        # 基础功率消耗
        base_power = {
            "cool": 1000,
            "heat": 1200,
            "dry": 800,
            "fan": 100
        }.get(self.mode, 1000)
        
        # 风速影响
        speed_multiplier = {
            "auto": 1.0,
            "low": 0.8,
            "medium": 1.0,
            "high": 1.2
        }.get(self.fan_speed, 1.0)
        
        # 摇摆功能额外消耗
        swing_power = 50 if self.swing else 0
        
        self.power_consumption = base_power * speed_multiplier + swing_power 