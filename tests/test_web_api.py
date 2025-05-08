import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from old.web_app import app
import json

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_add_device(client):
    # 测试添加设备
    response = client.post('/api/devices',
        json={'type': 'light', 'id': 'test-light-001'})
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'message' in data
    
    # 测试重复ID
    response = client.post('/api/devices',
        json={'type': 'light', 'id': 'test-light-001'})
    assert response.status_code == 400
    
    # 测试无效设备类型
    response = client.post('/api/devices',
        json={'type': 'invalid_type', 'id': 'test-invalid-001'})
    assert response.status_code == 400

def test_get_device(client):
    # 先添加一个设备
    client.post('/api/devices',
        json={'type': 'light', 'id': 'test-light-002'})
    
    # 测试获取设备状态
    response = client.get('/api/devices/test-light-002')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['type'] == 'light'
    assert data['online'] == True
    
    # 测试获取不存在的设备
    response = client.get('/api/devices/non-existent')
    assert response.status_code == 404

def test_send_command(client):
    # 先添加一个设备
    client.post('/api/devices',
        json={'type': 'light', 'id': 'test-light-003'})
    
    # 测试发送有效命令
    response = client.post('/api/devices/test-light-003/command',
        json={'command': 'turn_on'})
    assert response.status_code == 200
    
    # 测试发送无效命令
    response = client.post('/api/devices/test-light-003/command',
        json={'command': 'invalid_command'})
    assert response.status_code == 200  # 命令无效但API调用成功
    
    # 测试发送命令到不存在的设备
    response = client.post('/api/devices/non-existent/command',
        json={'command': 'turn_on'})
    assert response.status_code == 404 