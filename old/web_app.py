"""
智能家居设备模拟器Web界面

提供Web界面用于管理设备模拟和查看设备状态。
支持添加、删除设备，以及实时查看设备状态。
"""

from flask import Flask, render_template, jsonify, request
from .devices import (
    Light, Thermostat, DoorLock, Blind,
    AirConditioner, SmokeDetector, Fan, Plug
)
import threading
import time
import json
from typing import Dict, Any, Type
import paho.mqtt.client as mqtt
from dotenv import load_dotenv
import os
import random

# 加载环境变量
load_dotenv()

app = Flask(__name__)

# MQTT配置
broker_ip = os.getenv("BROKER_IP")
broker_port = int(os.getenv("BROKER_PORT"))
device_prefix = os.getenv("DEVICE_PREFIX")

# 设备类型映射
DEVICE_TYPES = {
    "light": Light,
    "thermostat": Thermostat,
    "doorlock": DoorLock,
    "blind": Blind,
    "ac": AirConditioner,
    "smoke_detector": SmokeDetector,
    "fan": Fan,
    "plug": Plug
}

# 存储设备实例
devices: Dict[str, Any] = {}

# MQTT客户端
mqtt_client = mqtt.Client(client_id="WebSimulator")

def on_message(client, userdata, msg):
    """处理接收到的MQTT消息"""
    try:
        device_id = msg.topic.split('/')[-1]
        if device_id in devices:
            command = json.loads(msg.payload)
            devices[device_id].handle_command(command)
    except Exception as e:
        print(f"Error handling message: {e}")

def publish_status(device_id: str):
    """发布设备状态到MQTT主题"""
    topic = f"{device_prefix}/status/{device_id}"
    payload = devices[device_id].to_dict()
    mqtt_client.publish(topic, json.dumps(payload))

def start_mqtt_client():
    """启动MQTT客户端"""
    mqtt_client.connect(broker_ip, broker_port, 60)
    mqtt_client.on_message = on_message
    mqtt_client.loop_start()

def start_device_simulator():
    """启动设备模拟器线程"""
    while True:
        for device_id, device in devices.items():
            publish_status(device_id)
            
            # 模拟传感器数据变化
            if isinstance(device, Thermostat) and random.random() < 0.3:
                new_temp = round(random.uniform(20, 30), 1)
                device.update_current_temp(new_temp)
            
            if isinstance(device, SmokeDetector) and random.random() < 0.1:
                device.trigger_alarm()
        
        time.sleep(10)

@app.route('/')
def index():
    """渲染主页"""
    return render_template('index.html', device_types=DEVICE_TYPES.keys())

@app.route('/api/devices', methods=['GET'])
def get_devices():
    """获取所有设备状态"""
    return jsonify({
        device_id: device.to_dict()
        for device_id, device in devices.items()
    })

@app.route('/api/devices', methods=['POST'])
def add_device():
    """添加新设备"""
    data = request.json
    device_type = data.get('type')
    device_id = data.get('id')
    
    if not device_type or not device_id:
        return jsonify({'error': 'Missing device type or ID'}), 400
    
    if device_id in devices:
        return jsonify({'error': 'Device ID already exists'}), 400
    
    if device_type not in DEVICE_TYPES:
        return jsonify({'error': 'Invalid device type'}), 400
    
    # 创建设备实例
    device_class = DEVICE_TYPES[device_type]
    devices[device_id] = device_class(device_id)
    
    # 订阅设备控制主题
    control_topic = f"{device_prefix}/control/{device_id}"
    mqtt_client.subscribe(control_topic)
    
    return jsonify({'message': 'Device added successfully'})

@app.route('/api/devices/<device_id>', methods=['GET'])
def get_device(device_id):
    """获取单个设备状态"""
    print(f"Getting status for device: {device_id}")
    if device_id not in devices:
        print(f"Device not found: {device_id}")
        return jsonify({'error': 'Device not found'}), 404
    device_data = devices[device_id].to_dict()
    print(f"Device data: {device_data}")
    return jsonify(device_data)

@app.route('/api/devices/<device_id>', methods=['DELETE'])
def remove_device(device_id):
    """删除设备"""
    if device_id not in devices:
        return jsonify({'error': 'Device not found'}), 404
    
    # 取消订阅设备控制主题
    control_topic = f"{device_prefix}/control/{device_id}"
    mqtt_client.unsubscribe(control_topic)
    
    del devices[device_id]
    return jsonify({'message': 'Device removed successfully'})

@app.route('/api/devices/<device_id>/command', methods=['POST'])
def send_command(device_id):
    """发送设备控制命令"""
    if device_id not in devices:
        return jsonify({'error': 'Device not found'}), 404
    
    command = request.json
    devices[device_id].handle_command(command)
    publish_status(device_id)
    
    return jsonify({'message': 'Command sent successfully'})

if __name__ == '__main__':
    # 启动MQTT客户端
    start_mqtt_client()
    
    # 启动设备模拟器线程
    simulator_thread = threading.Thread(target=start_device_simulator, daemon=True)
    simulator_thread.start()
    
    # 启动Web服务器
    app.run(debug=True, host='0.0.0.0', port=5000) 