"""
Flask应用工厂
"""
import os
import threading
import time
import json
import paho.mqtt.client as mqtt
from flask import Flask
from .routes.device_routes import device_bp
from .services.device_manager import DeviceManager
from config import get_config
from flask_cors import CORS
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

def create_app():
    """创建Flask应用实例"""
    app = Flask(__name__)
    
    # 启用CORS
    CORS(app, resources={
        r"/api/*": {
            "origins": ["http://localhost:5173"],  # Vue开发服务器地址
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type"]
        }
    })
    
    # 加载配置
    app.config.from_object(get_config())
    
    # 初始化MQTT客户端
    mqtt_client = mqtt.Client(client_id="WebSimulator")
    mqtt_client.connect(
        os.getenv('BROKER_IP', 'localhost'),
        int(os.getenv('BROKER_PORT', 1883)),
        60
    )
    
    # 初始化设备管理器
    device_manager = DeviceManager(
        mqtt_client,
        os.getenv('DEVICE_PREFIX', 'device')
    )
    
    # 将设备管理器添加到应用上下文
    app.device_manager = device_manager
    
    # 注册路由蓝图
    app.register_blueprint(device_bp, url_prefix='/api')
    
    # 启动MQTT客户端
    mqtt_client.loop_start()
    
    # 启动设备状态更新线程
    def update_devices():
        while True:
            device_manager.publish_all_status()
            time.sleep(5)  # 每5秒更新一次
    
    update_thread = threading.Thread(target=update_devices, daemon=True)
    update_thread.start()
    
    return app 