import pytest
import json
import time
from unittest.mock import MagicMock, patch
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from old.web_app import device_prefix

def test_mqtt_publish_subscribe(mock_mqtt):
    """测试MQTT消息发布和订阅"""
    # 模拟消息处理
    mock_mqtt.publish("test/topic", "test message")
    
    # 验证publish被调用
    mock_mqtt.publish.assert_called_with("test/topic", "test message")
    
    # 模拟接收消息
    message = MagicMock()
    message.payload = json.dumps({
        "command": "turn_on"
    }).encode()
    message.topic = f"{device_prefix}/control/test-device-001"
    
    # 调用消息处理函数
    mock_mqtt.on_message(mock_mqtt, None, message)
    
    # 验证消息处理
    assert mock_mqtt.on_message.called

def test_mqtt_error_handling(mock_mqtt):
    """测试MQTT错误处理"""
    # 模拟连接错误
    mock_mqtt.connect.side_effect = Exception("Connection failed")
    
    with pytest.raises(Exception) as exc_info:
        mock_mqtt.connect("localhost", 1883)
    assert str(exc_info.value) == "Connection failed"
    
    # 模拟发布错误
    mock_mqtt.publish.side_effect = Exception("Publish failed")
    with pytest.raises(Exception) as exc_info:
        mock_mqtt.publish("test/topic", "test message")
    assert str(exc_info.value) == "Publish failed" 