"""
设备管理服务
"""
from typing import Dict, Any, Optional, List
import paho.mqtt.client as mqtt
from ..models.light import Light
from ..models.thermostat import Thermostat
from ..models.doorlock import DoorLock
from ..models.blind import Blind
from ..models.ac import AirConditioner
from ..models.smoke_detector import SmokeDetector
from ..models.fan import Fan
from ..models.smart_plug import SmartPlug

class DeviceManager:
    """设备管理器类"""
    
    def __init__(self, mqtt_client: mqtt.Client, device_prefix: str = "device"):
        """
        初始化设备管理器
        
        Args:
            mqtt_client (mqtt.Client): MQTT客户端实例
            device_prefix (str): 设备主题前缀
        """
        self.mqtt_client = mqtt_client
        self.device_prefix = device_prefix
        self.devices: Dict[str, Any] = {}
        
        # 设备类型映射
        self.device_types = {
            "light": Light,
            "thermostat": Thermostat,
            "doorlock": DoorLock,
            "blind": Blind,
            "ac": AirConditioner,
            "smoke_detector": SmokeDetector,
            "fan": Fan,
            "smart_plug": SmartPlug
        }
    
    def add_device(self, device_id: str, device_type: str) -> bool:
        """
        添加新设备
        
        Args:
            device_id (str): 设备ID
            device_type (str): 设备类型
            
        Returns:
            bool: 是否添加成功
        """
        if device_id in self.devices:
            return False
        
        if device_type not in self.device_types:
            return False
        
        device_class = self.device_types[device_type]
        self.devices[device_id] = device_class(device_id)
        return True
    
    def remove_device(self, device_id: str) -> bool:
        """
        移除设备
        
        Args:
            device_id (str): 设备ID
            
        Returns:
            bool: 是否移除成功
        """
        if device_id not in self.devices:
            return False
        
        del self.devices[device_id]
        return True
    
    def get_device(self, device_id: str) -> Optional[Any]:
        """
        获取设备实例
        
        Args:
            device_id (str): 设备ID
            
        Returns:
            Optional[Any]: 设备实例，如果不存在则返回None
        """
        return self.devices.get(device_id)
    
    def get_all_devices(self) -> List[Dict[str, Any]]:
        """
        获取所有设备状态
        
        Returns:
            List[Dict[str, Any]]: 设备状态列表
        """
        return [
            {
                "id": device_id,
                "type": device.__class__.__name__.lower(),
                "state": device.get_state()
            }
            for device_id, device in self.devices.items()
        ]
    
    def handle_command(self, device_id: str, command: Dict[str, Any]) -> bool:
        """
        处理设备命令
        
        Args:
            device_id (str): 设备ID
            command (Dict[str, Any]): 命令数据
            
        Returns:
            bool: 是否处理成功
        """
        device = self.get_device(device_id)
        if not device:
            return False
        
        device.handle_command(command)
        self.publish_device_status(device_id)
        return True
    
    def publish_device_status(self, device_id: str) -> None:
        """
        发布设备状态
        
        Args:
            device_id (str): 设备ID
        """
        device = self.get_device(device_id)
        if not device:
            return
        
        topic = f"{self.device_prefix}/{device_id}/status"
        status = {
            "id": device_id,
            "type": device.__class__.__name__.lower(),
            "state": device.get_state()
        }
        self.mqtt_client.publish(topic, str(status))
    
    def publish_all_status(self) -> None:
        """发布所有设备状态"""
        for device_id in self.devices:
            self.publish_device_status(device_id) 