"""
智能窗帘设备模型
"""
from typing import Dict, Any
from datetime import datetime
from .base import BaseDevice

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
        self.power_consumption = 0  # 功率消耗（瓦特）
    
    def get_state(self) -> Dict[str, Any]:
        return {
            "position": self.position,
            "tilt": self.tilt,
            "moving": self.moving,
            "last_move_time": self.last_move_time,
            "power_consumption": self.power_consumption
        }
    
    def handle_command(self, command: Dict[str, Any]) -> None:
        cmd_type = command.get("command")
        if cmd_type == "open":
            self.position = 100
            self.moving = True
            self.power_consumption = 50  # 移动时消耗50W
        elif cmd_type == "close":
            self.position = 0
            self.moving = True
            self.power_consumption = 50
        elif cmd_type == "set_position":
            try:
                position = int(command.get("position", 0))
                self.position = max(0, min(100, position))
                self.moving = True
                self.power_consumption = 50
            except (ValueError, TypeError):
                self.error_state = "无效的位置值"
        elif cmd_type == "set_tilt":
            try:
                tilt = int(command.get("tilt", 0))
                self.tilt = max(0, min(180, tilt))
                self.power_consumption = 20  # 调整倾斜角度时消耗20W
            except (ValueError, TypeError):
                self.error_state = "无效的倾斜角度"
        
        if self.moving:
            self.last_move_time = datetime.now().isoformat()
            # 模拟移动完成
            self.moving = False
            self.power_consumption = 0
        self.update_status() 