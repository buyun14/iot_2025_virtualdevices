"""
智能插座设备模型
"""
from typing import Dict, Any
from .base import BaseDevice

class SmartPlug(BaseDevice):
    """智能插座设备类"""
    
    def __init__(self, device_id: str):
        """
        初始化智能插座设备
        
        Args:
            device_id (str): 设备唯一标识符
        """
        super().__init__(device_id)
        self.on = False
        self.power_consumption = 0  # 功率消耗（瓦特）
        self.voltage = 220  # 电压（伏特）
        self.current = 0  # 电流（安培）
        self.timer = 0  # 定时关闭时间（分钟）
        self.schedule = []  # 定时任务列表
    
    def get_state(self) -> Dict[str, Any]:
        return {
            "on": self.on,
            "power_consumption": self.power_consumption,
            "voltage": self.voltage,
            "current": self.current,
            "timer": self.timer,
            "schedule": self.schedule
        }
    
    def handle_command(self, command: Dict[str, Any]) -> None:
        cmd_type = command.get("command")
        if cmd_type == "turn_on":
            self.on = True
            self._update_power_consumption()
        elif cmd_type == "turn_off":
            self.on = False
            self.power_consumption = 0
            self.current = 0
        elif cmd_type == "set_timer":
            try:
                timer = int(command.get("minutes", 0))
                self.timer = max(0, min(1440, timer))  # 最大24小时
            except (ValueError, TypeError):
                self.error_state = "无效的定时值"
        elif cmd_type == "add_schedule":
            try:
                schedule = command.get("schedule", {})
                if self._validate_schedule(schedule):
                    self.schedule.append(schedule)
            except (ValueError, TypeError):
                self.error_state = "无效的定时任务"
        elif cmd_type == "remove_schedule":
            try:
                index = int(command.get("index", -1))
                if 0 <= index < len(self.schedule):
                    self.schedule.pop(index)
            except (ValueError, TypeError):
                self.error_state = "无效的定时任务索引"
        self.update_status()
    
    def _validate_schedule(self, schedule: Dict[str, Any]) -> bool:
        """验证定时任务格式"""
        required_fields = ["time", "action"]
        if not all(field in schedule for field in required_fields):
            return False
        
        try:
            time = schedule["time"]
            if not isinstance(time, str) or len(time) != 5:  # HH:MM格式
                return False
            
            hour, minute = map(int, time.split(":"))
            if not (0 <= hour <= 23 and 0 <= minute <= 59):
                return False
            
            if schedule["action"] not in ["turn_on", "turn_off"]:
                return False
            
            return True
        except (ValueError, TypeError):
            return False
    
    def _update_power_consumption(self):
        """更新功率消耗"""
        if not self.on:
            self.power_consumption = 0
            self.current = 0
            return
        
        # 模拟负载变化
        self.current = round(self.power_consumption / self.voltage, 2)
        if self.current > 10:  # 过载保护
            self.on = False
            self.power_consumption = 0
            self.current = 0
            self.error_state = "过载保护已触发" 