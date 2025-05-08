"""
智能家居设备模拟器主程序

此程序模拟了多个智能家居设备的行为，通过MQTT协议与外部系统进行通信。
设备状态会定期发布，并响应来自控制端的命令。
"""

import paho.mqtt.client as mqtt
import random
import time
import json
from dotenv import load_dotenv
import os
from devices import (
    Light, Thermostat, DoorLock, Blind,
    AirConditioner, SmokeDetector, Fan, Plug
)

# 加载环境变量
load_dotenv()

# MQTT 配置
broker_ip = os.getenv("BROKER_IP")
broker_port = int(os.getenv("BROKER_PORT"))
device_prefix = os.getenv("DEVICE_PREFIX")

# 创建客户端
client = mqtt.Client(client_id="HomeSimulator")

# 初始化设备实例
devices = {
    "light-001": Light("light-001"),
    "thermostat-001": Thermostat("thermostat-001"),
    "doorlock-001": DoorLock("doorlock-001"),
    "blind-001": Blind("blind-001"),
    "ac-001": AirConditioner("ac-001"),
    "smoke_detector-001": SmokeDetector("smoke_detector-001"),
    "fan-001": Fan("fan-001"),
    "plug-001": Plug("plug-001")
}

def on_message(client, userdata, msg):
    """
    处理接收到的MQTT消息
    
    Args:
        client: MQTT客户端实例
        userdata: 用户数据
        msg: 接收到的消息
    """
    for device_id, device in devices.items():
        control_topic = f"{device_prefix}/control/{device_id}"
        if msg.topic == control_topic:
            try:
                command = json.loads(msg.payload)
                print(f"Received command for {device_id}: {command}")
                device.handle_command(command)
                publish_status(device_id)
            except Exception as e:
                print(f"Error parsing command: {e}")

def publish_status(device_id):
    """
    发布设备状态到MQTT主题
    
    Args:
        device_id (str): 设备ID
    """
    topic = f"{device_prefix}/status/{device_id}"
    payload = devices[device_id].to_dict()
    client.publish(topic, json.dumps(payload))
    print(f"Published status of {device_id} to {topic}: {payload}")

# 连接到 MQTT Broker
client.connect(broker_ip, broker_port, 60)
client.on_message = on_message

# 订阅所有设备的控制主题
for device_id in devices:
    control_topic = f"{device_prefix}/control/{device_id}"
    client.subscribe(control_topic)
    print(f"Subscribed to {control_topic}")

client.loop_start()

# 模拟运行
try:
    while True:
        # 定期发布状态
        for device_id in devices:
            publish_status(device_id)

        # 模拟传感器数据变化
        if random.random() < 0.3:  # 30%概率改变温度
            new_temp = round(random.uniform(20, 30), 1)
            devices["thermostat-001"].update_current_temp(new_temp)

        if random.random() < 0.1:  # 10%概率触发烟雾报警
            devices["smoke_detector-001"].trigger_alarm()

        time.sleep(10)  # 每10秒更新一次状态

except KeyboardInterrupt:
    print("Stopping simulator...")

finally:
    client.loop_stop()
    client.disconnect()