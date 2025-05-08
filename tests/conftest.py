import pytest
import os
from dotenv import load_dotenv
from unittest.mock import patch

# 加载测试环境变量
@pytest.fixture(autouse=True)
def setup_test_env():
    # 设置测试环境变量
    os.environ['BROKER_IP'] = 'localhost'
    os.environ['BROKER_PORT'] = '1883'
    os.environ['DEVICE_PREFIX'] = 'test/devices'
    yield
    # 清理环境变量
    os.environ.pop('BROKER_IP', None)
    os.environ.pop('BROKER_PORT', None)
    os.environ.pop('DEVICE_PREFIX', None)

@pytest.fixture(autouse=True)
def mock_env_vars():
    """模拟环境变量"""
    with patch.dict(os.environ, {
        'BROKER_IP': 'localhost',
        'BROKER_PORT': '1883',
        'DEVICE_PREFIX': 'test/devices'
    }):
        yield

@pytest.fixture
def mock_mqtt(mocker):
    """模拟MQTT客户端"""
    mock_client = mocker.patch('paho.mqtt.client.Client')
    mock_instance = mock_client.return_value
    mock_instance.connect.return_value = 0
    mock_instance.subscribe.return_value = None
    mock_instance.publish.return_value = None
    return mock_instance 