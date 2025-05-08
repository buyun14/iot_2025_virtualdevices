# 智能家居设备模拟器

这是一个智能家居设备模拟器项目，用于模拟各种智能家居设备的行为和状态。该项目支持多种设备类型，包括智能灯、温控器、门锁、窗帘、空调、烟雾报警器、风扇和智能插座等。

## 功能特点

- 支持多种智能家居设备类型
- 实时设备状态监控
- MQTT通信支持
- RESTful API接口
- Web界面管理
- 设备模拟和测试功能

## 设备类型

- 智能灯 (Light)
- 温控器 (Thermostat)
- 智能门锁 (DoorLock)
- 智能窗帘 (Blind)
- 空调 (AirConditioner)
- 烟雾报警器 (SmokeDetector)
- 风扇 (Fan)
- 智能插座 (Plug)

详细设备说明请参考 [设备类型文档](文档/设备类型.md)

## 环境要求

- Python 3.8+
- MQTT Broker (如 Mosquitto)
- 现代浏览器

## 安装步骤

1. 克隆项目：
```bash
git clone [项目地址]
cd virtual_devices_IOT
```

2. 创建并激活虚拟环境：
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux/Mac
python3 -m venv .venv
source .venv/bin/activate
```

3. 安装依赖：
```bash
pip install -r requirements.txt
```

4. 配置环境变量：
创建 `.env` 文件并设置以下变量：
```env
BROKER_IP=localhost
BROKER_PORT=1883
DEVICE_PREFIX=home/devices
```

## 运行应用

1. 确保MQTT Broker已启动

2. 启动Web应用：
```bash
python -m old.web_app
```

3. 访问Web界面：
打开浏览器访问 `http://localhost:5000`

## 运行测试

1. 安装测试依赖：
```bash
pip install -r requirements-test.txt
```

2. 运行所有测试：
```bash
pytest tests/
```

3. 运行特定测试：
```bash
# 运行设备测试
pytest tests/test_devices.py

# 运行API测试
pytest tests/test_web_api.py

# 运行MQTT测试
pytest tests/test_mqtt.py
```

## 测试说明

项目包含以下测试模块：

1. 设备测试 (`test_devices.py`)
   - 基础设备功能测试
   - 智能灯控制测试
   - 温控器功能测试
   - 空调功能测试

2. Web API测试 (`test_web_api.py`)
   - 设备添加测试
   - 设备状态获取测试
   - 设备命令发送测试

3. MQTT测试 (`test_mqtt.py`)
   - 消息发布订阅测试
   - 错误处理测试

## API文档

### RESTful API

- `GET /api/devices` - 获取所有设备状态
- `POST /api/devices` - 添加新设备
- `GET /api/devices/<device_id>` - 获取单个设备状态
- `DELETE /api/devices/<device_id>` - 删除设备
- `POST /api/devices/<device_id>/command` - 发送设备控制命令

### MQTT主题

- 设备状态主题：`{device_prefix}/status/{device_id}`
- 设备控制主题：`{device_prefix}/control/{device_id}`

详细MQTT通信规范请参考 [MQTT通信规范](文档/MQTT通信规范.md)

## 项目结构

```
virtual_devices_IOT/
├── old/
│   ├── __init__.py
│   ├── devices.py      # 设备类定义
│   ├── web_app.py      # Web应用
│   └── templates/      # Web模板
├── tests/
│   ├── conftest.py     # 测试配置
│   ├── test_devices.py # 设备测试
│   ├── test_web_api.py # API测试
│   └── test_mqtt.py    # MQTT测试
├── 文档/
│   ├── 设备类型.md     # 设备类型说明
│   └── MQTT通信规范.md # MQTT通信规范
├── requirements.txt    # 项目依赖
├── requirements-test.txt # 测试依赖
└── README.md          # 项目说明
```

## 贡献指南

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

## 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 联系方式

如有问题或建议，请提交 Issue 或 Pull Request。 