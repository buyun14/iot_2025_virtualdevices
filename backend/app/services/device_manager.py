"""
设备管理服务
"""
import json
from typing import Dict, Any, Type
import paho.mqtt.client as mqtt
from ..models.base import BaseDevice
from ..models.light import Light
# 导入其他设备模型...

class DeviceManager:
    """设备管理服务类"""
    
    def __init__(self, mqtt_client: mqtt.Client, device_prefix: str):
        """
        初始化设备管理器
        
        Args:
            mqtt_client (mqtt.Client): MQTT客户端实例
            device_prefix (str): MQTT主题前缀
        """
        self.devices: Dict[str, BaseDevice] = {}
        self.mqtt_client = mqtt_client
        self.device_prefix = device_prefix
        
        # 设备类型映射
        self.device_types: Dict[str, Type[BaseDevice]] = {
            "light": Light,
            # 添加其他设备类型...
        }
    
    def add_device(self, device_type: str, device_id: str) -> bool:
        """
        添加新设备
        
        Args:
            device_type (str): 设备类型
            device_id (str): 设备ID
            
        Returns:
            bool: 是否添加成功
        """
        if device_id in self.devices:
            return False
        
        if device_type not in self.device_types:
            return False
        
        # 创建设备实例
        device_class = self.device_types[device_type]
        self.devices[device_id] = device_class(device_id)
        
        # 订阅设备控制主题
        control_topic = f"{self.device_prefix}/control/{device_id}"
        self.mqtt_client.subscribe(control_topic)
        
        return True
    
    def remove_device(self, device_id: str) -> bool:
        """
        删除设备
        
        Args:
            device_id (str): 设备ID
            
        Returns:
            bool: 是否删除成功
        """
        if device_id not in self.devices:
            return False
        
        # 取消订阅设备控制主题
        control_topic = f"{self.device_prefix}/control/{device_id}"
        self.mqtt_client.unsubscribe(control_topic)
        
        del self.devices[device_id]
        return True
    
    def get_device(self, device_id: str) -> BaseDevice:
        """
        获取设备实例
        
        Args:
            device_id (str): 设备ID
            
        Returns:
            BaseDevice: 设备实例
        """
        return self.devices.get(device_id)
    
    def get_all_devices(self) -> Dict[str, Dict[str, Any]]:
        """
        获取所有设备状态
        
        Returns:
            Dict[str, Dict[str, Any]]: 设备状态字典
        """
        return {
            device_id: device.to_dict()
            for device_id, device in self.devices.items()
        }
    
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
        self.publish_status(device_id)
        return True
    
    def publish_status(self, device_id: str) -> None:
        """
        发布设备状态
        
        Args:
            device_id (str): 设备ID
        """
        device = self.get_device(device_id)
        if not device:
            return
        
        topic = f"{self.device_prefix}/status/{device_id}"
        payload = device.to_dict()
        self.mqtt_client.publish(topic, json.dumps(payload))
    
    def publish_all_status(self) -> None:
        """发布所有设备状态"""
        for device_id in self.devices:
            self.publish_status(device_id) 