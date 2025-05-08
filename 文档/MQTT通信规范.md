# MQTT 通信规范

本文档详细说明了智能家居设备模拟器的 MQTT 通信规范。

## 环境配置

系统使用环境变量进行 MQTT 配置：
```env
BROKER_IP=your_broker_ip
BROKER_PORT=your_broker_port
DEVICE_PREFIX=your_device_prefix
```

## 主题结构

### 1. 设备状态主题
```
{device_prefix}/status/{device_id}
```
- 用途：发布设备状态更新
- 发布者：设备模拟器
- 订阅者：监控系统、其他设备
- 消息格式：JSON
- 发布频率：每10秒

### 2. 设备控制主题
```
{device_prefix}/control/{device_id}
```
- 用途：接收设备控制命令
- 发布者：控制端、其他设备
- 订阅者：设备模拟器
- 消息格式：JSON
- 发布时机：需要控制设备时

## 消息格式

### 1. 设备状态消息
```json
{
    "type": "设备类型",
    "online": true/false,
    "last_update": "ISO格式时间戳",
    "error_state": "错误信息或null",
    // 设备特定参数
    "param1": "value1",
    "param2": "value2"
}
```

### 2. 设备控制消息
```json
{
    "command": "命令名称",
    "param1": "value1",
    "param2": "value2"
}
```

## 设备特定命令

### 1. 智能灯 (Light)
```json
// 开关控制
{
    "command": "turn_on"
}
{
    "command": "turn_off"
}

// 亮度控制
{
    "command": "set_brightness",
    "brightness": 50
}

// 色温控制
{
    "command": "set_color_temp",
    "color_temp": 4000
}
```

### 2. 温控器 (Thermostat)
```json
// 温度设置
{
    "command": "set_target_temp",
    "temperature": 24
}

// 模式设置
{
    "command": "set_mode",
    "mode": "auto"
}

// 风速设置
{
    "command": "set_fan_speed",
    "speed": "auto"
}
```

### 3. 智能门锁 (DoorLock)
```json
// 上锁/解锁
{
    "command": "lock"
}
{
    "command": "unlock"
}
```

### 4. 智能窗帘 (Blind)
```json
// 开关控制
{
    "command": "open"
}
{
    "command": "close"
}

// 位置控制
{
    "command": "set_position",
    "position": 50
}

// 倾斜角度控制
{
    "command": "set_tilt",
    "tilt": 45
}
```

### 5. 空调 (AirConditioner)
```json
// 开关控制
{
    "command": "turn_on"
}
{
    "command": "turn_off"
}

// 温度设置
{
    "command": "set_temp",
    "temp": 26
}

// 模式设置
{
    "command": "set_mode",
    "mode": "cool"
}

// 风速设置
{
    "command": "set_fan_speed",
    "fan_speed": "auto"
}

// 摆风控制
{
    "command": "toggle_swing"
}
```

### 6. 烟雾报警器 (SmokeDetector)
```json
// 重置报警
{
    "command": "reset"
}

// 测试功能
{
    "command": "test"
}
```

### 7. 风扇 (Fan)
```json
// 开关控制
{
    "command": "turn_on"
}
{
    "command": "turn_off"
}

// 风速设置
{
    "command": "set_speed",
    "speed": 2
}

// 摆头控制
{
    "command": "toggle_oscillate"
}

// 定时设置
{
    "command": "set_timer",
    "minutes": 30
}
```

### 8. 智能插座 (Plug)
```json
// 开关控制
{
    "command": "turn_on"
}
{
    "command": "turn_off"
}

// 定时设置
{
    "command": "set_timer",
    "minutes": 60
}
```

## 错误处理

1. 设备离线状态：
   - 设备有1%的概率随机离线
   - 离线时会在状态消息中设置 `online: false`
   - 同时设置 `error_state` 为 "设备连接异常"

2. 命令错误处理：
   - 无效命令：返回错误消息
   - 参数范围错误：返回错误消息
   - 设备离线：返回错误消息

## 安全建议

1. 使用 TLS/SSL 加密 MQTT 连接
2. 实现适当的认证机制
3. 使用 ACL 控制主题访问权限
4. 定期更新设备固件和证书
5. 监控异常连接和消息

## 最佳实践

1. 消息发布：
   - 使用 QoS 1 确保消息可靠传递
   - 保持消息大小合理
   - 避免过于频繁的状态更新

2. 消息订阅：
   - 使用通配符主题时要谨慎
   - 实现消息去重机制
   - 处理消息积压情况

3. 连接管理：
   - 实现自动重连机制
   - 监控连接状态
   - 记录连接日志

4. 错误处理：
   - 实现优雅的错误恢复
   - 记录错误日志
   - 通知相关人员 