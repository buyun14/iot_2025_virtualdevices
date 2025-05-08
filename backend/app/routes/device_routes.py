"""
设备API路由
"""
from flask import Blueprint, jsonify, request
from ..services.device_manager import DeviceManager

# 创建设备路由蓝图
device_bp = Blueprint('device', __name__)

# 设备管理器实例（将在应用初始化时设置）
device_manager: DeviceManager = None

@device_bp.route('/api/devices', methods=['GET'])
def get_devices():
    """获取所有设备状态"""
    return jsonify(device_manager.get_all_devices())

@device_bp.route('/api/devices', methods=['POST'])
def add_device():
    """添加新设备"""
    data = request.json
    device_type = data.get('type')
    device_id = data.get('id')
    
    if not device_type or not device_id:
        return jsonify({'error': 'Missing device type or ID'}), 400
    
    if device_manager.add_device(device_type, device_id):
        return jsonify({'message': 'Device added successfully'})
    else:
        return jsonify({'error': 'Failed to add device'}), 400

@device_bp.route('/api/devices/<device_id>', methods=['DELETE'])
def remove_device(device_id):
    """删除设备"""
    if device_manager.remove_device(device_id):
        return jsonify({'message': 'Device removed successfully'})
    else:
        return jsonify({'error': 'Device not found'}), 404

@device_bp.route('/api/devices/<device_id>/command', methods=['POST'])
def send_command(device_id):
    """发送设备控制命令"""
    command = request.json
    if device_manager.handle_command(device_id, command):
        return jsonify({'message': 'Command sent successfully'})
    else:
        return jsonify({'error': 'Device not found'}), 404 