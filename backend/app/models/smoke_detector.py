"""
烟雾报警器设备模型
"""
from typing import Dict, Any
from datetime import datetime
import random
from .base import BaseDevice

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
        self.power_consumption = 0  # 功率消耗（瓦特）
    
    def get_state(self) -> Dict[str, Any]:
        return {
            "alarm": self.alarm,
            "battery_level": self.battery_level,
            "smoke_level": self.smoke_level,
            "last_test_time": self.last_test_time,
            "power_consumption": self.power_consumption
        }
    
    def handle_command(self, command: Dict[str, Any]) -> None:
        cmd_type = command.get("command")
        if cmd_type == "reset":
            self.alarm = False
            self.smoke_level = 0
            self.power_consumption = 0
        elif cmd_type == "test":
            self.last_test_time = datetime.now().isoformat()
            self.battery_level = max(0, self.battery_level - 0.5)
            self.power_consumption = 10  # 测试时消耗10W
            # 测试完成后恢复
            self.power_consumption = 0
        self.update_status()
    
    def trigger_alarm(self) -> None:
        """触发烟雾报警"""
        self.alarm = True
        self.smoke_level = random.randint(50, 100)
        self.power_consumption = 20  # 报警时消耗20W
        self.update_status() 