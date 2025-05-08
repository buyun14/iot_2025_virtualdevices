import pytest
from datetime import datetime
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from old.devices import BaseDevice, Light, Thermostat, AirConditioner

# 基础设备测试
def test_base_device():
    # 使用Light作为具体实现来测试基础设备功能
    device = Light("test-device-001")
    assert device.device_id == "test-device-001"
    assert device.online == True
    assert device.error_state == None
    assert isinstance(device.last_update, datetime)

# 智能灯测试
def test_light():
    light = Light("light-001")
    # 测试开关控制
    light.handle_command({"command": "turn_on"})
    assert light.state == "on"
    assert light.power_consumption > 0
    
    light.handle_command({"command": "turn_off"})
    assert light.state == "off"
    assert light.power_consumption == 0
    
    # 测试亮度调节
    light.handle_command({"command": "set_brightness", "brightness": 75})
    assert light.brightness == 75
    
    # 测试色温调节
    light.handle_command({"command": "set_color_temp", "color_temp": 5000})
    assert light.color_temp == 5000

# 温控器测试
def test_thermostat():
    thermostat = Thermostat("thermostat-001")
    # 测试温度设置
    thermostat.handle_command({"command": "set_target_temp", "temperature": 25})
    assert thermostat.target_temp == 25
    
    # 测试模式切换
    thermostat.handle_command({"command": "set_mode", "mode": "cool"})
    assert thermostat.mode == "cool"
    
    # 测试风速调节
    thermostat.handle_command({"command": "set_fan_speed", "speed": "high"})
    assert thermostat.fan_speed == "high"

# 空调测试
def test_airconditioner():
    ac = AirConditioner("ac-001")
    # 测试开关控制
    ac.handle_command({"command": "turn_on"})
    assert ac.on == True
    assert ac.power_consumption > 0
    
    # 测试温度设置
    ac.handle_command({"command": "set_temp", "temp": 26})
    assert ac.temp == 26
    
    # 测试模式切换
    ac.handle_command({"command": "set_mode", "mode": "heat"})
    assert ac.mode == "heat"
    
    # 测试摆风控制
    ac.handle_command({"command": "toggle_swing"})
    assert ac.swing == True 