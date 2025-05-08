"""
Flask应用工厂
"""
import threading
import time
import json
import paho.mqtt.client as mqtt
from flask import Flask
from .routes.device_routes import device_bp, device_manager
from .services.device_manager import DeviceManager
from ..config import get_config

def create_app():
    """创建Flask应用实例"""
    app = Flask(__name__)
    
    # 加载配置
    app.config.from_object(get_config())
    
    # 初始化MQTT客户端
    mqtt_client = mqtt.Client(client_id="WebSimulator")
    mqtt_client.connect(
        app.config['MQTT_BROKER'],
        app.config['MQTT_PORT'],
        60
    )
    
    # 初始化设备管理器
    global device_manager
    device_manager = DeviceManager(
        mqtt_client,
        app.config['MQTT_DEVICE_PREFIX']
    )
    
    # 注册路由蓝图
    app.register_blueprint(device_bp)
    
    # 启动MQTT客户端
    mqtt_client.loop_start()
    
    # 启动设备状态更新线程
    def update_devices():
        while True:
            device_manager.publish_all_status()
            time.sleep(app.config['DEVICE_UPDATE_INTERVAL'])
    
    update_thread = threading.Thread(target=update_devices, daemon=True)
    update_thread.start()
    
    return app 