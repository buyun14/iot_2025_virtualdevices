"""
门锁设备模型
"""
from typing import Dict, Any
from .base import BaseDevice

class DoorLock(BaseDevice):
    """门锁设备类"""
    
    def __init__(self, device_id: str):
        """
        初始化门锁设备
        
        Args:
            device_id (str): 设备唯一标识符
        """
        super().__init__(device_id)
        self.locked = True  # 是否上锁
        self.battery_level = 100  # 电池电量
        self.last_lock_time = None  # 最后上锁时间
        self.last_unlock_time = None  # 最后解锁时间
        self.tamper_alert = False  # 防撬警报
    
    def get_state(self) -> Dict[str, Any]:
        return {
            "locked": self.locked,
            "battery_level": self.battery_level,
            "last_lock_time": self.last_lock_time,
            "last_unlock_time": self.last_unlock_time,
            "tamper_alert": self.tamper_alert
        }
    
    def handle_command(self, command: Dict[str, Any]) -> None:
        cmd_type = command.get("command")
        if cmd_type == "lock":
            self.locked = True
            self.last_lock_time = self.last_update
            self.tamper_alert = False
        elif cmd_type == "unlock":
            self.locked = False
            self.last_unlock_time = self.last_update
            self.tamper_alert = False
        elif cmd_type == "check_battery":
            # 模拟电池电量缓慢下降
            self.battery_level = max(0, self.battery_level - 1)
            if self.battery_level < 20:
                self.error_state = "电池电量低"
        self.update_status() 