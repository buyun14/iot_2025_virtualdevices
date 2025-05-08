import paho.mqtt.client as mqtt
import random
import time
import json
from dotenv import load_dotenv  # 导入 dotenv 模块
import os

# 加载 .env 文件中的环境变量
load_dotenv()

# 从 .env 文件中读取 MQTT 参数
broker_ip = os.getenv("BROKER_IP")  # MQTT Broker IP 地址
broker_port = int(os.getenv("BROKER_PORT"))  # MQTT Broker 端口，转换为整数
topic = os.getenv("TOPIC")  # 发布主题

# 创建 MQTT 客户端
client = mqtt.Client()

# 连接到 MQTT Broker
client.connect(broker_ip, broker_port, 60)

# 开始循环
client.loop_start()

# 模拟传感器
try:
    sensor_types = [
        "temperature", 
        "humidity", 
        "soil_moisture", 
        "light_intensity", 
        "air_quality_index", 
        "co2_level", 
        "pressure"
    ] # 传感器类型列表
    
    sensor_ids = [1, 2, 3, 4]  # 每种类型的唯一 ID
    while True:
        # 随机选择传感器类型和 ID
        sensor_type = random.choice(sensor_types)
        sensor_id = random.choice(sensor_ids)
        type_id = f"{sensor_type}-{sensor_id}"  # 组合为 type_id 格式

        # 生成随机值（根据传感器类型）
        if sensor_type == "temperature":
            value = random.randint(5, 35)  # 温度范围：5 到 35 摄氏度
        elif sensor_type == "humidity":
            value = random.randint(30, 90)  # 湿度范围：30% 到 90%
        elif sensor_type == "soil_moisture":
            value = random.randint(0, 100)  # 土壤湿度范围：0% 到 100%
        elif sensor_type == "light_intensity":
            value = random.randint(0, 1000)  # 光照强度范围：0 到 1000 lux
        elif sensor_type == "air_quality_index":
            value = random.randint(0, 500)  # 空气质量指数范围：0 到 500
        elif sensor_type == "co2_level":
            value = random.randint(350, 2000)  # CO2浓度范围：350 到 2000 ppm
        elif sensor_type == "pressure":
            value = random.randint(950, 1050)  # 压力范围：950 到 1050 hPa

        # 构造消息
        payload = {
            "type": sensor_type,
            "id": sensor_id,
            "value": value,
        }

        # 发布消息
        client.publish(topic, json.dumps(payload))
        print(f"Published: {payload}")

        # 等待一段时间
        time.sleep(5)

except KeyboardInterrupt:
    print("模拟传感器已停止")

finally:
    # 停止 MQTT 循环
    client.loop_stop()
    client.disconnect()