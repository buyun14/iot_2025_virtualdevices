"""
风扇设备模型
"""
from typing import Dict, Any
from .base import BaseDevice

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
        self.power_consumption = 0  # 功率消耗（瓦特）
    
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
            self._update_power_consumption()
        elif cmd_type == "turn_off":
            self.on = False
            self.power_consumption = 0
        elif cmd_type == "set_speed":
            try:
                speed = int(command.get("speed", 1))
                self.speed = max(1, min(3, speed))
                if self.on:
                    self._update_power_consumption()
            except (ValueError, TypeError):
                self.error_state = "无效的风速值"
        elif cmd_type == "toggle_oscillate":
            self.oscillate = not self.oscillate
            if self.on:
                self._update_power_consumption()
        elif cmd_type == "set_timer":
            try:
                timer = int(command.get("minutes", 0))
                self.timer = max(0, min(120, timer))
            except (ValueError, TypeError):
                self.error_state = "无效的定时值"
        self.update_status()
    
    def _update_power_consumption(self):
        """更新功率消耗"""
        if not self.on:
            self.power_consumption = 0
            return
        
        # 基础功率消耗（根据风速）
        base_power = self.speed * 20  # 1档20W，2档40W，3档60W
        
        # 摇摆功能额外消耗
        oscillate_power = 10 if self.oscillate else 0
        
        self.power_consumption = base_power + oscillate_power 